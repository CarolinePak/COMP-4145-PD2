# SkinInsight - System Architecture

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Design Philosophy](#design-philosophy)
- [System Components](#system-components)
	- [1. Application Entry Point](#1-application-entry-point)
	- [2. API Client Module](#2-api-client-module)
	- [3. Skin Analysis Module](#3-skin-analysis-module)
	- [4. Chatbot Module](#4-chatbot-module)
	- [5. Authentication Module](#5-authentication-module)
	- [6. History Analytics Module](#6-history-analytics-module)
	- [7. Recommendations Module](#7-recommendations-module)
	- [8. Prompt Templates](#8-prompt-templates)
- [Data Flow](#data-flow)
	- [Skin Analysis Flow](#skin-analysis-flow)
	- [Chatbot Interaction Flow](#chatbot-interaction-flow)
	- [User History Flow](#user-history-flow)
- [Data Storage Strategy](#data-storage-strategy)
	- [Session State Structure](#session-state-structure)
	- [JSON File Structure](#json-file-structure)
- [UI/UX Architecture](#uiux-architecture)
	- [Page Layout Structure](#page-layout-structure)
	- [Navigation Pattern](#navigation-pattern)
	- [Component Hierarchy](#component-hierarchy)
- [Prompt Engineering Architecture](#prompt-engineering-architecture)
	- [Prompt Structure Standards](#prompt-structure-standards)
	- [Response Format Enforcement](#response-format-enforcement)
- [Error Handling Strategy](#error-handling-strategy)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Scalability & Future Enhancements](#scalability--future-enhancements)

## Architecture Overview

SkinInsight follows a **LLM-Centric Modular Architecture** where the Large Language Model (GPT-6-Luna) serves as the primary processing engine for all intelligent features. The architecture is designed around three core principles:

1. **Prompt-Driven Logic**: Business logic is encoded in prompts rather than hard-coded algorithms
2. **Modular Components**: Each feature is isolated in its own module for maintainability
3. **Stateful UI**: Streamlit session state manages user context across interactions

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                            │
│                   (Streamlit UI)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                     app.py                                  │
│              (Main Application Controller)                  │
│  - Page routing via sidebar                                 │
│  - Session state initialization                             │
│  - Global UI components                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┬─────────────┐
         ↓             ↓             ↓             ↓
┌─────────────┐ ┌─────────────┐ ┌──────────┐ ┌──────────────┐
│   Skin      │ │  Chatbot    │ │  Auth    │ │   History    │
│  Analysis   │ │   Module    │ │  Module  │ │   Module     │
│   Module    │ │             │ │          │ │              │
└──────┬──────┘ └──────┬──────┘ └────┬─────┘ └──────┬───────┘
       │               │              │              │
       └───────────────┴──────────────┴──────────────┘
                       │
                       ↓
              ┌────────────────┐
              │  API Client    │
              │    Module      │
              └────────┬───────┘
                       │
                       ↓
              ┌────────────────────────────┐
              │   GPT-6-Luna API           │
              │ (HKBU LLM Endpoint)        │
              └────────────────────────────┘
```

## Design Philosophy

### LLM-Centric Approach
Instead of building complex backend services, we leverage the LLM's capabilities:
- **Traditional Approach**: Write code → Process data → Return results
- **Our Approach**: Craft prompt → LLM processes → Parse structured output

**Benefits:**
- Rapid development with minimal code
- Flexibility to change behavior via prompt updates
- Natural language understanding for complex tasks
- No need for ML model training or fine-tuning

### Stateless LLM + Stateful UI
- **LLM calls are stateless**: Each API request is independent
- **UI maintains state**: Streamlit session_state preserves context between reruns
- **Best of both worlds**: Scalable API calls + rich user experience

## System Components

### 1. Application Entry Point

**File:** `app.py`

**Purpose:** Main orchestrator that initializes the application, manages navigation, and routes to feature modules.

**Detailed Implementation:**

```python
# app.py structure

import streamlit as st
from modules import skin_analysis, chatbot, auth, history, recommendations
from config import config

# Page configuration (MUST be first Streamlit command)
st.set_page_config(
    page_title="SkinInsight - AI Skin Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.analyses = []
    st.session_state.chat_history = []
    st.session_state.current_analysis = None

# Sidebar navigation
with st.sidebar:
    st.title("🔬 SkinInsight")
    st.markdown("---")
    
    # Navigation menu
    page = st.radio(
        "Navigation",
        ["🏠 Skin Analysis", "💬 Chatbot", "👤 My Profile", "📊 History", "💄 Recommendations"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # API Configuration (collapsible)
    with st.expander("⚙️ API Settings"):
        api_key = st.text_input("API Key", type="password", value=config.API_KEY)
        if st.button("Save API Key"):
            config.API_KEY = api_key
            st.success("API Key saved!")

# Main content area - route to selected page
if page == "🏠 Skin Analysis":
    skin_analysis.render()
elif page == "💬 Chatbot":
    chatbot.render()
elif page == "👤 My Profile":
    auth.render()
elif page == "📊 History":
    history.render()
elif page == "💄 Recommendations":
    recommendations.render()
```

**Key Responsibilities:**
- Initialize Streamlit page configuration (MUST be the first st command)
- Set up session state variables on first run
- Render sidebar navigation
- Route to appropriate module based on selection
- Provide global API configuration interface

**Session State Variables Initialized:**
- `initialized`: Boolean flag to prevent re-initialization
- `user_id`: Unique identifier for current user (UUID)
- `username`: Display name for current user
- `analyses`: List of all analysis results (list of dicts)
- `chat_history`: Chatbot conversation history (list of message dicts)
- `current_analysis`: Most recent analysis result (dict or None)

### 2. API Client Module

**File:** `modules/api_client.py`

**Purpose:** Centralized wrapper for all LLM API communications. Handles request formatting, error handling, retries, and response parsing.

**Detailed Implementation:**

```python
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
```

**Key Features:**
- Exponential backoff retry mechanism (1s → 2s → 4s delays)
- Handles rate limiting (429 errors) gracefully
- Supports both text-only and image+text inputs
- Returns standardized response format
- Centralizes error handling
- Configurable timeout and retry limits

**Response Format:**
```python
{
    "success": True/False,
    "response": "LLM response text here...",
    "error": None or "Error message",
    "tokens_used": 1234
}
```

### 3. Skin Analysis Module

**File:** `modules/skin_analysis.py`

**Purpose:** Core feature for analyzing uploaded skin images and displaying structured KPI results.

**Detailed Implementation:**

```python
# modules/skin_analysis.py

import streamlit as st
import json
from datetime import datetime
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt
import uuid

def render():
    """
    Render the Skin Analysis page.
    Main interface for uploading and analyzing skin images.
    """
    
    st.title("🔬 AI-Powered Skin Analysis")
    st.markdown("Upload a clear face photo for comprehensive skin quality assessment.")
    
    # Create two columns: left for upload, right for results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a face image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear, well-lit photo of your face. Best results with front-facing images.",
            label_visibility="collapsed"
        )
        
        # Display uploaded image
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Skin", type="primary", use_container_width=True):
                analyze_skin(uploaded_file)
        else:
            st.info("👆 Please upload an image to begin analysis")
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        # Display results if available
        if st.session_state.current_analysis:
            display_results(st.session_state.current_analysis)
        else:
            st.info("Results will appear here after analysis")


def analyze_skin(uploaded_file):
    """
    Perform skin analysis using LLM.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    """
    
    # Show loading state
    with st.spinner("🔬 Analyzing your skin... This may take 10-20 seconds."):
        
        # Read image bytes
        image_bytes = uploaded_file.read()
        
        # Load prompt template
        system_prompt = load_prompt("skin_analysis_system")
        user_prompt = load_prompt("skin_analysis_user")
        
        # Call LLM API with image
        result = llm_client.call_with_image(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_bytes=image_bytes,
            temperature=0.3,  # Lower temperature for consistent analysis
            max_tokens=1500
        )
        
        if result["success"]:
            # Parse LLM response
            try:
                analysis_data = parse_analysis_response(result["response"])
                
                # Add metadata
                analysis_data["timestamp"] = datetime.now().isoformat()
                analysis_data["analysis_id"] = str(uuid.uuid4())
                analysis_data["image_name"] = uploaded_file.name
                
                # Store in session state
                st.session_state.current_analysis = analysis_data
                st.session_state.analyses.append(analysis_data)
                
                # Save to file (for history)
                save_analysis(analysis_data)
                
                st.success("✅ Analysis complete!")
                st.rerun()  # Refresh to show results
            
            except json.JSONDecodeError as e:
                st.error(f"❌ Failed to parse analysis results: {str(e)}")
                st.error("Raw response:")
                st.code(result["response"])
        
        else:
            st.error(f"❌ Analysis failed: {result['error']}")


def parse_analysis_response(response_text: str) -> dict:
    """
    Parse LLM response into structured format.
    
    Expected response format from LLM:
    {
        "skin_cleanliness_score": 8,
        "skin_quality_score": 7,
        "age_estimate": 28,
        "skin_condition_description": "...",
        "concerns": ["concern1", "concern2"],
        "recommendations": ["rec1", "rec2"]
    }
    
    Args:
        response_text: Raw LLM response
    
    Returns:
        Parsed dict with structured data
    """
    
    # Try to extract JSON from response
    # LLM might wrap JSON in markdown code blocks
    response_text = response_text.strip()
    
    # Remove markdown code blocks if present
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "", 1)
    if response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]
    
    # Parse JSON
    data = json.loads(response_text.strip())
    
    # Validate required fields
    required_fields = [
        "skin_cleanliness_score",
        "skin_quality_score",
        "age_estimate",
        "skin_condition_description"
    ]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    # Ensure scores are in range [0, 10]
    data["skin_cleanliness_score"] = max(0, min(10, data["skin_cleanliness_score"]))
    data["skin_quality_score"] = max(0, min(10, data["skin_quality_score"]))
    
    return data


def display_results(analysis: dict):
    """
    Display analysis results in structured UI.
    
    Args:
        analysis: Parsed analysis dict
    """
    
    # KPI Cards Row
    st.markdown("### 📈 Key Metrics")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric(
            label="Skin Cleanliness",
            value=f"{analysis['skin_cleanliness_score']}/10",
            delta=None,
            help="Overall cleanliness and clarity of skin"
        )
    
    with metric_col2:
        st.metric(
            label="Skin Quality",
            value=f"{analysis['skin_quality_score']}/10",
            delta=None,
            help="Overall health and condition of skin"
        )
    
    with metric_col3:
        st.metric(
            label="Estimated Age",
            value=f"{analysis['age_estimate']} years",
            delta=None,
            help="AI-estimated age based on skin condition"
        )
    
    # Progress bars for visual representation
    st.markdown("---")
    st.markdown("**Cleanliness Score**")
    st.progress(analysis['skin_cleanliness_score'] / 10)
    
    st.markdown("**Quality Score**")
    st.progress(analysis['skin_quality_score'] / 10)
    
    # Detailed Description
    st.markdown("---")
    st.markdown("### 📝 Skin Condition Analysis")
    st.write(analysis['skin_condition_description'])
    
    # Concerns (if present)
    if 'concerns' in analysis and analysis['concerns']:
        st.markdown("---")
        st.markdown("### ⚠️ Identified Concerns")
        for concern in analysis['concerns']:
            st.markdown(f"- {concern}")
    
    # Quick Recommendations (if present)
    if 'recommendations' in analysis and analysis['recommendations']:
        st.markdown("---")
        st.markdown("### 💡 Quick Recommendations")
        for rec in analysis['recommendations']:
            st.markdown(f"- {rec}")
    
    # Action Buttons
    st.markdown("---")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("💬 Discuss with Chatbot", use_container_width=True):
            # Switch to chatbot page with context
            st.session_state.chat_context = analysis
            st.switch_page("pages/chatbot.py")  # Or handle navigation via app.py
    
    with btn_col2:
        if st.button("💄 Get Product Recommendations", use_container_width=True):
            # Switch to recommendations page
            st.switch_page("pages/recommendations.py")
    
    with btn_col3:
        if st.button("📊 View History", use_container_width=True):
            st.switch_page("pages/history.py")


def save_analysis(analysis: dict):
    """
    Save analysis to JSON file for history tracking.
    
    Args:
        analysis: Analysis dict to save
    """
    import os
    
    # Create user directory if doesn't exist
    user_id = st.session_state.get("user_id", "guest")
    user_dir = f"data/analyses/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    
    # Save analysis as JSON file
    filename = f"{user_dir}/{analysis['analysis_id']}.json"
    
    with open(filename, 'w') as f:
        json.dump(analysis, f, indent=2)
```

**Key Implementation Details:**

1. **Two-Column Layout**: Upload on left, results on right
2. **Async Analysis**: Shows spinner during API call (10-20 seconds)
3. **Robust Parsing**: Handles markdown code blocks in LLM response
4. **Data Validation**: Ensures scores are in [0, 10] range
5. **Persistence**: Saves to both session_state and JSON file
6. **Navigation**: Buttons to switch to related pages

**Expected LLM Response Format:**
```json
{
  "skin_cleanliness_score": 8,
  "skin_quality_score": 7,
  "age_estimate": 28,
  "skin_condition_description": "Your skin appears generally healthy with good moisture levels. There are minor signs of sun exposure...",
  "concerns": ["Mild hyperpigmentation", "Fine lines around eyes"],
  "recommendations": ["Use SPF 50+ daily", "Consider vitamin C serum"]
}
```

### 4. Chatbot Module

**File:** `modules/chatbot.py`

**Purpose:** Interactive conversational interface for skincare advice and follow-up questions.

**Detailed Implementation:**

```python
# modules/chatbot.py

import streamlit as st
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt
from datetime import datetime

def render():
    """
    Render the Chatbot page.
    Provides conversational interface for skincare questions.
    """
    
    st.title("💬 SkinCare AI Assistant")
    st.markdown("Ask me anything about skincare, your analysis results, or get personalized advice!")
    
    # Initialize chat history in session state if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(message["timestamp"])
    
    # Chat input at bottom
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Add user message to history
        user_message = {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.chat_history.append(user_message)
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
            st.caption(user_message["timestamp"])
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot_response = get_chatbot_response(user_input)
                st.markdown(bot_response)
                
                # Add bot message to history
                bot_message = {
                    "role": "assistant",
                    "content": bot_response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.chat_history.append(bot_message)
    
    # Sidebar options
    with st.sidebar:
        st.markdown("### 💬 Chat Options")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Quick Questions")
        
        quick_questions = [
            "What products should I use for my skin type?",
            "How can I improve my skin quality score?",
            "Explain my latest analysis results",
            "What causes skin aging?",
            "Best routine for oily skin?"
        ]
        
        for question in quick_questions:
            if st.button(question, use_container_width=True):
                # Simulate clicking the question
                st.session_state.pending_question = question
                st.rerun()
    
    # Handle quick question selection
    if 'pending_question' in st.session_state:
        # Process pending question
        # (This will be picked up by chat_input in next rerun)
        pass


def get_chatbot_response(user_input: str) -> str:
    """
    Get chatbot response from LLM.
    
    Args:
        user_input: User's question/message
    
    Returns:
        Bot's response text
    """
    
    # Build context from current analysis if available
    context = build_conversation_context()
    
    # Load system prompt
    system_prompt = load_prompt("chatbot_system")
    
    # Add context to system prompt
    if context:
        system_prompt += f"\n\nUser's Latest Analysis Context:\n{context}"
    
    # Build message history for LLM
    # Include recent chat history for context (last 5 messages)
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add recent chat history (last 10 messages to stay within token limits)
    recent_history = st.session_state.chat_history[-10:]
    for msg in recent_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Add current user input
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Call LLM
    result = llm_client.call_llm(
        messages=messages,
        temperature=0.7,  # Slightly more creative for conversation
        max_tokens=800
    )
    
    if result["success"]:
        return result["response"]
    else:
        return f"❌ Sorry, I encountered an error: {result['error']}\n\nPlease try again or check your API settings."


def build_conversation_context() -> str:
    """
    Build context string from user's latest analysis.
    
    Returns:
        Formatted context string for LLM
    """
    
    if not st.session_state.current_analysis:
        return ""
    
    analysis = st.session_state.current_analysis
    
    context = f"""
Latest Skin Analysis (performed on {analysis.get('timestamp', 'N/A')}):
- Skin Cleanliness Score: {analysis.get('skin_cleanliness_score', 'N/A')}/10
- Skin Quality Score: {analysis.get('skin_quality_score', 'N/A')}/10
- Estimated Age: {analysis.get('age_estimate', 'N/A')} years
- Condition: {analysis.get('skin_condition_description', 'N/A')}
"""
    
    if 'concerns' in analysis and analysis['concerns']:
        context += f"\nIdentified Concerns: {', '.join(analysis['concerns'])}"
    
    return context.strip()
```

**Key Implementation Details:**

1. **Chat History Persistence**: Uses `st.session_state.chat_history`
2. **Context-Aware**: Includes latest skin analysis in system prompt
3. **Recent Message Window**: Only sends last 10 messages to LLM to save tokens
4. **Quick Questions**: Sidebar with pre-defined common questions
5. **Real-time Display**: Messages appear immediately as they're sent
6. **Clear History**: Button to reset conversation

**Message Format in session_state:**
```python
{
    "role": "user" or "assistant",
    "content": "message text",
    "timestamp": "14:23:45"
}
```

### 5. Authentication Module

**File:** `modules/auth.py`

**Purpose:** LLM-simulated user authentication and profile management.

**Implementation Notes:**
- This is a **simulated** authentication system using LLM prompts
- No real password hashing or security
- Suitable for demo/prototype purposes only
- Uses session state to track "logged in" user

**Detailed Implementation:**

```python
# modules/auth.py

import streamlit as st
import json
import os
import uuid
from datetime import datetime
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt

def render():
    """
    Render the User Profile / Authentication page.
    """
    
    st.title("👤 User Profile")
    
    # Check if user is "logged in"
    if st.session_state.get("user_id"):
        display_profile()
    else:
        display_auth_forms()


def display_auth_forms():
    """
    Display login/registration forms.
    """
    
    st.markdown("### Welcome to SkinInsight")
    st.markdown("Create a profile to track your skin journey over time!")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_registration_form()


def render_login_form():
    """
    Render login form.
    """
    
    st.markdown("#### Login to Your Account")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submit:
            if authenticate_user(username, password):
                st.success(f"✅ Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")


def render_registration_form():
    """
    Render registration form.
    """
    
    st.markdown("#### Create New Account")
    
    with st.form("register_form"):
        username = st.text_input("Choose Username")
        age = st.number_input("Age", min_value=13, max_value=120, value=25)
        skin_type = st.selectbox(
            "Skin Type",
            ["Normal", "Dry", "Oily", "Combination", "Sensitive"]
        )
        concerns = st.multiselect(
            "Primary Concerns (optional)",
            ["Acne", "Aging", "Dark Spots", "Redness", "Dryness", "Oiliness", "Sensitivity"]
        )
        
        submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)
        
        if submit:
            if not username:
                st.error("❌ Please enter a username")
            elif user_exists(username):
                st.error("❌ Username already exists")
            else:
                create_user(username, age, skin_type, concerns)
                st.success(f"✅ Account created! Welcome, {username}!")
                st.rerun()


def display_profile():
    """
    Display user profile and settings.
    """
    
    user = load_user(st.session_state.user_id)
    
    st.markdown(f"### Welcome, {user['username']}! 👋")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Profile Information")
        
        st.markdown(f"**User ID:** `{user['user_id']}`")
        st.markdown(f"**Username:** {user['username']}")
        st.markdown(f"**Age:** {user['age']}")
        st.markdown(f"**Skin Type:** {user['skin_type']}")
        st.markdown(f"**Primary Concerns:** {', '.join(user.get('concerns', [])) or 'None'}")
        st.markdown(f"**Member Since:** {user['created_at']}")
        
        # Analysis Statistics
        st.markdown("---")
        st.markdown("#### 📊 Your Statistics")
        
        analyses_count = len(st.session_state.get('analyses', []))
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("Total Analyses", analyses_count)
        with stat_col2:
            st.metric("Chat Messages", len(st.session_state.get('chat_history', [])))
        with stat_col3:
            if analyses_count > 0:
                avg_quality = sum(a.get('skin_quality_score', 0) for a in st.session_state.analyses) / analyses_count
                st.metric("Avg Quality Score", f"{avg_quality:.1f}/10")
            else:
                st.metric("Avg Quality Score", "N/A")
    
    with col2:
        st.markdown("#### Actions")
        
        if st.button("📝 Edit Profile", use_container_width=True):
            st.session_state.editing_profile = True
            st.rerun()
        
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.session_state.get('confirm_clear'):
                clear_user_data()
                st.session_state.confirm_clear = False
                st.success("✅ All data cleared!")
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm deletion")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()
    
    # Edit profile form
    if st.session_state.get('editing_profile'):
        st.markdown("---")
        st.markdown("### Edit Profile")
        
        with st.form("edit_profile_form"):
            new_age = st.number_input("Age", min_value=13, max_value=120, value=user['age'])
            new_skin_type = st.selectbox(
                "Skin Type",
                ["Normal", "Dry", "Oily", "Combination", "Sensitive"],
                index=["Normal", "Dry", "Oily", "Combination", "Sensitive"].index(user['skin_type'])
            )
            new_concerns = st.multiselect(
                "Primary Concerns",
                ["Acne", "Aging", "Dark Spots", "Redness", "Dryness", "Oiliness", "Sensitivity"],
                default=user.get('concerns', [])
            )
            
            submit_col1, submit_col2 = st.columns(2)
            
            with submit_col1:
                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                    update_user(user['user_id'], new_age, new_skin_type, new_concerns)
                    st.session_state.editing_profile = False
                    st.success("✅ Profile updated!")
                    st.rerun()
            
            with submit_col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.editing_profile = False
                    st.rerun()


# Helper functions

def user_exists(username: str) -> bool:
    """Check if username already exists."""
    users_file = "data/users/users_index.json"
    
    if not os.path.exists(users_file):
        return False
    
    with open(users_file, 'r') as f:
        users_index = json.load(f)
    
    return username in users_index


def create_user(username: str, age: int, skin_type: str, concerns: list):
    """Create new user profile."""
    user_id = str(uuid.uuid4())
    
    user_data = {
        "user_id": user_id,
        "username": username,
        "age": age,
        "skin_type": skin_type,
        "concerns": concerns,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create user directory
    os.makedirs("data/users", exist_ok=True)
    
    # Save user profile
    with open(f"data/users/{user_id}.json", 'w') as f:
        json.dump(user_data, f, indent=2)
    
    # Update users index
    users_file = "data/users/users_index.json"
    
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users_index = json.load(f)
    else:
        users_index = {}
    
    users_index[username] = user_id
    
    with open(users_file, 'w') as f:
        json.dump(users_index, f, indent=2)
    
    # Set session state
    st.session_state.user_id = user_id
    st.session_state.username = username


def authenticate_user(username: str, password: str) -> bool:
    """
    Simulate authentication (NO REAL SECURITY - DEMO ONLY).
    For demo purposes, any username that exists can login.
    """
    users_file = "data/users/users_index.json"
    
    if not os.path.exists(users_file):
        return False
    
    with open(users_file, 'r') as f:
        users_index = json.load(f)
    
    if username in users_index:
        user_id = users_index[username]
        st.session_state.user_id = user_id
        st.session_state.username = username
        return True
    
    return False


def load_user(user_id: str) -> dict:
    """Load user profile from file."""
    with open(f"data/users/{user_id}.json", 'r') as f:
        return json.load(f)


def update_user(user_id: str, age: int, skin_type: str, concerns: list):
    """Update user profile."""
    user = load_user(user_id)
    user['age'] = age
    user['skin_type'] = skin_type
    user['concerns'] = concerns
    
    with open(f"data/users/{user_id}.json", 'w') as f:
        json.dump(user, f, indent=2)


def logout_user():
    """Clear user session."""
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.analyses = []
    st.session_state.chat_history = []
    st.session_state.current_analysis = None


def clear_user_data():
    """Clear user's analysis history."""
    st.session_state.analyses = []
    st.session_state.chat_history = []
    st.session_state.current_analysis = None
```

**Key Features:**
- Tab-based login/registration UI
- Profile editing capabilities
- User statistics display
- Session-based "authentication" (not secure, demo only)
- JSON file-based user storage
- Logout and data clearing

### 6. History Analytics Module

**File:** `modules/history.py`

**Purpose:** Visualize user's skin analysis history and track progress over time.

**Detailed Implementation:**

```python
# modules/history.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

def render():
    """
    Render the History Analytics page.
    """
    
    st.title("📊 Your Skin Journey")
    st.markdown("Track your skin quality progress over time")
    
    # Check if user has any analyses
    analyses = st.session_state.get('analyses', [])
    
    if not analyses:
        st.info("📭 No analysis history yet. Upload your first image on the Skin Analysis page!")
        
        if st.button("🔬 Go to Skin Analysis", type="primary"):
            # Navigate to analysis page
            pass
        
        return
    
    # Convert to DataFrame for easier manipulation
    df = create_analyses_dataframe(analyses)
    
    # Summary Cards
    st.markdown("### 📈 Overview")
    render_summary_cards(df)
    
    st.markdown("---")
    
    # Score Trends Chart
    st.markdown("### 📉 Score Trends Over Time")
    render_score_trends(df)
    
    st.markdown("---")
    
    # Analysis Timeline
    st.markdown("### 🕐 Analysis Timeline")
    render_timeline(analyses)
    
    st.markdown("---")
    
    # Detailed History Table
    st.markdown("### 📋 Detailed History")
    render_history_table(df)


def create_analyses_dataframe(analyses: list) -> pd.DataFrame:
    """
    Convert analyses list to pandas DataFrame.
    
    Args:
        analyses: List of analysis dicts
    
    Returns:
        DataFrame with analysis data
    """
    
    data = []
    
    for analysis in analyses:
        data.append({
            'timestamp': datetime.fromisoformat(analysis['timestamp']),
            'cleanliness_score': analysis['skin_cleanliness_score'],
            'quality_score': analysis['skin_quality_score'],
            'age_estimate': analysis['age_estimate'],
            'image_name': analysis.get('image_name', 'N/A'),
            'analysis_id': analysis['analysis_id']
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('timestamp')
    
    return df


def render_summary_cards(df: pd.DataFrame):
    """
    Render summary statistics cards.
    """
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Analyses",
            len(df),
            help="Total number of skin analyses performed"
        )
    
    with col2:
        latest_quality = df.iloc[-1]['quality_score']
        if len(df) > 1:
            previous_quality = df.iloc[-2]['quality_score']
            delta = latest_quality - previous_quality
        else:
            delta = None
        
        st.metric(
            "Latest Quality Score",
            f"{latest_quality}/10",
            delta=f"{delta:+.1f}" if delta is not None else None,
            help="Your most recent skin quality score"
        )
    
    with col3:
        avg_quality = df['quality_score'].mean()
        st.metric(
            "Average Quality",
            f"{avg_quality:.1f}/10",
            help="Average of all quality scores"
        )
    
    with col4:
        avg_cleanliness = df['cleanliness_score'].mean()
        st.metric(
            "Average Cleanliness",
            f"{avg_cleanliness:.1f}/10",
            help="Average of all cleanliness scores"
        )


def render_score_trends(df: pd.DataFrame):
    """
    Render line chart showing score trends.
    """
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add Cleanliness Score trace
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['cleanliness_score'],
        mode='lines+markers',
        name='Cleanliness Score',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=8)
    ))
    
    # Add Quality Score trace
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['quality_score'],
        mode='lines+markers',
        name='Quality Score',
        line=dict(color='#2196F3', width=3),
        marker=dict(size=8)
    ))
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Score (0-10)",
        yaxis=dict(range=[0, 10]),
        hovermode='x unified',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_timeline(analyses: list):
    """
    Render timeline of analyses with expandable details.
    """
    
    # Sort by timestamp (newest first)
    sorted_analyses = sorted(
        analyses,
        key=lambda x: x['timestamp'],
        reverse=True
    )
    
    for i, analysis in enumerate(sorted_analyses):
        timestamp = datetime.fromisoformat(analysis['timestamp'])
        date_str = timestamp.strftime("%B %d, %Y at %H:%M")
        
        with st.expander(f"📅 {date_str} - Quality: {analysis['skin_quality_score']}/10"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Cleanliness Score**")
                st.progress(analysis['skin_cleanliness_score'] / 10)
                st.markdown(f"{analysis['skin_cleanliness_score']}/10")
            
            with col2:
                st.markdown("**Quality Score**")
                st.progress(analysis['skin_quality_score'] / 10)
                st.markdown(f"{analysis['skin_quality_score']}/10")
            
            with col3:
                st.markdown("**Age Estimate**")
                st.markdown(f"### {analysis['age_estimate']} years")
            
            st.markdown("---")
            st.markdown("**Condition Description:**")
            st.write(analysis['skin_condition_description'])
            
            if 'concerns' in analysis and analysis['concerns']:
                st.markdown("**Concerns:**")
                for concern in analysis['concerns']:
                    st.markdown(f"- {concern}")
            
            # Action buttons
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                if st.button("💬 Discuss This Analysis", key=f"discuss_{i}"):
                    # Load this analysis as context and go to chatbot
                    st.session_state.current_analysis = analysis
                    pass
            
            with btn_col2:
                if st.button("💄 Get Recommendations", key=f"recommend_{i}"):
                    # Load this analysis and go to recommendations
                    st.session_state.current_analysis = analysis
                    pass


def render_history_table(df: pd.DataFrame):
    """
    Render detailed history as a table.
    """
    
    # Format DataFrame for display
    display_df = df.copy()
    display_df['Date'] = display_df['timestamp'].dt.strftime("%Y-%m-%d %H:%M")
    display_df = display_df[[
        'Date',
        'cleanliness_score',
        'quality_score',
        'age_estimate',
        'image_name'
    ]]
    display_df.columns = [
        'Date',
        'Cleanliness',
        'Quality',
        'Age',
        'Image'
    ]
    
    # Display table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Export button
    if st.button("📥 Export History as CSV"):
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"skin_analysis_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
```

**Key Features:**
- Summary statistics cards with delta indicators
- Interactive Plotly charts for trend visualization
- Timeline view with expandable analysis details
- Data table with export to CSV functionality
- Direct navigation to related features (chatbot, recommendations)

### 7. Recommendations Module

**File:** `modules/recommendations.py`

**Purpose:** LLM-generated personalized product recommendations based on skin analysis.

**Detailed Implementation:**

```python
# modules/recommendations.py

import streamlit as st
import json
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt

def render():
    """
    Render the Product Recommendations page.
    """
    
    st.title("💄 Personalized Skincare Recommendations")
    st.markdown("AI-powered product suggestions tailored to your skin condition")
    
    # Check if there's an analysis to base recommendations on
    if not st.session_state.current_analysis:
        st.warning("⚠️ No analysis found. Please complete a skin analysis first!")
        
        if st.button("🔬 Go to Skin Analysis", type="primary"):
            # Navigate to analysis page
            pass
        
        return
    
    # Display current analysis summary
    render_analysis_summary()
    
    st.markdown("---")
    
    # Generate recommendations button
    if 'recommendations' not in st.session_state or st.session_state.recommendations is None:
        if st.button("✨ Generate Recommendations", type="primary", use_container_width=True):
            generate_recommendations()
            st.rerun()
    else:
        # Display existing recommendations
        display_recommendations()
        
        st.markdown("---")
        
        if st.button("🔄 Regenerate Recommendations", use_container_width=True):
            generate_recommendations()
            st.rerun()


def render_analysis_summary():
    """
    Display brief summary of current analysis.
    """
    
    analysis = st.session_state.current_analysis
    
    st.markdown("### 📊 Based on Your Latest Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Cleanliness Score", f"{analysis['skin_cleanliness_score']}/10")
    
    with col2:
        st.metric("Quality Score", f"{analysis['skin_quality_score']}/10")
    
    with col3:
        st.metric("Age Estimate", f"{analysis['age_estimate']} years")
    
    if 'concerns' in analysis and analysis['concerns']:
        st.markdown(f"**Identified Concerns:** {', '.join(analysis['concerns'])}")


def generate_recommendations():
    """
    Generate product recommendations using LLM.
    """
    
    with st.spinner("✨ Generating personalized recommendations..."):
        
        # Build prompt with analysis data
        analysis = st.session_state.current_analysis
        
        system_prompt = load_prompt("recommendation_system")
        user_prompt = build_recommendation_prompt(analysis)
        
        # Call LLM
        result = llm_client.call_llm(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        if result["success"]:
            try:
                # Parse recommendations
                recommendations = parse_recommendations_response(result["response"])
                st.session_state.recommendations = recommendations
                st.success("✅ Recommendations generated!")
            
            except Exception as e:
                st.error(f"❌ Failed to parse recommendations: {str(e)}")
                st.error("Raw response:")
                st.code(result["response"])
        
        else:
            st.error(f"❌ Failed to generate recommendations: {result['error']}")


def build_recommendation_prompt(analysis: dict) -> str:
    """
    Build prompt for recommendation generation.
    
    Args:
        analysis: Current analysis dict
    
    Returns:
        Formatted prompt string
    """
    
    prompt = f"""
Please generate personalized skincare product recommendations based on the following skin analysis:

Skin Cleanliness Score: {analysis['skin_cleanliness_score']}/10
Skin Quality Score: {analysis['skin_quality_score']}/10
Age Estimate: {analysis['age_estimate']} years
Condition: {analysis['skin_condition_description']}
"""
    
    if 'concerns' in analysis and analysis['concerns']:
        prompt += f"\nIdentified Concerns: {', '.join(analysis['concerns'])}"
    
    prompt += """

Generate recommendations in the following JSON format:
{
    "overall_routine": "Brief description of recommended routine",
    "products": [
        {
            "category": "Cleanser/Moisturizer/Serum/Treatment/Sunscreen",
            "recommendation": "Product name or type",
            "why": "Reason for this recommendation",
            "key_ingredients": ["ingredient1", "ingredient2"],
            "usage": "How and when to use"
        }
    ],
    "tips": ["tip1", "tip2", "tip3"]
}
"""
    
    return prompt


def parse_recommendations_response(response_text: str) -> dict:
    """
    Parse LLM response into structured recommendations.
    
    Args:
        response_text: Raw LLM response
    
    Returns:
        Parsed recommendations dict
    """
    
    # Clean response
    response_text = response_text.strip()
    
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "", 1)
    if response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)
    if response_text.endswith("```"):
        response_text = response_text.rsplit("```", 1)[0]
    
    # Parse JSON
    data = json.loads(response_text.strip())
    
    return data


def display_recommendations():
    """
    Display generated recommendations in UI.
    """
    
    recommendations = st.session_state.recommendations
    
    # Overall Routine
    st.markdown("### 🌟 Recommended Routine")
    st.info(recommendations.get('overall_routine', 'No routine description available'))
    
    st.markdown("---")
    
    # Product Recommendations
    st.markdown("### 🧴 Product Recommendations")
    
    products = recommendations.get('products', [])
    
    for i, product in enumerate(products):
        with st.container():
            st.markdown(f"#### {i+1}. {product['category']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Recommendation:** {product['recommendation']}")
                st.markdown(f"**Why:** {product['why']}")
                st.markdown(f"**Usage:** {product['usage']}")
            
            with col2:
                st.markdown("**Key Ingredients:**")
                for ingredient in product.get('key_ingredients', []):
                    st.markdown(f"- {ingredient}")
            
            st.markdown("---")
    
    # Additional Tips
    if 'tips' in recommendations and recommendations['tips']:
        st.markdown("### 💡 Additional Tips")
        
        for tip in recommendations['tips']:
            st.markdown(f"- {tip}")


```

**Expected LLM Response Format:**
```json
{
  "overall_routine": "A balanced routine focusing on hydration and sun protection...",
  "products": [
    {
      "category": "Cleanser",
      "recommendation": "Gentle, pH-balanced cleanser",
      "why": "Your skin needs gentle cleansing without stripping natural oils",
      "key_ingredients": ["Glycerin", "Hyaluronic Acid"],
      "usage": "Use twice daily, morning and evening"
    },
    {
      "category": "Serum",
      "recommendation": "Vitamin C serum",
      "why": "Helps with hyperpigmentation and brightening",
      "key_ingredients": ["L-Ascorbic Acid", "Vitamin E"],
      "usage": "Apply in the morning before sunscreen"
    }
  ],
  "tips": [
    "Always apply sunscreen as the last step in your morning routine",
    "Introduce new products one at a time",
    "Stay hydrated by drinking at least 8 glasses of water daily"
  ]
}
```

### 8. Prompt Templates

**Directory:** `prompts/`

All prompts are stored as text files and loaded dynamically. This allows easy editing without changing code.

**File:** `prompts/prompt_utils.py`

```python
# prompts/prompt_utils.py

import os

PROMPTS_DIR = os.path.dirname(__file__)

def load_prompt(prompt_name: str) -> str:
    """
    Load prompt template from file.
    
    Args:
        prompt_name: Name of prompt file (without .txt extension)
    
    Returns:
        Prompt text content
    """
    
    prompt_file = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")
    
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read().strip()


def save_prompt(prompt_name: str, content: str):
    """
    Save prompt template to file.
    
    Args:
        prompt_name: Name of prompt file (without .txt extension)
        content: Prompt text content
    """
    
    prompt_file = os.path.join(PROMPTS_DIR, f"{prompt_name}.txt")
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(content)
```

**File:** `prompts/skin_analysis_system.txt`

```
You are an expert dermatologist and skincare analyst with over 20 years of experience. Your role is to analyze facial images and provide comprehensive, professional skin quality assessments.

When analyzing an image, you must:
1. Carefully examine the overall skin condition
2. Evaluate skin cleanliness (pore clarity, makeup/dirt presence, overall surface cleanness)
3. Evaluate skin quality (texture, tone evenness, visible concerns, hydration, signs of aging)
4. Estimate the person's age based on skin condition and facial features
5. Identify specific skin concerns if present
6. Provide brief, actionable recommendations

CRITICAL: You MUST respond in valid JSON format with NO additional text before or after. Use this exact structure:

{
    "skin_cleanliness_score": <integer 0-10>,
    "skin_quality_score": <integer 0-10>,
    "age_estimate": <integer>,
    "skin_condition_description": "<detailed 2-3 sentence description>",
    "concerns": ["<concern1>", "<concern2>"],
    "recommendations": ["<brief rec1>", "<brief rec2>"]
}

Scoring Guidelines:
- Cleanliness (0-10): 0-3 = Poor (visible dirt/makeup), 4-6 = Moderate (some impurities), 7-8 = Good (mostly clean), 9-10 = Excellent (very clean)
- Quality (0-10): 0-3 = Poor (many concerns), 4-6 = Fair (moderate concerns), 7-8 = Good (minor concerns), 9-10 = Excellent (minimal concerns)

Be professional, empathetic, and constructive in your assessment.
```

**File:** `prompts/skin_analysis_user.txt`

```
Please analyze this facial image and provide a comprehensive skin quality assessment. Focus on:

1. Overall skin cleanliness (pore clarity, presence of makeup or dirt, surface cleanliness)
2. Skin quality (texture, tone, hydration, any visible concerns)
3. Age estimation based on skin condition and facial features
4. Specific concerns if present (acne, wrinkles, dark spots, redness, etc.)
5. Brief recommendations for improvement

Remember to respond ONLY with valid JSON in the specified format. Do not include any explanatory text before or after the JSON.
```

**File:** `prompts/chatbot_system.txt`

```
You are SkinCare AI Assistant, a knowledgeable and friendly skincare expert. Your role is to provide helpful, accurate, and personalized skincare advice based on the user's questions and their skin analysis results.

Personality:
- Warm and conversational, like a knowledgeable friend
- Professional but not overly technical
- Encouraging and supportive about skin health journey
- Clear and concise in explanations

Guidelines:
1. If the user has recent analysis results, reference them naturally in your responses
2. Provide evidence-based skincare advice
3. Recommend consulting a dermatologist for serious concerns
4. Be honest about what can and cannot be achieved with skincare
5. Keep responses focused and actionable (2-4 paragraphs usually sufficient)
6. If asked about products, provide general categories and ingredients rather than specific brand names
7. Explain skincare concepts in simple terms

DO NOT:
- Diagnose medical conditions
- Recommend prescription medications
- Make unrealistic promises about results
- Promote specific commercial brands
- Provide advice that contradicts general dermatological consensus

Always prioritize the user's skin health and safety.
```

**File:** `prompts/recommendation_system.txt`

```
You are a skincare product recommendation specialist. Your role is to suggest appropriate skincare products and routines based on the user's skin analysis results.

When generating recommendations:
1. Consider the user's skin scores, concerns, and age
2. Recommend a complete routine (cleanser, treatment products, moisturizer, sunscreen)
3. Explain WHY each product is recommended
4. List key ingredients that would be beneficial
5. Provide usage instructions

Focus on:
- Product categories and types rather than specific brands
- Evidence-based ingredients
- Appropriate order of application
- Realistic expectations

CRITICAL: Respond ONLY with valid JSON in this exact format:

{
    "overall_routine": "<brief routine description>",
    "products": [
        {
            "category": "<Cleanser/Moisturizer/Serum/Treatment/Sunscreen/etc>",
            "recommendation": "<general product type or description>",
            "why": "<reason this is recommended>",
            "key_ingredients": ["<ingredient1>", "<ingredient2>"],
            "usage": "<how and when to use>"
        }
    ],
    "tips": ["<tip1>", "<tip2>", "<tip3>"]
}

Include 4-6 product recommendations covering a complete routine.
Keep explanations clear and actionable.
```

## Data Flow

### Skin Analysis Flow

```
User uploads image
       ↓
Image bytes extracted
       ↓
Prompt templates loaded (skin_analysis_system.txt + skin_analysis_user.txt)
       ↓
API Client encodes image to base64
       ↓
Request sent to GPT-6-Luna API
       {
         "model": "gpt-6-luna",
         "messages": [
           {"role": "system", "content": "You are an expert..."},
           {"role": "user", "content": [
             {"type": "text", "text": "Please analyze..."},
             {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
           ]}
         ]
       }
       ↓
LLM processes image and returns JSON response
       ↓
Response parsed and validated
       ↓
Analysis data stored in:
   - st.session_state.current_analysis (for current session)
   - st.session_state.analyses (append to list)
   - data/analyses/{user_id}/{analysis_id}.json (persistent storage)
       ↓
UI displays results with metrics, progress bars, and description
       ↓
User can navigate to chatbot, recommendations, or history
```

### Chatbot Interaction Flow

```
User enters message in chat input
       ↓
Message added to st.session_state.chat_history
       ↓
Build context from latest analysis (if available)
       ↓
Load chatbot_system.txt prompt
       ↓
Append analysis context to system prompt
       ↓
Build messages array:
   - System prompt with context
   - Last 10 messages from chat_history
   - Current user message
       ↓
Send to LLM API
       ↓
Response received and displayed
       ↓
Bot response added to chat_history
       ↓
UI updates to show conversation
```

### User History Flow

```
User navigates to History page
       ↓
Load st.session_state.analyses (list of all analyses)
       ↓
Convert to pandas DataFrame for easier manipulation
       ↓
Calculate statistics:
   - Total count
   - Latest score vs previous (delta)
   - Average scores
       ↓
Generate Plotly charts:
   - Line chart with cleanliness and quality trends
   - X-axis: timestamps, Y-axis: scores (0-10)
       ↓
Render timeline with expandable cards (newest first)
       ↓
Render data table with export option
       ↓
User can click to discuss specific analysis or get recommendations
```

## Data Storage Strategy

### Session State Structure

```python
st.session_state = {
    # Initialization flag
    'initialized': True,
    
    # User authentication (simulated)
    'user_id': '550e8400-e29b-41d4-a716-446655440000',  # UUID
    'username': 'john_doe',
    
    # Analysis data
    'current_analysis': {
        'analysis_id': '...',
        'timestamp': '2026-11-03T14:23:45',
        'skin_cleanliness_score': 8,
        'skin_quality_score': 7,
        'age_estimate': 28,
        'skin_condition_description': '...',
        'concerns': ['...'],
        'recommendations': ['...'],
        'image_name': 'selfie.jpg'
    },
    
    # All analyses (list)
    'analyses': [
        {...},  # analysis 1
        {...},  # analysis 2
    ],
    
    # Chat history
    'chat_history': [
        {
            'role': 'user',
            'content': 'What products should I use?',
            'timestamp': '14:23:45'
        },
        {
            'role': 'assistant',
            'content': 'Based on your analysis...',
            'timestamp': '14:23:50'
        }
    ],
    
    # Recommendations
    'recommendations': {
        'overall_routine': '...',
        'products': [...],
        'tips': [...]
    },
    
    # UI state flags
    'editing_profile': False,
    'confirm_clear': False,
    'pending_question': None
}
```

### JSON File Structure

**User Profile:** `data/users/{user_id}.json`
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john_doe",
  "age": 28,
  "skin_type": "Combination",
  "concerns": ["Acne", "Dark Spots"],
  "created_at": "2026-11-01 10:30:00"
}
```

**User Index:** `data/users/users_index.json`
```json
{
  "john_doe": "550e8400-e29b-41d4-a716-446655440000",
  "jane_smith": "660e8400-e29b-41d4-a716-446655440001"
}
```

**Analysis Record:** `data/analyses/{user_id}/{analysis_id}.json`
```json
{
  "analysis_id": "abc123...",
  "timestamp": "2026-11-03T14:23:45",
  "image_name": "selfie.jpg",
  "skin_cleanliness_score": 8,
  "skin_quality_score": 7,
  "age_estimate": 28,
  "skin_condition_description": "Your skin appears generally healthy...",
  "concerns": ["Mild hyperpigmentation", "Fine lines"],
  "recommendations": ["Use SPF 50+ daily", "Consider vitamin C serum"]
}
```

## UI/UX Architecture

### Page Layout Structure

All pages follow consistent layout:

```
┌─────────────────────────────────────────────────────────┐
│  [Sidebar - Fixed Left]        [Main Content Area]     │
│                                                         │
│  🔬 SkinInsight                 Page Title              │
│  ───────────────                ════════════            │
│                                                         │
│  Navigation:                    [Content specific       │
│  ○ 🏠 Skin Analysis              to selected page]     │
│  ○ 💬 Chatbot                                          │
│  ○ 👤 My Profile                                       │
│  ○ 📊 History                                          │
│  ○ 💄 Recommendations                                  │
│                                                         │
│  ───────────────                                       │
│                                                         │
│  ⚙️ API Settings                                        │
│  (collapsible)                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Navigation Pattern

**Sidebar-Based Navigation:**
- Fixed sidebar always visible
- Radio buttons for page selection
- Selection stored in local variable (not session_state)
- Page content rendered based on selection
- No page reloads, smooth transitions

**Implementation:**
```python
# In app.py
with st.sidebar:
    page = st.radio("Navigation", [
        "🏠 Skin Analysis",
        "💬 Chatbot",
        "👤 My Profile",
        "📊 History",
        "💄 Recommendations"
    ])

# Route to module
if page == "🏠 Skin Analysis":
    skin_analysis.render()
elif page == "💬 Chatbot":
    chatbot.render()
# ... etc
```

### Component Hierarchy

**Streamlit Component Usage:**

1. **Containers** (`st.container()`):
   - Group related content
   - Apply consistent styling
   - Maintain visual hierarchy

2. **Columns** (`st.columns()`):
   - Side-by-side layouts
   - Metric cards
   - Form fields
   - Action buttons

3. **Expanders** (`st.expander()`):
   - Collapsible sections
   - Detailed information
   - Settings panels
   - Timeline entries

4. **Forms** (`st.form()`):
   - Login/registration
   - Profile editing
   - Batch input submission

5. **Tabs** (`st.tabs()`):
   - Related content sections
   - Login vs Register
   - Different view modes

**Consistent Styling:**
- Use emojis for visual indicators
- Consistent color scheme via Streamlit theme
- Progress bars for scores (0-1 scale)
- Metrics for KPIs with deltas
- Info/warning/error/success callouts

## Prompt Engineering Architecture

### Prompt Structure Standards

All prompts follow this structure:

```
[ROLE DEFINITION]
You are a [expert/specialist] in [domain]...

[PERSONALITY/TONE] (for conversational interfaces)
- Trait 1
- Trait 2

[TASK DESCRIPTION]
Your task is to...

[SPECIFIC INSTRUCTIONS]
1. Instruction 1
2. Instruction 2

[OUTPUT FORMAT]
CRITICAL: You MUST respond in [format]...

[FORMAT TEMPLATE]
{
    "field": "value"
}

[GUIDELINES/CONSTRAINTS]
- Guideline 1
- Guideline 2

[WHAT NOT TO DO]
DO NOT:
- Don't 1
- Don't 2
```

### Response Format Enforcement

**JSON Response Handling:**

1. **In System Prompt:**
   - Explicitly state "CRITICAL: You MUST respond in valid JSON"
   - Provide exact JSON template
   - Show example with field types

2. **In Parsing Code:**
   - Strip markdown code blocks (```json)
   - Trim whitespace
   - Use try/except for JSON parsing
   - Validate required fields
   - Provide fallback values if possible

3. **Error Handling:**
   - Display raw response if parsing fails
   - Allow user to retry
   - Log errors for debugging

**Example:**
```python
def parse_json_response(response_text: str) -> dict:
    # Clean response
    text = response_text.strip()
    
    # Remove markdown
    if text.startswith("```json"):
        text = text.replace("```json", "", 1)
    if text.startswith("```"):
        text = text.replace("```", "", 1)
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    
    # Parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}\n\nRaw response:\n{response_text}")
```

## Error Handling Strategy

### API Error Handling

```python
# In api_client.py

# HTTP Status Codes:
# 200: Success → Return response
# 401: Unauthorized → Show "Invalid API key" message
# 429: Rate Limit → Retry with exponential backoff (1s, 2s, 4s)
# 500-599: Server Error → Show generic error message
# Timeout: Retry up to 3 times

# Return format always includes:
{
    "success": bool,
    "response": str or None,
    "error": str or None,
    "tokens_used": int
}
```

### UI Error Handling

```python
# In module functions:

try:
    # Call LLM
    result = llm_client.call_llm(...)
    
    if result["success"]:
        # Parse and display
        data = parse_response(result["response"])
        # ... display logic
    else:
        # Show error to user
        st.error(f"❌ Error: {result['error']}")

except Exception as e:
    # Catch unexpected errors
    st.error(f"❌ Unexpected error: {str(e)}")
    # Optionally show debug info
    with st.expander("Debug Info"):
        st.code(traceback.format_exc())
```

### Graceful Degradation

- If API call fails: Show error but allow retry
- If parsing fails: Show raw response for debugging
- If data missing: Use fallback values ("N/A", 0, empty list)
- If image too large: Show size limit message
- If no internet: Show connection error with troubleshooting tips

## Security Considerations

### ⚠️ Important Disclaimers

**This is a PROTOTYPE for educational purposes:**

1. **Authentication is NOT secure:**
   - No password hashing
   - No session tokens
   - Usernames stored in plain JSON
   - Only suitable for demo/development

2. **API Key Handling:**
   - Stored in plaintext (config or .env)
   - Not suitable for production
   - Users should use test API keys only

3. **Data Privacy:**
   - Images sent to external API
   - No encryption at rest
   - Local file storage only
   - Not HIPAA/GDPR compliant

### Production Recommendations

If deploying for real use:
- Implement proper authentication (OAuth, JWT)
- Use password hashing (bcrypt)
- Encrypt API keys (environment variables + secrets management)
- Use HTTPS for all communications
- Implement rate limiting per user
- Add input validation and sanitization
- Use secure database (PostgreSQL with SSL)
- Implement audit logging
- Add CSRF protection
- Comply with data protection regulations

## Performance Optimization

### Caching Strategy

```python
# Use Streamlit's caching for expensive operations

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_user_analyses(user_id: str):
    """Load all analyses for a user."""
    # Load from files
    return analyses

@st.cache_resource
def get_llm_client():
    """Create singleton LLM client."""
    return LLMClient()
```

### Token Usage Optimization

1. **Prompt Engineering:**
   - Use concise system prompts
   - Avoid unnecessary verbosity
   - Request structured outputs (JSON reduces tokens vs prose)

2. **Chat History Limits:**
   - Keep only last 10 messages in context
   - Summarize very long conversations

3. **Image Encoding:**
   - Compress images before encoding (max 1024x1024)
   - Use JPEG with quality=85

4. **Response Limits:**
   - Set appropriate max_tokens (1500 usually sufficient)
   - Lower temperature for deterministic tasks (0.3)

### UI Performance

1. **Lazy Loading:**
   - Don't load all history at once
   - Paginate or virtualize long lists

2. **Minimize Reruns:**
   - Use forms for batch input
   - Careful with st.rerun()
   - Cache expensive computations

3. **Async Operations:**
   - Show spinners during API calls
   - Disable buttons during processing

## Scalability & Future Enhancements

### Current Limitations

1. **Single User:**
   - No concurrent user support
   - File-based storage
   - No access control

2. **Local Storage:**
   - Limited to disk space
   - No backup strategy
   - Not cloud-scalable

3. **Simple History:**
   - Linear list of analyses
   - No search/filter
   - No comparison tools

### Future Enhancement Ideas

**Phase 2 (Database Migration):**
- Replace JSON files with SQLite/PostgreSQL
- Add proper relational schema
- Implement query optimization

**Phase 3 (Multi-User):**
- Real authentication system
- User roles (admin, user)
- Data isolation per user
- Concurrent access handling

**Phase 4 (Advanced Features):**
- Compare two analyses side-by-side
- Progress photos with before/after
- Export reports as PDF
- Email notifications
- Mobile app (React Native + API)
- Integration with eCommerce (Shopify, WooCommerce)
- Appointment booking with dermatologists
- Community features (forums, tips sharing)

**Phase 5 (AI Enhancements):**
- Fine-tune custom model for better accuracy
- Multi-modal analysis (video, 3D scanning)
- Predictive analytics (future skin condition)
- Personalized routine optimization over time

---

**Last Updated:** 2026-11-03  
**Version:** 1.0  
**Author:** SkinInsight Development Team
