"""The golden set: questions with what a correct answer MUST contain.
Several acceptable spellings are separated by |."""
CASES = [
    ("How much does it cost to deliver a sofa?", "39"),
    ("How long do I have to send something back?", "30 days|30-day"),
    ("My lamp arrived broken. What should I do?", "photo"),
    ("Can I pay in monthly instalments?", "no|not|don't|do not"),
    ("How long is a gift card valid?", "2 years|two years"),
    ("How long is the password reset link valid?", "1 hour|one hour"),
    ("Is the chat open on Saturday?", "9:00|9 am|9am"),
    ("When do I get my money back after a return?", "14 days|14 working days"),
    ("Why was 6.90 euros taken off my refund?", "return shipping|return"),
    ("Where do I enter my VAT number?", "account settings|settings"),
    ("Can I combine two discount codes?", "one discount code|only one|no|not"),
    ("How long do you keep my invoices?", "10 years|ten years"),
    # not in the handbook: the right answer is to say so
    ("Do you sell garden furniture?", "don't know|not in the handbook"),
    ("What is your phone number?", "don't know|not in the handbook"),
    ("Do you deliver to Germany?", "no|not|don't|only"),
]
