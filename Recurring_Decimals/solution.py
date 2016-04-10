import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n = int(raw_input())
n = 2
n = 7
n = 195312500
n = 561
# n = 210

dividend = 1
dividend *= 10
fraction_parts = []
pairs = []

while True:
    zeroes = []
    # pair_candidates = [(dividend, n)]
    if n > dividend:
        fraction_parts.append('0')
    else:
        quotient = dividend / n
        dividend -= quotient * n
        fraction_parts.append(str(quotient))
        remainder = dividend % n
        if dividend == 0:
            break

    pair = (dividend, n)
    if pair in pairs:
        fraction_parts = fraction_parts[:-1]
        fraction_parts.insert(0, '(')
        fraction_parts.append(')')
        break

    # if len(zeroes):
    #     pairs.append(pair_candidate)

    pairs.append(pair)
    dividend *= 10
# quotient
# reminder


# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

print '0.' + ''.join(fraction_parts)