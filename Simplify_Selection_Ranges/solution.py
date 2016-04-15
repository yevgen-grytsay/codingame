# n = '[1,2,5,6,7,9,12,55,56,57,58,60,61,62,64,65,70]'
n = '[2,1,3]'
# numbers = sorted(map(lambda s: int(s), n.split(',')))
numbers = sorted(map(lambda s: int(s), n[1:-1].split(',')))

i = 1
prev = numbers[0]
numbers += [-1]
cnt = 1
in_range = False
while i < len(numbers):
    n = numbers[i]

    if (n - prev) == 1:
        in_range = True
        cnt += 1
    elif in_range or n == -1:
        if cnt > 2:
            numbers = numbers[0:i-cnt] + ['{}{}{}'.format(numbers[i-cnt], '-', numbers[i-1])] + numbers[i:]
            i = i - cnt + 1
        cnt = 1
        in_range = False
    i += 1
    prev = n

print ','.join(map(str, numbers[:-1]))