# n = '[1,2,5,6,7,9,12,55,56,57,58,60,61,62,64,65,70]'
n = '[1,2,5,6,7,9,12,55,56,57,58,60,61,62,64,65,70]'
# n = '[2,1,3,6]'
# numbers = sorted(map(lambda s: int(s), n.split(',')))
numbers = sorted(map(lambda s: int(s), n[1:-1].split(',')))

i = 1
cursor = numbers[0]
numbers += [-1]
cnt = 1
in_range = False
while i < len(numbers):
    n = numbers[i]

    if (cursor + 1) == n:
        in_range = True
        cnt += 1
        cursor += 1
    elif in_range or n == -1:
        if cnt > 2:
            numbers = numbers[0:i-cnt] + ['{}{}{}'.format(numbers[i-cnt], '-', numbers[i-1])] + numbers[i:]
            i = i - cnt + 1
        cursor = n
        cnt = 1
        in_range = False
    else:
        cursor = n
    i += 1

print ','.join(map(str, numbers[:-1]))
