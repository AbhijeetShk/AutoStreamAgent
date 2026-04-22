import json


def load_kb():
    with open('knowledge_base.json', 'r') as f:
        return json.load(f)


def answer_from_kb(question: str) -> str:
    data = load_kb()
    q = question.lower()

    if 'basic' in q:
        return 'Basic Plan: $29/month, 10 videos/month, 720p resolution.'

    if 'pro' in q:
        return 'Pro Plan: $79/month, unlimited videos, 4K resolution, AI captions.'

    if 'refund' in q:
        return data['policies']['refund']

    if 'support' in q:
        return data['policies']['support']

    return 'We offer Basic ($29) and Pro ($79) plans. Ask me anything specific.'