def detect_intent(text: str) -> str:
    t = text.lower()

    if any(x in t for x in ['hi', 'hello', 'hey']):
        return 'greeting'

    if any(x in t for x in ['price', 'pricing', 'plan', 'cost', 'refund', 'support']):
        return 'product_query'

    if any(x in t for x in ['want to buy', 'sign up', 'try pro', 'start now', 'interested', 'subscribe']):
        return 'high_intent'

    return 'general'