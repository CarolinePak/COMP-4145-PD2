"""Catalogue loading, request construction and strict response validation (no UI)."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_RECOMMENDED_PRODUCTS = 4

def load_catalogue():
    data = json.loads((ROOT / 'data/products.json').read_text(encoding='utf-8'))
    products = data['products']
    ids = [p['product_id'] for p in products]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate catalogue IDs.')
    return products

def analysis_context(analysis):
    # Minimize data shared: no photo, age, score, username or local file metadata.
    return {k: analysis.get(k, [] if k == 'concerns' else '')
            for k in ('concerns', 'skin_condition_description')}

def request_signature(analysis, catalogue):
    request_data = [analysis_context(analysis), catalogue, MAX_RECOMMENDED_PRODUCTS]
    return hashlib.sha256(json.dumps(request_data, sort_keys=True).encode()).hexdigest()

def build_messages(analysis, catalogue):
    return [
        {'role': 'system', 'content': (ROOT / 'prompts/recommendation_system.txt').read_text(encoding='utf-8')},
        {'role': 'user', 'content': json.dumps({'analysis': analysis_context(analysis), 'catalogue': catalogue})}
    ]

def text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 2000:
        raise ValueError(f'Invalid {label}.')
    return value.strip()

def validate_response(raw, catalogue):
    raw = raw.strip()
    if raw.startswith('```'):
        lines = raw.splitlines()
        if lines[-1].strip() != '```':
            raise ValueError('Incomplete response.')
        raw = '\n'.join(lines[1:-1])
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError('Expected an object.')
    for key in ('analysis_summary', 'limitations'):
        data[key] = text(data.get(key), key)
    products = data.get('products')
    if not isinstance(products, list) or len(products) > MAX_RECOMMENDED_PRODUCTS:
        raise ValueError(f'Expected up to {MAX_RECOMMENDED_PRODUCTS} products.')
    known = {p['product_id'] for p in catalogue}
    selected = set()
    for p in products:
        if not isinstance(p, dict) or p.get('product_id') not in known or p['product_id'] in selected:
            raise ValueError('Unknown or duplicate product ID.')
        selected.add(p['product_id'])
        p['why'] = text(p.get('why'), 'recommendation reason')
        p['selection_note'] = text(p.get('selection_note'), 'selection note')
    routine = data.get('routine')
    if not isinstance(routine, dict):
        raise ValueError('Missing routine.')
    for period in ('morning', 'evening'):
        steps = routine.get(period)
        if not isinstance(steps, list) or not 1 <= len(steps) <= 5:
            raise ValueError('Invalid routine steps.')
        for step in steps:
            if not isinstance(step, dict) or 'product_id' not in step:
                raise ValueError('Invalid routine step.')
            step['instruction'] = text(step.get('instruction'), 'instruction')
            if step['product_id'] is not None and step['product_id'] not in selected:
                raise ValueError('Routine references an unselected product.')
    tips = data.get('tips')
    if not isinstance(tips, list) or len(tips) > 3:
        raise ValueError('Invalid tips.')
    data['tips'] = [text(t, 'tip') for t in tips]
    return data
