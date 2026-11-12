"""SkinInsight application shell and page navigation."""

from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="SkinInsight",
    page_icon=":material/flare:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from modules import chatbot, history, profile, recommendations, skin_analysis, ui


PAGES = {
    "My Profile": (profile.render, "profile", "Manage your goals and skin journal."),
    "Skin Analysis": (skin_analysis.render, "scan", "Review visible skin patterns from a clear photo."),
    "Chatbot": (chatbot.render, "chat", "Ask a skincare question or make sense of your results."),
    "History": (history.render, "history", "See how your saved skin assessments change over time."),
    "Recommendations": (recommendations.render, "routine", "Explore skincare products and routines based on your latest assessment."),
}

if not st.session_state.get("initialized"):
    st.session_state.update(
        initialized=True, user_id=None, username=None, analyses=[],
        chat_history=[], current_analysis=None, recommendations=None,
    )

if st.session_state.get("navigation_page") not in PAGES:
    st.session_state.navigation_page = "My Profile"

stylesheet = Path(__file__).parent / "assets" / "styles" / "premium.css"
ui.html(f"<style>{stylesheet.read_text(encoding='utf-8')}</style>")

page = st.session_state.navigation_page
with ui.panel("navigation"):
    brand, *links, settings = st.columns([2, 1.05, 1.16, .88, .82, 1.44, .9], gap="small")
    with brand:
        ui.html(
            f'<div class="wordmark"><span>{ui.icon("brand")}</span>'
            '<div>SkinInsight<small>SKIN HEALTH JOURNAL</small></div></div>'
        )
    for column, name in zip(links, PAGES):
        with column:
            ui.page_button(name, name, key=f"nav_{name}", primary=name == page, full=True)
    with settings:
        with st.popover("Settings", use_container_width=True):
            st.markdown("#### AI settings")
            api_key = st.text_input(
                "API key", type="password",
                help="Use the API key supplied by your instructor.",
            )
            if st.button("Save API key", type="primary"):
                if api_key.strip():
                    st.session_state.api_key = api_key.strip()
                    st.success("API key saved for this session.")
                else:
                    st.warning("Enter an API key.")
            st.caption("AI-generated guidance is for information and does not provide a diagnosis.")

render_page, glyph, description = PAGES[page]
if page != "My Profile" and not st.session_state.get("user_id"):
    ui.heading(page, description, glyph)
    with ui.panel("card"):
        ui.empty_state(
            "Start with a profile",
            "Create or select a local profile to keep your skin insights together.",
            "profile",
        )
        ui.page_button("Go to My Profile", "My Profile", key="profile_required", primary=True)
else:
    render_page()

ui.html(
    '<footer class="site-footer"><strong>SkinInsight</strong>'
    '<span>AI-assisted skincare information for everyday use.</span></footer>'
)
