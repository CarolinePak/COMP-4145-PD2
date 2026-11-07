import math
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st


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
    st.title("📊 Analysis History")

    records = st.session_state.get("analyses", [])
    grouped = get_daily_records(records)

    this_week, all_records = st.tabs(["This Week", "All Records"])

    with this_week:
        today = datetime.now(TIMEZONE).date()
        monday = today - timedelta(days=today.weekday())
        days = [monday + timedelta(days=i) for i in range(7)]

        daily_scores = {
            day: average_score(grouped.get(day, []))
            for day in days
        }

        valid_scores = [
            score for score in daily_scores.values()
            if score is not None
        ]
        highest = max(valid_scores) if valid_scores else None

        st.caption(f"{monday:%d %b} – {days[-1]:%d %b %Y}")

        # Static styles; no user text is inserted into HTML.
        st.markdown(
            """
            <style>
            .week-card {
                text-align: center;
                border-radius: 12px;
                padding: 14px 2px;
                border: 1px solid #d1d5db;
                min-height: 145px;
                box-sizing: border-box;
            }
            .week-card .weekday {
                font-size: 14px;
                font-weight: 600;
            }
            .week-card .month {
                margin-top: 12px;
                font-size: 12px;
            }
            .week-card .day {
                font-size: 28px;
                font-weight: 700;
            }
            .week-card .status {
                margin-top: 8px;
                font-size: 11px;
            }
            .week-empty {
                background: #e5e7eb;
                color: #6b7280;
            }
            .week-recorded {
                background: #ffffff;
                color: #1f2937;
                box-shadow: 0 3px 10px #00000012;
            }
            .week-best {
                background: #dcfce7;
                color: #166534;
                border-color: #22c55e;
            }
            .week-low {
                background: #fee2e2;
                color: #991b1b;
                border-color: #ef4444;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        columns = st.columns(7)

        for index, day in enumerate(days):
            day_records = grouped.get(day, [])
            score = daily_scores[day]

            if not day_records:
                style = "week-empty"
                status = "No record"
            elif score is None:
                style = "week-recorded"
                status = "Score unavailable"
            elif score < GOOD_SCORE:
                style = "week-low"
                status = f"{score:.1f}/10 · Low"
            elif highest is not None and math.isclose(score, highest):
                style = "week-best"
                status = f"{score:.1f}/10 · Best"
            else:
                style = "week-recorded"
                status = f"{score:.1f}/10"

            with columns[index]:
                st.markdown(
                    f"""
                    <div class="week-card {style}">
                        <div class="weekday">{weekdays[index]}</div>
                        <div class="month">{day:%b}</div>
                        <div class="day">{day.day}</div>
                        <div class="status">{status}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.caption(
            "Gray: no record · White: recorded · "
            "Green: weekly best at 7+ · Red: below 7"
        )
        st.caption(
            "Daily scores average the AI cleanliness and quality scores "
            "across valid records. These are not medical measurements."
        )

        st.divider()
        st.subheader("This Week's Records")

        week_records = [
            record
            for day in reversed(days)
            for record in grouped.get(day, [])
        ]

        if not week_records:
            st.info("No records this week. Complete a skin analysis first.")

        for index, record in enumerate(week_records):
            with st.expander(
                f"{record.get('timestamp', '')} · Record {index + 1}"
            ):
                col1, col2 = st.columns(2)
                col1.metric(
                    "Cleanliness",
                    f"{record.get('skin_cleanliness_score', 'N/A')}/10",
                )
                col2.metric(
                    "Skin Quality",
                    f"{record.get('skin_quality_score', 'N/A')}/10",
                )
                st.write(record.get("skin_condition_description", ""))
                st.write("Notes:", record.get("user_note") or "No notes.")

    with all_records:
        st.date_input("Select a date")
        st.info("Date filtering will be added in the next step.")