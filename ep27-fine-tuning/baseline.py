"""
Episode 27 - step 1: how good is the small model WITHOUT fine-tuning?
Short prompt, long prompt, and long prompt with examples, on 48 test messages.
"""
from common import EXAMPLES, LONG_PROMPT, SHORT_PROMPT, load_model, score

tok, model = load_model()
score(tok, model, SHORT_PROMPT, name="short prompt")
score(tok, model, LONG_PROMPT, name="long prompt")
score(tok, model, LONG_PROMPT, EXAMPLES, name="long prompt + 6 examples")
