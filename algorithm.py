def check_brackets(string):
    stack = []
    mismatches = []
    for i, char in enumerate(string):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if not stack:
                mismatches.append(('?', i))
            else:
                stack.pop()
    while stack:
        mismatches.append(('x', stack.pop()))
    mismatches.sort(key=lambda x: x[1])
    marks = [' ' for _ in range(len(string))]
    for mark, index in mismatches:
        marks[index] = mark
    return ''.join(marks)
test_strings = [
    "bge))))))))",
    "(((III))))",
    "(()()()(uuu",
    "))))UUUU((("
]
for test in test_strings:
    print(test)
    print(check_brackets(test))