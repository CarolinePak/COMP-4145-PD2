# modules/chatbot.py

import streamlit as st
from modules.api_client import llm_client
from prompts.prompt_utils import load_prompt
from datetime import datetime


FAQ_ITEMS = [
    (
        "How accurate is the skin analysis?",
        "It is an AI estimate based on visible features in one photo. Lighting, "
        "camera quality, makeup, and facial angle can affect the result, so it "
        "should not be treated as a clinical measurement.",
    ),
    (
        "Is my photo stored?",
        "The application sends the selected photo to the configured AI service "
        "for analysis, but it does not save the original photo locally. Only the "
        "text-based analysis result is stored for history.",
    ),
    (
        "What do the scores mean?",
        "Cleanliness and quality are AI-estimated scores from 0 to 10. They are "
        "designed for general comparison within this demo and are not medical "
        "health scores.",
    ),
    (
        "How often should I repeat an analysis?",
        "For a more useful comparison, try once a week under similar lighting, "
        "camera distance, angle, and skincare conditions.",
    ),
    (
        "Can SkinInsight diagnose a skin condition?",
        "No. SkinInsight provides general skincare information and cannot diagnose "
        "or treat medical conditions. Seek a qualified healthcare professional for "
        "persistent, painful, severe, or rapidly changing symptoms.",
    ),
    (
        "Should I use every recommended product?",
        "No. Recommended products are alternatives, not a shopping checklist. "
        "Check ingredient labels, introduce one product at a time, and patch test "
        "when appropriate.",
    ),
]

def render():
    """
    Render the Chatbot page.
    Provides conversational interface for skincare questions.
    """

    st.title("💬 SkinCare AI Assistant")
    st.markdown("Ask me anything about skincare, your analysis results, or get personalized advice!")

    with st.expander("❓ Frequently Asked Questions"):
        for index, (question, answer) in enumerate(FAQ_ITEMS):
            st.markdown(f"**{question}**")
            st.write(answer)
            if index < len(FAQ_ITEMS) - 1:
                st.divider()

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

        st.markdown("---")

        # Quick questions
        st.markdown("### 💡 Quick Questions")
        st.caption("Click to ask:")

        quick_questions = [
            "What products should I use for my skin type?",
            "How can I improve my skin quality score?",
            "Explain my latest analysis results",
            "What causes premature skin aging?",
            "Best skincare routine for beginners?"
        ]

        for i, question in enumerate(quick_questions):
            if st.button(question, key=f"quick_q_{i}", use_container_width=True):
                # Add question to chat
                handle_user_message(question)
                st.rerun()


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
