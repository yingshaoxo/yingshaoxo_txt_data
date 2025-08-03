hi = """
"""

splits = hi.split("___")
new_text = ""
for one in splits:
    new_text += one[::-1] + "\n____\n"
print(new_text)
