"""Local demo profiles for the SkinInsight Streamlit application."""

import json
import os
import shutil
import uuid
from datetime import datetime
from html import escape

import streamlit as st

from config import config
from modules import ui


SKINCARE_GOALS = [
    "Reduce acne",
    "Improve hydration",
    "Control oil",
    "Reduce redness",
    "Brighten skin",
    "Fade dark spots",
    "Anti-aging",
    "Strengthen skin barrier",
]


def render():
    """Render the profile landing page and journal."""
    user_id = st.session_state.get("user_id")
    user = load_user(user_id) if user_id else None
    if user_id and not user:
        _clear_active_profile()

    _render_hero(user)
    if user:
        _render_journal_tools()
        _render_dashboard(user)
    else:
        with ui.panel("card"):
            _render_profile_entry()


def _render_hero(user):
    with ui.panel("hero"):
        copy, portrait = st.columns([.94, 1.06], gap="small")
        with copy:
            greeting = f"Welcome back, {escape(user['username'])}" if user else "Your personal skin journal"
            ui.html(
                f'<div class="hero-copy"><div class="kicker">{greeting}</div>'
                '<h1>Get to know<br>your skin.</h1>'
                '<p>Review visible skin patterns, ask skincare questions, and track changes over time.</p></div>'
            )
            if user:
                ui.page_button("Start skin analysis", "Skin Analysis", key="hero_scan", primary=True)
            else:
                ui.html('<a class="editorial-button" href="#profile-setup" target="_self">Set up your profile</a>')
        with portrait:
            ui.html(
                '<div class="hero-photo" role="img" '
                'aria-label="A man and a woman with natural skin texture in soft daylight"></div>'
            )


def _render_journal_tools():
    ui.html('<div class="section-heading"><h2>Your skin journal</h2></div>')
    tools = [
        ("Chatbot", "Ask a skincare question", "Talk through your results or ask about everyday skincare.", "chat", "sage"),
        ("History", "Follow your progress", "Revisit your saved assessments and see what changes over time.", "history", "stone"),
        ("Recommendations", "Build your routine", "Explore products and a routine based on your latest assessment.", "routine", "clay"),
    ]
    with ui.panel("tools"):
        for column, (page, title, description, glyph, tone) in zip(st.columns(3), tools):
            with column, ui.panel(f"feature {tone}"):
                ui.card_heading(title, description, glyph, tone)
                ui.page_button(f"Open {page.lower()}", page, key=f"journal_{page}")


def _render_profile_entry():
    ui.html('<div id="profile-setup" class="section-heading"><h2>Your profile</h2>'
            '<p>Create a local profile or continue with one already on this device.</p></div>')
    create_tab, existing_tab = st.tabs(["Create profile", "Existing profile"])

    with create_tab:
        with st.form("create_profile_form"):
            username = st.text_input(
                "Username",
                max_chars=30,
                placeholder="What should we call you?",
            )
            goals = st.multiselect(
                "Skincare goals",
                SKINCARE_GOALS,
                help="Choose up to three goals. You can change these later.",
                max_selections=3,
            )
            submitted = st.form_submit_button(
                "Create profile", type="primary", use_container_width=True
            )

        if submitted:
            error = _validate_new_profile(username, goals)
            if error:
                st.error(error)
            else:
                user = create_user(username.strip(), goals)
                _activate_user(user)
                st.success("Profile created.")
                st.rerun()

    with existing_tab:
        users = list_users()
        if not users:
            st.info("No local profiles yet. Create the first profile above.")
        else:
            labels = {user["user_id"]: user["username"] for user in users}
            user_ids = list(labels)
            last_user_id = load_last_user_id()
            default_index = (
                user_ids.index(last_user_id)
                if last_user_id in user_ids
                else 0
            )
            selected_id = st.selectbox(
                "Select local profile",
                user_ids,
                index=default_index,
                format_func=lambda user_id: labels[user_id],
            )
            if st.button(
                "Continue with this profile", type="primary", use_container_width=True
            ):
                user = load_user(selected_id)
                if user:
                    _activate_user(user)
                    st.rerun()


def _render_dashboard(user):
    analyses = load_user_analyses(user["user_id"])
    latest = analyses[-1] if analyses else None
    latest_score = latest.get("skin_quality_score") if latest else None
    first_score = analyses[0].get("skin_quality_score") if len(analyses) >= 2 else None
    improvement = (
        latest_score - first_score
        if isinstance(latest_score, (float, int)) and isinstance(first_score, (float, int))
        else None
    )

    with ui.panel("dashboard"):
        goals_col, assessment_col = st.columns([.85, 1.55])
        with goals_col, ui.panel("card"):
            st.header("Skincare goals")
            if st.session_state.get("editing_profile"):
                _render_goal_editor(user)
            else:
                goals = user.get("skincare_goals", [])
                if goals:
                    tags = "".join(f'<li>{escape(goal)}</li>' for goal in goals)
                    ui.html(f'<ul class="goal-tags">{tags}</ul>')
                else:
                    st.caption("No goals selected yet.")
                if st.button("Edit goals"):
                    st.session_state.editing_profile = True
                    st.rerun()

        with assessment_col, ui.panel("card"):
            st.header("Assessment overview")
            with ui.panel("metrics"):
                count_col, score_col, change_col = st.columns(3)
                count_col.metric("Saved analyses", len(analyses))
                score_col.metric("Latest quality score", f"{latest_score}/10" if latest_score is not None else "—")
                change_col.metric("Change since first", f"{improvement:+.1f}" if improvement is not None else "—")
            if latest:
                st.caption(f"Last analyzed {_format_timestamp(latest.get('timestamp'))}")
                concerns = latest.get("concerns") or []
                if concerns:
                    st.write("**Visible concerns**")
                    st.write(", ".join(concerns))
                st.write(latest.get("skin_condition_description") or "No summary available.")
                with st.expander("Additional measures"):
                    st.write(f"**Cleanliness score** {latest.get('skin_cleanliness_score', '—')}/10")
                    st.write(f"**Estimated age** {latest.get('age_estimate', '—')}")
            else:
                st.caption("Complete your first skin analysis to see your assessment here.")

    with st.expander("Manage profile"):
        if st.button("Switch profile"):
            _clear_active_profile()
            st.rerun()
        st.caption(
            f"Created {_format_timestamp(user.get('created_at'))}. Profile data is stored locally as JSON."
        )
        if st.checkbox("I understand this will permanently delete this profile and its analyses"):
            if st.button("Delete local profile", type="secondary"):
                delete_user(user["user_id"])
                _clear_active_profile()
                st.rerun()


def _render_goal_editor(user):
    with st.form("edit_goals_form"):
        goals = st.multiselect(
            "Skincare goals",
            SKINCARE_GOALS,
            default=user.get("skincare_goals", []),
            max_selections=3,
        )
        save_col, cancel_col = st.columns(2)
        save = save_col.form_submit_button("Save", type="primary", use_container_width=True)
        cancel = cancel_col.form_submit_button("Cancel", use_container_width=True)

    if save:
        if not goals:
            st.error("Choose at least one skincare goal.")
        else:
            user["skincare_goals"] = goals
            _write_json(_user_path(user["user_id"]), user)
            st.session_state.editing_profile = False
            st.rerun()
    if cancel:
        st.session_state.editing_profile = False
        st.rerun()


def create_user(username, goals):
    """Create and persist a local user profile."""
    os.makedirs(config.USERS_DIR, exist_ok=True)
    user = {
        "user_id": str(uuid.uuid4()),
        "username": username,
        "skincare_goals": goals,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    _write_json(_user_path(user["user_id"]), user)
    return user


def list_users():
    """Return all valid local profiles sorted by username."""
    os.makedirs(config.USERS_DIR, exist_ok=True)
    users = []
    for filename in os.listdir(config.USERS_DIR):
        if not filename.endswith(".json") or filename in {
            "users_index.json",
            "last_profile.json",
        }:
            continue
        try:
            with open(os.path.join(config.USERS_DIR, filename), encoding="utf-8") as file:
                user = json.load(file)
            if user.get("user_id") and user.get("username"):
                users.append(user)
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(users, key=lambda item: item["username"].casefold())


def load_user(user_id):
    """Load one local profile, returning None if unavailable."""
    try:
        with open(_user_path(user_id), encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError, TypeError):
        return None


def load_user_analyses(user_id):
    """Load a user's valid analyses in chronological order."""
    directory = os.path.join(config.ANALYSES_DIR, user_id)
    if not os.path.isdir(directory):
        return []
    analyses = []
    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join(directory, filename), encoding="utf-8") as file:
                analyses.append(json.load(file))
        except (OSError, json.JSONDecodeError):
            continue
    return sorted(analyses, key=lambda item: item.get("timestamp", ""))


def delete_user(user_id):
    """Delete a local profile and its saved analyses."""
    try:
        os.remove(_user_path(user_id))
    except FileNotFoundError:
        pass
    analysis_directory = os.path.join(config.ANALYSES_DIR, user_id)
    if os.path.isdir(analysis_directory):
        shutil.rmtree(analysis_directory)
    if load_last_user_id() == user_id:
        try:
            os.remove(_last_profile_path())
        except FileNotFoundError:
            pass


def _activate_user(user):
    analyses = load_user_analyses(user["user_id"])
    st.session_state.user_id = user["user_id"]
    st.session_state.username = user["username"]
    st.session_state.analyses = analyses
    st.session_state.current_analysis = analyses[-1] if analyses else None
    st.session_state.chat_history = []
    st.session_state.recommendations = None
    st.session_state.editing_profile = False
    _write_json(_last_profile_path(), {"user_id": user["user_id"]})


def _clear_active_profile():
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.analyses = []
    st.session_state.current_analysis = None
    st.session_state.chat_history = []
    st.session_state.recommendations = None
    st.session_state.editing_profile = False


def _validate_new_profile(username, goals):
    username = username.strip()
    if not username:
        return "Enter a username."
    if not goals:
        return "Choose at least one skincare goal."
    if any(user["username"].casefold() == username.casefold() for user in list_users()):
        return "That username already exists on this device."
    return None


def _user_path(user_id):
    return os.path.join(config.USERS_DIR, f"{user_id}.json")


def _last_profile_path():
    return os.path.join(config.USERS_DIR, "last_profile.json")


def load_last_user_id():
    """Return the last activated local profile ID, if it can be read."""
    try:
        with open(_last_profile_path(), encoding="utf-8") as file:
            data = json.load(file)
        user_id = data.get("user_id")
        return user_id if isinstance(user_id, str) else None
    except (OSError, json.JSONDecodeError, AttributeError):
        return None


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def _format_timestamp(value):
    if not value:
        return "Unknown"
    try:
        return datetime.fromisoformat(value).strftime("%b %d, %Y")
    except (TypeError, ValueError):
        return str(value)
