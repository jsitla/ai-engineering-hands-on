"""Ten customer messages with the correct label, used to test our prompts."""
MESSAGES = [
    ("My package still hasn't arrived after two weeks.", "shipping"),
    ("I was charged twice for the same order!", "billing"),
    ("How do I change the email address on my account?", "account"),
    ("The blender I got makes a burning smell.", "product"),
    ("Can I get an invoice with my company's VAT number?", "billing"),
    ("The tracking link says 'label created' for 5 days.", "shipping"),
    ("I can't log in, it says my password is wrong.", "account"),
    ("One of the three glasses in the set arrived cracked.", "product"),
    ("Do you deliver to Croatia?", "shipping"),
    ("Please delete my account and all my data.", "account"),
]
LABELS = ["shipping", "billing", "account", "product"]
