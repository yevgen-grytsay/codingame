import sys
import math


def calculate(crew, life_expectancy, duration, capacity):
    low = 20
    high = int(life_expectancy / 2)
    population = 0

    for _ in range(1, duration):
        new_crew = advance_time(crew, life_expectancy)
        babies = calc_new_babies(new_crew, low, high)
        if babies > 0:
            new_crew[0] = babies
        population = calc_population(new_crew)
        crew = new_crew
        if population > capacity:
            return 1
        elif population == 0:
            return -1
    if population < 200:
        return -1
    return 0


def calc_population(crew):
    return reduce(lambda sum, v: sum + v, crew.itervalues(), 0)


def advance_time(crew, life_expectancy):
    new_crew = {}
    for k, v in crew.iteritems():
        new_age = k + 1
        if new_age <= life_expectancy:
            new_crew[new_age] = v
    return new_crew


def calc_new_babies(crew, low, high):
    """
    :type crew: dict
    :type low: int
    :type high: int
    :rtype: int
    """
    sum = 0
    for k, v in crew.iteritems():
        if low <= k <= high:
            sum += v
    return int(sum / 10)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

y = int(raw_input())
c = int(raw_input())
n = int(raw_input())
crew = {}
for i in xrange(n):
    age, number = [int(j) for j in raw_input().split()]
    crew[age] = number

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

low_life = 1
high_life = 200
valid_expectancy = 0
while True:
    current_expectancy = int((high_life + low_life) / 2)
    if current_expectancy == 0:
        raise Exception("Not found")

    result = calculate(crew, current_expectancy, y, c)
    if result == 0:
        valid_expectancy = current_expectancy
        break
    elif result == -1:
        low_life = current_expectancy
    elif result == 1:
        high_life = current_expectancy

if valid_expectancy > 0:
    max_exp = valid_expectancy
    while True:
        cur_exp = max_exp + 1
        result = calculate(crew, cur_exp, y, c)
        if result == 0:
            max_exp = cur_exp
        else:
            break

    min_exp = valid_expectancy
    while True:
        cur_exp = min_exp - 1
        result = calculate(crew, cur_exp, y, c)
        if result == 0:
            min_exp = cur_exp
        else:
            break

    print min_exp, max_exp
else:
    print 0