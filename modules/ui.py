"""Shared presentation for the SkinInsight workspace."""

from contextlib import contextmanager
from html import escape

import streamlit as st


ICONS = {
    "brand": '<path d="M12 3c3 4.4 6 7 6 11a6 6 0 1 1-12 0c0-4 3-6.6 6-11Z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
    "profile": '<circle cx="12" cy="8" r="3.2"/><path d="M5 20v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1"/>',
    "scan": '<path d="M8 4H5a1 1 0 0 0-1 1v3m12-4h3a1 1 0 0 1 1 1v3M4 16v3a1 1 0 0 0 1 1h3m12-4v3a1 1 0 0 1-1 1h-3M8 12h8"/>',
    "chat": '<path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H5l1.2-3.2A7.5 7.5 0 1 1 20 11.5Z"/><path d="M9 11.5h6m-6 3h3"/>',
    "history": '<rect x="4" y="6" width="16" height="14" rx="2"/><path d="M8 4v4m8-4v4M4 10h16m-11 4h6m-6 3h3"/>',
    "routine": '<path d="M12 3.5 14 9l5.5 2-5.5 2-2 5.5-2-5.5L4.5 11 10 9l2-5.5ZM18 15l1.2 2.8L22 19l-2.8 1.2L18 23l-1.2-2.8L14 19l2.8-1.2L18 15Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
    "moon": '<path d="M20 15a8.5 8.5 0 0 1-11-11 8.5 8.5 0 1 0 11 11Z"/>',
    "lock": '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 1 1 8 0v3m-4 4v3"/>',
    "arrow": '<path d="M5 12h14m-5-5 5 5-5 5"/>',
}


def icon(name):
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{ICONS[name]}</svg>'
    )


def html(content):
    st.markdown(content, unsafe_allow_html=True)


@contextmanager
def panel(variant):
    """Give a native Streamlit container a named presentation style."""
    with st.container():
        html(f'<span class="ui-marker ui-{variant}" aria-hidden="true"></span>')
        yield


def heading(title, description, glyph):
    html(
        f'<header class="page-heading page-{glyph}"><span class="tile-icon">{icon(glyph)}</span>'
        f'<h1>{escape(title)}</h1><p>{escape(description)}</p></header>'
    )


def card_heading(title, description, glyph, tone="clay"):
    html(
        f'<div class="card-heading {tone}"><span class="tile-icon">{icon(glyph)}</span>'
        f'<h3>{escape(title)}</h3><p>{escape(description)}</p></div>'
    )


def empty_state(title, description, glyph):
    html(
        f'<div class="empty-state"><span class="tile-icon">{icon(glyph)}</span>'
        f'<h3>{escape(title)}</h3><p>{escape(description)}</p></div>'
    )


def navigate(page):
    st.session_state.navigation_page = page


def page_button(label, page, *, key, primary=False, full=False):
    return st.button(
        label, key=key, type="primary" if primary else "secondary",
        use_container_width=full, on_click=navigate, args=(page,),
    )
