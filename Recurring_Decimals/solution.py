n = int(raw_input())

dividend = 1
fraction_parts = []
pairs = []
while True:
    pair = (dividend, n)
    if n > dividend:
        fraction_parts.append('0')
    else:
        quotient, remainder = divmod(dividend, n)
        dividend = remainder
        fraction_parts.append(str(quotient))
        if remainder == 0:
            break

    if pair in pairs:
        index = pairs.index(pair)
        fraction_parts = fraction_parts[:-1]
        fraction_parts.insert(index, '(')
        fraction_parts.append(')')
        break

    pairs.append(pair)
    dividend *= 10

fraction_parts.insert(1, '.')
print ''.join(fraction_parts)