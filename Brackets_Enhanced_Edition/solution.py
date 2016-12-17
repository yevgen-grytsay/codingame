from itertools import ifilter

brackets = {')': 0, '(': 0, '}': 1, '{': 1, ']': 2, '[': 2, '>': 3, '<': 3}

n = int(raw_input())
for _ in xrange(n):
    line = raw_input()
    stack = []
    for c in ifilter(lambda c: c in brackets, line):
        if len(stack) == 0 or brackets[c] != brackets[stack[-1]]:
            stack.append(c)
        else:
            stack.pop()

    if len(stack) == 0:
        print 'true'
    else:
        print 'false'
