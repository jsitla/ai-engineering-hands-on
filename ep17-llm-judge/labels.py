"""My own verdicts on the 30 answers from episode 16 (answers.json), made by reading
each answer next to the handbook. Rule: correct = the key fact is right AND the answer
doesn't add anything false or misleading."""
LABELS = {
    "A: vector search, 1 chunk": [
        True,   # sofa 39 euros ("regardless of the order total" is a fair reading)
        True,   # 30 days
        False,  # broken lamp: talks about the warranty, not "photo + report within 14 days"
        True, True, True, True, True, True, True, True, True, True, True,
        False,  # "Yes, Northwind Home delivers to Germany" - wrong
    ],
    "B: hybrid search, 3 chunks": [
        False,  # sofa: invents "does not include shipping costs"
        False,  # 14 days: that's the damage rule, returns are 30 days
        True,   # broken lamp
        False,  # instalments: says "I don't know", but the handbook says no instalments
        True, True, True, True, True,
        False,  # VAT: sends you to a "Company Information" section that doesn't exist
        False,  # discount codes: invents an exception
        True, True, True, True,
    ],
}
