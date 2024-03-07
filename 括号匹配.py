def check_brackets(string):
    stack = []  

    for i, char in enumerate(string):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if len(stack) > 0:
                stack.pop()
            else:
                string = string[:i] + '?' + string[i+1:]

    for index in stack:
        string = string[:index] + 'x' + string[index+1:]

    return string

inputs = [
    "bge)))))))))",
    "((IIII))))))",
    "()()()()(uuu",
    "))))UUUU((()",
]

for input_string in inputs:
    output_string = check_brackets(input_string)
    print(f"{input_string}\n{output_string}\n")