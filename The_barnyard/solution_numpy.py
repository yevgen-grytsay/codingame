from StringIO import StringIO

import numpy as np

input_str = None
# input_str = StringIO('''5
# Cows Pegasi Demons Chickens Rabbits
# Eyes 128
# Heads 61
# Legs 202
# Wings 72
# Horns 34
# ''')
if input_str:
    def raw_input():
        return next(input_str)

n = int(raw_input())
species_list = raw_input().split()
things = []
number_of_things = []
for i in xrange(n):
    thing, number = raw_input().split()
    number = int(number)
    things.append(thing)
    number_of_things.append(number)

thing_index_map = {'Heads': 0, 'Horns': 1, 'Legs': 2, 'Wings': 3, 'Eyes': 4}
thing_map = {
    'Rabbits':  [1, 0, 4, 0, 2],
    'Chickens': [1, 0, 2, 2, 2],
    'Cows':     [1, 2, 4, 0, 2],
    'Pegasi':   [1, 0, 4, 2, 2],
    'Demons':   [1, 4, 4, 2, 4]
}
A = []
index_list = [thing_index_map[t] for t in things]
# print index_list
for species in species_list:
    constants = [thing_map[species][i] for i in index_list]
    A.append(constants)

Am = zip(*A)
# print Am, number_of_things

a = np.array(Am)
b = np.array(number_of_things)
x = np.linalg.solve(a, b)
# print zip(species_list, map(int, x))
for t in zip(species_list, map(lambda n: '%d' % n, x)):
    print ' '.join(t)