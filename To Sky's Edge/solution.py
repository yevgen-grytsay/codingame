import sys
import math


def calculate(crew, life_expectancy, duration, capacity):
    low = 20
    high = int(life_expectancy / 2)
    population = 0

    for _ in range(0, duration):
        crew = advance_time(crew, life_expectancy, low, high)
        population = calc_population(crew)
        if population > capacity:
            return 1
        elif population == 0:
            return -1
    if population < 200:
        return -1
    return 0


def calc_population(crew):
    return reduce(lambda sum, v: sum + v, crew.itervalues(), 0)


def advance_time(crew, life_expectancy, low, high):
    new_crew = {}
    for k, v in crew.iteritems():
        new_age = k + 1
        if new_age <= life_expectancy:
            new_crew[new_age] = v

    babies = calc_new_babies(new_crew, low, high)
    if babies > 0:
        new_crew[0] = babies
    return new_crew


def calc_new_babies(crew, low, high):
    sum = 0
    for k, v in crew.iteritems():
        if low <= k <= high:
            sum += v
    return int(sum / 10)


def find_bin_max(fnc, low, high):
    while (low + 1) != high:
        cur = (low + high) / 2
        result = fnc(cur)
        if result == -1 or result == 0:
            low = cur
        else:
            high = cur
    return low


def find_bin_min(fnc, low, high):
    while (low + 1) != high:
        cur = int(round((low + high) / 2.0))
        result = fnc(cur)
        if result == 1 or result == 0:
            high = cur
        else:
            low = cur

    return high

#
# Input
#
y = int(raw_input())
c = int(raw_input())
n = int(raw_input())
crew = {}
for i in xrange(n):
    age, number = [int(j) for j in raw_input().split()]
    crew[age] = number

low_life = 1
high_life = 200
valid_expectancy = 0


def create_calc_function(crew, y, c):
    def fnc(current_expectancy):
        return calculate(crew, current_expectancy, y, c)
    return fnc

fnc = create_calc_function(crew, y, c)
low = find_bin_min(fnc, 1, 200)
print low, find_bin_max(fnc, low, 200)