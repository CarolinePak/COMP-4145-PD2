"""Local demo profiles for the SkinInsight Streamlit application."""

import json
import os
import shutil
import uuid
from datetime import datetime

import streamlit as st

from config import config


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
    """Render the local profile selector or the active user's dashboard."""
    st.title("👤 My Profile")
    st.caption("Local demo profile · Your data is stored only on this device.")

    if st.session_state.get("user_id"):
        user = load_user(st.session_state.user_id)
        if user:
            _render_dashboard(user)
            return
        _clear_active_profile()

    _render_profile_entry()


def _render_profile_entry():
    st.subheader("Welcome to SkinInsight")
    st.write("Create a small local profile or continue with an existing one.")

    create_tab, existing_tab = st.tabs(["Create profile", "Existing profile"])

    with create_tab:
        with st.form("create_profile_form"):
            username = st.text_input(
                "Username",
                max_chars=30,
                placeholder="How should we call you?",
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

    heading, switch = st.columns([4, 1])
    with heading:
        st.subheader(f"Welcome back, {user['username']} 👋")
        st.write("Your skincare journey at a glance.")
    with switch:
        if st.button("Switch profile", use_container_width=True):
            _clear_active_profile()
            st.rerun()

    total = len(analyses)
    latest_score = latest.get("skin_quality_score") if latest else None
    improvement = None
    if len(analyses) >= 2:
        improvement = latest_score - analyses[0].get("skin_quality_score", 0)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total analyses", total)
    col2.metric("Latest quality score", f"{latest_score}/10" if latest_score is not None else "N/A")
    col3.metric(
        "Change since first analysis",
        f"{improvement:+.1f}" if improvement is not None else "N/A",
    )

    st.divider()
    goals_col, assessment_col = st.columns([1, 2])

    with goals_col:
        st.markdown("### 🎯 Skincare goals")
        if st.session_state.get("editing_profile"):
            _render_goal_editor(user)
        else:
            for goal in user.get("skincare_goals", []):
                st.markdown(f"- {goal}")
            if st.button("Edit goals", use_container_width=True):
                st.session_state.editing_profile = True
                st.rerun()
        st.caption("Used to personalize chatbot answers and recommendations.")

    with assessment_col:
        st.markdown("### 🔬 Latest AI assessment")
        if latest:
            timestamp = _format_timestamp(latest.get("timestamp"))
            st.caption(f"Last analyzed: {timestamp}")
            score1, score2, score3 = st.columns(3)
            score1.metric("Skin quality", f"{latest.get('skin_quality_score', 'N/A')}/10")
            score2.metric("Cleanliness", f"{latest.get('skin_cleanliness_score', 'N/A')}/10")
            score3.metric("Estimated age", latest.get("age_estimate", "N/A"))

            concerns = latest.get("concerns", [])
            st.markdown("**Visible concerns**")
            st.write(", ".join(concerns) if concerns else "No visible concerns reported.")
            st.markdown("**AI summary**")
            st.write(latest.get("skin_condition_description", "No summary available."))
            st.caption("AI-estimated from the latest photo; this is not a medical diagnosis.")
        else:
            st.info(
                "No skin analysis yet. Open Skin Analysis from the sidebar to complete your first assessment."
            )

    st.divider()
    st.markdown("### Quick actions")
    action1, action2, action3 = st.columns(3)
    action1.button(
        "🔬 New skin analysis",
        type="primary",
        use_container_width=True,
        on_click=_navigate_to,
        args=("🏠 Skin Analysis",),
    )
    action2.button(
        "📊 View history",
        use_container_width=True,
        on_click=_navigate_to,
        args=("📊 History",),
    )
    action3.button(
        "💄 Get recommendations",
        use_container_width=True,
        on_click=_navigate_to,
        args=("💄 Recommendations",),
    )

    with st.expander("Local profile management"):
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


def _navigate_to(page):
    """Update the sidebar navigation from a profile quick action."""
    st.session_state.navigation_page = page


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
