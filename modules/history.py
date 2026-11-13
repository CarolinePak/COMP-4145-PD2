import math
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st

from modules import ui


TIMEZONE = ZoneInfo("Asia/Hong_Kong")
GOOD_SCORE = 7


def get_daily_records(records):
    """Group actual records by their Hong Kong date."""
    grouped = {}

    for record in records:
        try:
            timestamp = datetime.fromisoformat(record["timestamp"])

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=TIMEZONE)

            day = timestamp.astimezone(TIMEZONE).date()
            grouped.setdefault(day, []).append(record)
        except (KeyError, TypeError, ValueError):
            continue

    return grouped


def average_score(records):
    """Return a daily average without inventing missing scores."""
    scores = []

    for record in records:
        try:
            raw_scores = [
                record["skin_cleanliness_score"],
                record["skin_quality_score"],
            ]

            if any(isinstance(value, bool) for value in raw_scores):
                continue

            cleanliness, quality = map(float, raw_scores)

            if all(
                math.isfinite(value) and 0 <= value <= 10
                for value in (cleanliness, quality)
            ):
                scores.append((cleanliness + quality) / 2)

        except (KeyError, TypeError, ValueError):
            continue

    return sum(scores) / len(scores) if scores else None


def render():
    ui.heading("Skin History", "Revisit your saved assessments and follow changes over time.", "history")
    grouped = get_daily_records(st.session_state.get("analyses", []))
    week_view, all_records = st.tabs(["Weekly view", "All records"])

    with week_view, ui.panel("card"):
        _render_week(grouped)
    with all_records, ui.panel("card"):
        if grouped:
            selected = st.selectbox(
                "Filter by date",
                [None, *sorted(grouped, reverse=True)],
                format_func=lambda day: day.strftime("%d %b %Y") if day else "All dates",
            )
            days = [selected] if selected else sorted(grouped, reverse=True)
            _render_records(days, grouped)
        else:
            _empty_history("Saved assessments will appear here after your first skin analysis.")


def _change_week(offset):
    st.session_state.history_week_offset = offset


def _render_week(grouped):
    today = datetime.now(TIMEZONE).date()
    offset = st.session_state.get("history_week_offset", 0)
    monday = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)
    days = [monday + timedelta(days=i) for i in range(7)]
    scores = {day: average_score(grouped.get(day, [])) for day in days}
    highest = max((score for score in scores.values() if score is not None), default=None)

    st.header(f"{monday:%d %b} – {days[-1]:%d %b %Y}")
    with ui.panel("week-controls"):
        previous, current = st.columns(2, gap="small")
        previous.button("Previous", help="Show the previous week", on_click=_change_week, args=(offset - 1,), use_container_width=True)
        current.button("This week", on_click=_change_week, args=(0,), disabled=offset == 0, use_container_width=True)

    tiles = []
    for day, score in scores.items():
        tone, status = _day_status(grouped.get(day, []), score, highest)
        current = ' aria-current="date"' if day == today else ""
        tone += " today" if day == today else ""
        tiles.append(
            f'<div class="calendar-day {tone}"{current}><span>{day:%a}</span>'
            f'<strong>{day.day}</strong><span>{status}</span></div>'
        )
    ui.html(f'<div class="calendar-grid">{"".join(tiles)}</div>')
    st.caption("Daily scores average the AI cleanliness and quality estimates across valid assessments.")

    st.subheader("Assessments this week")
    if any(day in grouped for day in days):
        _render_records(reversed(days), grouped)
    else:
        ui.empty_state("No assessments this week", "Check another week or open All records.", "history")


def _day_status(records, score, highest):
    if not records:
        return "", "No record"
    if score is None:
        return "recorded", "Score unavailable"
    if score < GOOD_SCORE:
        return "low", f"{score:.1f}/10 · Low"
    if highest is not None and math.isclose(score, highest):
        return "best", f"{score:.1f}/10 · Best"
    return "recorded", f"{score:.1f}/10"


def _empty_history(description):
    ui.empty_state("No assessments yet", description, "history")


def _render_records(days, grouped):
    for day in days:
        for index, record in enumerate(reversed(grouped.get(day, [])), 1):
            timestamp = datetime.fromisoformat(record["timestamp"])
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=TIMEZONE)
            time = timestamp.astimezone(TIMEZONE).strftime("%H:%M")
            with st.expander(f"{day:%d %b %Y} · {time} · Record {index}"):
                with ui.panel("metrics"):
                    cleanliness, quality = st.columns(2)
                    cleanliness.metric("Cleanliness", f"{record.get('skin_cleanliness_score', '—')}/10")
                    quality.metric("Skin quality", f"{record.get('skin_quality_score', '—')}/10")
                st.write(record.get("skin_condition_description", ""))
                st.write("Notes:", record.get("user_note") or "No notes.")
