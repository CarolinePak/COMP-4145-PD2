# modules/api_client.py

import requests
import json
import time
from typing import Dict, List, Optional, Any
import base64
from config import config

class LLMClient:
    """
    Wrapper for GPT-6-Luna API calls.
    Handles all communication with the LLM endpoint.
    """

    def __init__(self, api_key: str = None, endpoint: str = None, model: str = None):
        """
        Initialize API client.

        Args:
            api_key: API authentication key (defaults to config.API_KEY)
            endpoint: API endpoint URL (defaults to config.API_ENDPOINT)
            model: Model name (defaults to config.MODEL_NAME)
        """
        self.api_key = api_key or config.API_KEY
        self.endpoint = endpoint or config.API_ENDPOINT
        self.model = model or config.MODEL_NAME
        self.timeout = 30  # seconds
        self.max_retries = 3

    def call_llm(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1500,
        response_format: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make API call to LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'
                     Example: [{"role": "system", "content": "..."},
                              {"role": "user", "content": "..."}]
            temperature: Sampling temperature (0.0 to 1.0)
                        Lower = more focused, Higher = more creative
            max_tokens: Maximum tokens in response
            response_format: Expected format hint (e.g., "json", "markdown")

        Returns:
            Dict containing:
                - success: bool
                - response: str (LLM response text)
                - error: str (error message if success=False)
                - tokens_used: int (total tokens consumed)
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Add response format hint if provided
        if response_format:
            payload["response_format"] = {"type": response_format}

        # Retry logic with exponential backoff
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "response": data["choices"][0]["message"]["content"],
                        "error": None,
                        "tokens_used": data.get("usage", {}).get("total_tokens", 0)
                    }

                elif response.status_code == 401:
                    return {
                        "success": False,
                        "response": None,
                        "error": "Invalid API key. Please check your API key in settings.",
                        "tokens_used": 0
                    }

                elif response.status_code == 429:
                    # Rate limit - retry with backoff
                    if attempt < self.max_retries - 1:
                        wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "response": None,
                            "error": "Rate limit exceeded. Please try again later.",
                            "tokens_used": 0
                        }

                else:
                    return {
                        "success": False,
                        "response": None,
                        "error": f"API error: {response.status_code} - {response.text}",
                        "tokens_used": 0
                    }

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return {
                        "success": False,
                        "response": None,
                        "error": "Request timeout. Please check your internet connection.",
                        "tokens_used": 0
                    }

            except Exception as e:
                return {
                    "success": False,
                    "response": None,
                    "error": f"Unexpected error: {str(e)}",
                    "tokens_used": 0
                }

        return {
            "success": False,
            "response": None,
            "error": "Max retries exceeded.",
            "tokens_used": 0
        }

    def encode_image(self, image_bytes: bytes) -> str:
        """
        Encode image to base64 for API transmission.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(image_bytes).decode('utf-8')

    def call_with_image(
        self,
        system_prompt: str,
        user_prompt: str,
        image_bytes: bytes,
        temperature: float = 0.7,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:
        """
        Make API call with image input.

        Args:
            system_prompt: System message (sets behavior)
            user_prompt: User message (task description)
            image_bytes: Image file bytes
            temperature: Sampling temperature
            max_tokens: Maximum response tokens

        Returns:
            Same format as call_llm()
        """

        # Encode image
        image_base64 = self.encode_image(image_bytes)

        # Format messages with image
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]

        return self.call_llm(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

# Create global client instance
llm_client = LLMClient()


def client_for_session() -> LLMClient:
    """Use the current session's key or the configured server default."""
    import streamlit as st

    return LLMClient(api_key=st.session_state.get("api_key"))
