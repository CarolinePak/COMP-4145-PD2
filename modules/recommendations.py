"""Catalogue recommendations and daily routines based on the latest analysis."""

from html import escape

import streamlit as st

from modules import ui
from modules.api_client import client_for_session
from modules.recommendation_logic import (
    analysis_context,
    build_messages,
    load_catalogue,
    request_signature,
    validate_response,
)


def render():
    ui.heading(
        "Recommendations",
        "Explore product options and a daily routine based on your latest skin analysis.",
        "routine",
    )
    analysis = st.session_state.get("current_analysis")
    if not analysis:
        _render_start()
        return

    context = analysis_context(analysis)
    if not context["concerns"] and not context["skin_condition_description"]:
        st.info("There is not enough analysis information to generate recommendations.")
        return

    try:
        catalogue = load_catalogue()
    except (OSError, ValueError, KeyError):
        st.error("The product catalogue could not be loaded. Please contact the project team.")
        return

    signature = request_signature(analysis, catalogue)
    stored = st.session_state.get("recommendations")
    if stored is not None and (
        not isinstance(stored, dict) or stored.get("signature") != signature
    ):
        st.session_state.recommendations = None
        stored = None

    output = stored["output"] if stored else None
    description = context["skin_condition_description"]
    with ui.panel("card ui-recommendation-overview"):
        if output:
            summary_col, actions_col = st.columns([2.25, 1])
            with summary_col:
                _render_summary(output["analysis_summary"], context["concerns"])
            with actions_col:
                with st.expander("Review analysis or regenerate"):
                    if description:
                        st.write(description)
                    _render_generate(analysis, catalogue, signature, "Regenerate recommendations")
        else:
            _render_summary(description, context["concerns"])
            _render_generate(analysis, catalogue, signature, "Generate Recommendations")

    if output:
        _render_results(output, catalogue)
    else:
        _render_catalogue(catalogue)

    st.caption("AI-generated skincare information. For educational use only.")


def _render_summary(summary, concerns):
    st.header("Your skin at a glance")
    content = f"<p>{escape(summary)}</p>" if isinstance(summary, str) and summary else ""
    if isinstance(concerns, list) and concerns:
        tags = "".join(f"<li>{escape(str(concern))}</li>" for concern in concerns)
        content += f'<ul class="goal-tags" aria-label="Visible concerns">{tags}</ul>'
    if content:
        ui.html(f'<div class="recommendation-summary">{content}</div>')


def _render_generate(analysis, catalogue, signature, label):
    st.caption("The AI service receives your analysis description, visible concerns, and the product catalogue.")
    if not st.button(label, type="primary"):
        return
    client = client_for_session()
    if not client.api_key:
        st.warning("Open Settings and save your API key to generate recommendations.")
        return

    try:
        with st.spinner("Preparing your routine and product options…"):
            result = client.call_llm(
                build_messages(analysis, catalogue), temperature=0.2, max_tokens=2600
            )
            if not result.get("success"):
                st.error("The AI service could not complete the request. Check your API key and connection, then retry.")
                return
            output = validate_response(result["response"], catalogue)
    except (AttributeError, KeyError, TypeError, ValueError):
        st.error("The AI response was incomplete or contained invalid product references. Please retry.")
        return

    st.session_state.recommendations = {"signature": signature, "output": output}
    st.rerun()


def _render_results(output, catalogue):
    by_id = {product["product_id"]: product for product in catalogue}
    with ui.panel("recommendation-results"):
        products_tab, routine_tab, tips_tab = st.tabs(
            ["Product options", "Daily routine", "Tips & cautions"]
        )

        with products_tab:
            _render_products(output["products"], by_id)
            _render_catalogue(catalogue)

        with routine_tab:
            _render_routine(output["routine"], by_id)

        with tips_tab:
            if output["tips"]:
                with ui.panel("card"):
                    st.header("Everyday tips")
                    tips = "".join(f"<li>{escape(tip)}</li>" for tip in output["tips"])
                    ui.html(f'<ul class="recommendation-tips">{tips}</ul>')
            with ui.panel("card"):
                st.header("Limitations and cautions")
                ui.html(f'<p class="recommendation-note">{escape(output["limitations"])}</p>')
                st.caption("Brand claims come from US product pages. Formulas and suitability may vary by region and person.")


def _render_routine(routine, by_id):
    cards = []
    for period, glyph in (("morning", "sun"), ("evening", "moon")):
        steps = []
        for step in routine[period]:
            product = by_id.get(step["product_id"])
            product_label = ""
            if product:
                name = escape(f"{product['brand']} · {product['product_name']}")
                product_label = f'<span class="routine-product">{name}</span>'
            steps.append(
                f"<li><p>{escape(step['instruction'])}</p>{product_label}</li>"
            )
        cards.append(
            f'<section class="routine-card {period}">'
            f'<header><span class="tile-icon">{ui.icon(glyph)}</span><h2>{period.title()}</h2></header>'
            f'<ol>{"".join(steps)}</ol></section>'
        )
    ui.html(f'<div class="routine-grid">{"".join(cards)}</div>')


def _render_products(selections, by_id):
    if not selections:
        st.info("No suitable product match was identified in the catalogue.")
        return

    with ui.panel("product-grid"):
        for start in range(0, len(selections), 2):
            for column, selection in zip(st.columns(2), selections[start:start + 2]):
                with column, ui.panel("card"):
                    _render_product_card(by_id[selection["product_id"]], selection)


def _render_product_card(product, selection):
    brand = escape(product["brand"])
    name = escape(product["product_name"])
    why = escape(selection["why"])
    note = escape(selection["selection_note"])
    ui.html(
        f'<div class="recommendation-product-copy"><h3>{name}</h3>'
        f'<p class="product-brand">{brand}</p>'
        f'<p><strong>Why it was suggested</strong><br>{why}</p>'
        f'<p><strong>How to choose</strong><br>{note}</p></div>'
    )
    with st.expander("Ingredients, benefits and usage"):
        st.write(product["description"])
        st.write("**Key ingredients**")
        st.write(", ".join(product["key_ingredients"]))
        st.write("**Benefits**")
        for benefit in product["benefits"]:
            st.write(f"• {benefit}")
        st.write("**Usage and cautions**")
        st.write(product["usage"])
        st.caption(product["usage_status"])
        for caution in product["cautions"]:
            st.write(f"• {caution}")
    st.link_button("Official product page", product["source_url"])


def _render_catalogue(catalogue):
    with st.expander(f"Browse full catalogue ({len(catalogue)} products)"):
        st.dataframe(
            [
                {
                    "Brand": product["brand"],
                    "Product": product["product_name"],
                    "Category": product["category"],
                    "Concerns": ", ".join(product["target_concerns"]),
                }
                for product in catalogue
            ],
            hide_index=True,
            use_container_width=True,
        )


def _render_start():
    with ui.panel("recommendations"):
        main, aside = st.columns([1.4, 1])
        with main, ui.panel("card"):
            ui.empty_state(
                "Start with a skin analysis",
                "Review a photo to get skincare suggestions based on your visible concerns.",
                "scan",
            )
            ui.page_button("Open Skin Analysis", "Skin Analysis", key="routine_scan", primary=True)
        with aside, ui.panel("card"):
            st.header("What you’ll get")
            ui.card_heading("Product options", "Explore catalogue products and why they were suggested.", "routine")
            ui.card_heading("Morning and evening", "See your suggested steps grouped by time of day.", "sun")
