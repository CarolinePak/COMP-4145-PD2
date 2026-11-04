# app.py

import streamlit as st
from config import config

# Import modules
from modules import skin_analysis, chatbot

# MUST be first Streamlit command
st.set_page_config(
    page_title=f"{config.APP_ICON} {config.APP_TITLE}",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.analyses = []
        st.session_state.chat_history = []
        st.session_state.current_analysis = None
        st.session_state.recommendations = None

init_session_state()

# Sidebar navigation
with st.sidebar:
    st.title(f"{config.APP_ICON} {config.APP_TITLE}")
    st.markdown("---")

    # Navigation menu
    page = st.radio(
        "Navigate to:",
        [
            "🏠 Skin Analysis",
            "💬 Chatbot",
            "👤 My Profile",
            "📊 History",
            "💄 Recommendations"
        ],
        index=0,
        label_visibility="visible"
    )

    st.markdown("---")

    # API Configuration
    with st.expander("⚙️ API Settings", expanded=False):
        st.markdown("**Configure your API key:**")

        api_key_input = st.text_input(
            "API Key",
            value=config.API_KEY if config.API_KEY else "",
            type="password",
            help="Enter your GPT-6-Luna API key from your instructor"
        )

        if st.button("💾 Save API Key", use_container_width=True):
            config.API_KEY = api_key_input
            # Update the global client with new key
            from modules.api_client import llm_client
            llm_client.api_key = api_key_input
            st.success("✅ API Key saved for this session!")
            st.info("💡 Note: Key is only saved for current session. Add to .env file for persistence.")

    st.markdown("---")

    # About section
    with st.expander("ℹ️ About SkinInsight"):
        st.markdown("""
        **SkinInsight** is an AI-powered skincare analysis platform that uses advanced language models to:

        - Analyze skin condition from photos
        - Provide personalized skincare advice
        - Track your skin health progress
        - Recommend suitable products

        **Powered by GPT-6-Luna**
        """)

    st.markdown("---")
    st.caption(f"SkinInsight v1.0 | COMP4145 PD2")

# Main content routing
if page == "🏠 Skin Analysis":
    skin_analysis.render()
elif page == "💬 Chatbot":
    chatbot.render()
elif page == "👤 My Profile":
    st.title("👤 My Profile")
    st.info("🚧 Coming soon... Manage your profile and preferences here!")
elif page == "📊 History":
    st.title("📊 History")
    st.info("🚧 Coming soon... View your skin analysis history and progress!")
elif page == "💄 Recommendations":
    st.title("💄 Recommendations")
    st.info("🚧 Coming soon... Get personalized product recommendations!")
