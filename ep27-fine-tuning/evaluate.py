"""
Episode 27 - step 3: the fine-tuned model, with only the SHORT prompt.
"""
from common import SHORT_PROMPT, load_model, score

tok, model = load_model(adapter="adapter")
score(tok, model, SHORT_PROMPT, name="fine-tuned, short prompt")
