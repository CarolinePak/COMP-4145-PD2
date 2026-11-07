# modules/chatbot.py

import streamlit as st
from modules.api_client import llm_client
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
        # Show welcome message if no history
        if not st.session_state.chat_history:
            with st.chat_message("assistant"):
                st.markdown("👋 Hello! I'm your AI skincare assistant. How can I help you today?")

                # Show analysis summary if available
                if st.session_state.current_analysis:
                    analysis = st.session_state.current_analysis
                    st.info(f"I see you recently completed a skin analysis:\n\n"
                           f"- **Quality Score:** {analysis['skin_quality_score']}/10\n"
                           f"- **Cleanliness Score:** {analysis['skin_cleanliness_score']}/10\n"
                           f"- **Age Estimate:** {analysis['age_estimate']} years\n\n"
                           f"Feel free to ask me about your results!")

        # Display message history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(message["timestamp"])

    # Suggested prompts close to the input, like conversation starters.
    st.caption("Not sure what to ask? Try one of these:")
    suggestion_columns = st.columns(2)
    for index, question in enumerate(SUGGESTED_QUESTIONS):
        suggestion_columns[index % 2].button(
            question,
            key=f"suggested_question_{index}",
            use_container_width=True,
            on_click=_queue_suggested_question,
            args=(question,),
        )

    suggested_input = st.session_state.pop("suggested_question", None)
    if suggested_input:
        handle_user_message(suggested_input)
        st.rerun()

    # Chat input at bottom
    user_input = st.chat_input("Type your question here...")

    if user_input:
        handle_user_message(user_input)

    # Sidebar quick actions
    with st.sidebar:
        st.markdown("### 💬 Chat Options")

        # Clear history button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        # Message count
        msg_count = len(st.session_state.chat_history)
        st.caption(f"Messages in history: {msg_count}")



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

    # Display user message
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
            st.caption(bot_message["timestamp"])


def get_chatbot_response(user_input: str) -> str:
    """
    Get chatbot response from LLM.

    Args:
        user_input: User's question/message

    Returns:
        Bot's response text
    """

    from config import config

    # Check API key
    if not config.API_KEY:
        return "❌ API key not configured. Please add your API key in the sidebar settings."

    # Build context
    context = build_conversation_context()

    # Load system prompt
    try:
        system_prompt = load_prompt("chatbot_system")
    except FileNotFoundError:
        return "❌ Chatbot system prompt not found. Please ensure all prompt files are present."

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

    # Add current user input
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Call LLM
    result = llm_client.call_llm(
        messages=messages,
        temperature=0.7,  # More creative for conversation
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
