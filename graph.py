from intents import detect_intent
from rag import answer_from_kb
from tools import mock_lead_capture


def build_graph():
    class Bot:
        def invoke(self, payload):
            msg = payload['message']
            state = payload['state']
            intent = detect_intent(msg)
            state['intent'] = intent

            if 'qualified' not in state:
                state['qualified'] = False

            if state['qualified']:
                if not state.get('name'):
                    state['name'] = msg
                    return {'reply': 'Please share your email.', 'state': state}

                if not state.get('email'):
                    state['email'] = msg
                    return {'reply': 'Which creator platform do you use? (YouTube / Instagram etc.)', 'state': state}

                if not state.get('platform'):
                    state['platform'] = msg
                    mock_lead_capture(state['name'], state['email'], state['platform'])
                    return {'reply': 'Thanks! Your request has been submitted.', 'state': state}

            if intent == 'greeting':
                return {'reply': 'Hi! How can I help you today?', 'state': state}

            if intent == 'product_query':
                return {'reply': answer_from_kb(msg), 'state': state}

            if intent == 'high_intent':
                state['qualified'] = True
                return {'reply': 'Great to hear that. Can I get your name?', 'state': state}

            return {'reply': 'Can you tell me more about what you need?', 'state': state}

    return Bot()