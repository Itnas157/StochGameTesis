from examples.example_alternative import trans_str, vars

trans_str = trans_str.replace('\n', '')
trans = trans_str.split(';')
trans.pop()

print(trans)

