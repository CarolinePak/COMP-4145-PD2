"""API-generated catalogue recommendations and simple routines."""
import streamlit as st
from modules.api_client import LLMClient
from config import config
from modules.recommendation_logic import (load_catalogue, analysis_context, request_signature,
                                           build_messages, validate_response)

def render():
    st.title('Recommended Products & Skincare Routine')
    st.write('Explore product options and a simple routine based on your latest skin analysis.')
    analysis = st.session_state.get('current_analysis')
    if not analysis:
        st.info('Complete a Skin Analysis first, then return here.')
        return
    context = analysis_context(analysis)
    st.subheader('Your Analysis Summary')
    st.write(context['skin_condition_description'])
    for concern in context['concerns'] if isinstance(context['concerns'], list) else []:
        st.write('• ' + str(concern))
    if not context['concerns'] and not context['skin_condition_description']:
        st.info('There is not enough analysis information to generate recommendations.')
        return
    try:
        catalogue = load_catalogue()
    except (OSError, ValueError, KeyError):
        st.error('The product catalogue could not be loaded. Please contact the project team.')
        return
    signature = request_signature(analysis, catalogue)
    stored = st.session_state.get('recommendations')
    if stored and (not isinstance(stored, dict) or stored.get('signature') != signature):
        st.session_state.recommendations = None
        stored = None
    st.caption('Generate sends your analysis description and concerns to the configured AI service. Your photo is not sent again.')
    if st.button('Generate Recommendations', type='primary'):
        key = config.API_KEY
        if not key:
            st.warning('Enter and save your API key in API Settings first.')
            return
        st.session_state.recommendations = None
        stored = None
        try:
            with st.spinner('Selecting products and preparing your routine…'):
                client = LLMClient(api_key=key)
                result = client.call_llm(build_messages(analysis, catalogue), temperature=0.2, max_tokens=2600)
                if not result.get('success'):
                    st.error('The AI service could not complete this request. Check your API key and connection, then retry.')
                    return
                output = validate_response(result['response'], catalogue)
                stored = {'signature': signature, 'output': output}
                st.session_state.recommendations = stored
        except (ValueError, KeyError, TypeError):
            st.error('The AI response was incomplete or contained invalid product references. Please retry.')
            return
    if stored:
        output = stored['output']
        st.write(output['analysis_summary'])
        st.subheader('Recommended Products')
        st.caption('Options are not a shopping checklist. Similar products are alternatives; you do not need to use them all.')
        by_id = {p['product_id']: p for p in catalogue}
        if not output['products']:
            st.info('No suitable product match was identified from the available catalogue.')
        for selection in output['products']:
            p = by_id[selection['product_id']]
            with st.container(border=True):
                st.subheader(p['brand'] + ' — ' + p['product_name'])
                st.write(p['description'])
                st.markdown('**Why Recommended**')
                st.write(selection['why'])
                st.write(selection['selection_note'])
                st.markdown('**Benefits**')
                for benefit in p['benefits']:
                    st.write('• ' + benefit)
                st.write('Key ingredients: ' + ', '.join(p['key_ingredients']))
                with st.expander('Usage & Cautions'):
                    st.write(p['usage'])
                    st.caption(p['usage_status'])
                    for caution in p['cautions']:
                        st.write('• ' + caution)
                st.link_button('View Official Product Page', p['source_url'])
        st.subheader('Suggested Skincare Routine')
        for column, period in zip(st.columns(2), ('morning', 'evening')):
            with column:
                st.markdown('**' + period.title() + '**')
                for i, step in enumerate(output['routine'][period], 1):
                    st.write(f"{i}. {step['instruction']}")
                    if step['product_id']:
                        p = by_id[step['product_id']]
                        st.caption(p['brand'] + ' — ' + p['product_name'])
        st.subheader('Simple Skincare Tips')
        for tip in output['tips']:
            st.write('• ' + tip)
        st.info(output['limitations'])
    with st.expander(f'Browse Product Catalogue ({len(catalogue)} products)'):
        st.dataframe([{'Brand':p['brand'], 'Product':p['product_name'], 'Category':p['category'],
                       'Concerns':', '.join(p['target_concerns'])} for p in catalogue], hide_index=True)
    st.caption('AI-generated information, not a medical diagnosis. Brand claims are summarized from US official pages; regional formulas and individual suitability vary.')
