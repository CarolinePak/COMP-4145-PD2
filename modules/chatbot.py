# modules/chatbot.py

import streamlit as st
from modules import ui
from modules.api_client import client_for_session
from prompts.prompt_utils import load_prompt
from datetime import datetime


SUGGESTED_QUESTIONS = [
    "Explain my latest analysis results",
    "How can I improve my skin quality score?",
    "What skincare routine suits my concerns?",
    "What ingredients should I look for?",
    "How often should I repeat a skin analysis?",
]

def render():
    ui.heading("Skincare Chatbot", "Ask about your results, skincare ingredients, or your daily routine.", "chat")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with ui.panel("chat-layout"):
        with ui.panel("card conversation"):
            title_col, action_col = st.columns([5, 1])
            with title_col:
                st.header("Conversation")
            with action_col:
                if st.session_state.chat_history:
                    st.button(
                        "Clear",
                        key="clear_chat",
                        use_container_width=True,
                        on_click=_clear_conversation,
                    )

            with st.container(height=430, border=False):
                if not st.session_state.chat_history:
                    st.caption("Ask a question below to start the conversation.")

                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                        if message.get("timestamp"):
                            st.caption(message["timestamp"])

            if not st.session_state.chat_history:
                with ui.panel("chat-suggestions"):
                    st.caption("Try asking one of these questions:")
                    suggestion_columns = st.columns(2)
                    for index, question in enumerate(SUGGESTED_QUESTIONS):
                        suggestion_columns[index % 2].button(
                            question,
                            key=f"suggested_question_{index}",
                            use_container_width=True,
                            on_click=_queue_suggested_question,
                            args=(question,),
                        )

            user_input = st.chat_input("Ask a skincare question")
            question = st.session_state.pop("suggested_question", None) or user_input
            if question:
                handle_user_message(question)
                st.rerun()


def _clear_conversation():
    st.session_state.chat_history = []


def _queue_suggested_question(question: str):
    """Queue a conversation starter to be sent on the next rerun."""
    st.session_state.suggested_question = question


def handle_user_message(user_input: str):
    """
    Handle user's chat message.

    Args:
        user_input: User's message text
    """

    # Add user message to history
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.chat_history.append(user_message)

    # Get the response, then let the next rerun render both messages inside the
    # fixed-height transcript rather than extending the page.
    with st.spinner("Thinking..."):
        bot_response = get_chatbot_response(user_input)

    bot_message = {
        "role": "assistant",
        "content": bot_response,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.chat_history.append(bot_message)


def get_chatbot_response(user_input: str) -> str:
    """
    Get chatbot response from LLM.

    Args:
        user_input: User's question/message

    Returns:
        Bot's response text
    """

    client = client_for_session()
    if not client.api_key:
        return "API key not configured. Add your API key in Settings to continue."

    # Build context
    context = build_conversation_context()

    # Load system prompt
    try:
        system_prompt = load_prompt("chatbot_system")
    except FileNotFoundError:
        return "The chatbot prompt could not be found. Please check that the prompt files are present."

    # Add context to system prompt
    if context:
        system_prompt += f"\n\n{context}"

    # Build messages array
    messages = [{"role": "system", "content": system_prompt}]

    # Add recent chat history (last 10 messages to stay within token limits)
    recent_history = st.session_state.chat_history[-10:] if len(st.session_state.chat_history) > 10 else st.session_state.chat_history

    for msg in recent_history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Call LLM
    result = client.call_llm(
        messages=messages,
        temperature=0.7,  # More creative for conversation
        max_tokens=800
    )

    if result["success"]:
        return result["response"]
    else:
        return f"I couldn't complete that response: {result['error']}\n\nPlease try again or check your API settings."


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
=== USER'S LATEST SKIN ANALYSIS ===
(Use this information to provide personalized advice)

Analysis Date: {analysis.get('timestamp', 'N/A')}
Skin Cleanliness Score: {analysis.get('skin_cleanliness_score', 'N/A')}/10
Skin Quality Score: {analysis.get('skin_quality_score', 'N/A')}/10
Estimated Age: {analysis.get('age_estimate', 'N/A')} years
Condition: {analysis.get('skin_condition_description', 'N/A')}
"""

    if analysis.get('concerns'):
        context += f"\nIdentified Concerns: {', '.join(analysis['concerns'])}"

    context += "\n" + "=" * 40

    return context.strip()
