# coding=utf-8
import functools
from itertools import ifilter
from pprint import pprint


class Abc(object):
    brackets = list('<{[()]}>')
    pairs = [('<', '>'), ('{', '}'), ('[', ']'), ('(', ')')]
    opening = [b[0] for b in pairs]
    closing = [b[1] for b in pairs]
    counterparts = {}
    for a, b in pairs:
        counterparts[a] = b
        counterparts[b] = a

    @classmethod
    def filter_brackets(cls, char):
        return char in cls.brackets

    @classmethod
    def is_bracket(cls, char):
        return char in cls.brackets

    @classmethod
    def flip(cls, bracket):
        return cls.counterparts.get(bracket)

    @classmethod
    def to_opening(cls, bracket):
        if bracket in cls.closing:
            bracket = cls.flip(bracket)
        return bracket

    @classmethod
    def is_same(cls, a, b):
        return a == b or a == cls.flip(b)

    @classmethod
    def all_same(cls, chars):
        first = chars[0]
        return all(map(lambda c: Abc.is_same(first, c), chars[1:]))


class Bracket(object):
    def __init__(self, char):
        self.char = char

    def __eq__(self, other):
        return isinstance(other, self.__class__) and Abc.is_same(self.char, other.char)

    def __hash__(self):
        return hash(Abc.to_opening(self.char))


def assert_right_count(chars):
    if len(chars) % 2 > 0:
        raise Exception("Expected even count of chars: " + "".join(chars))
    mp = aggregate(chars)
    agg = map(is_even, mp.values())
    if not all(agg):
        raise Exception("Expected even count of all bracket groups")


def is_even(number):
    return number % 2 == 0


def is_odd(number):
    return not is_even(number)


def aggregate(chars):
    brackets = map(lambda c: Bracket(c), chars)
    mp = {}
    for br in brackets:
        if br not in mp:
            mp[br] = 0
        mp[br] += 1
    return mp


def find_enclosing_indexes(chars):
    if len(chars) == 0:
        return []
    first = chars[0]
    indexes = []
    for tpl in ifilter(lambda tpl: is_even(tpl[0]) and Abc.is_same(first, tpl[1]), enumerate(chars[1:])):
        indexes.append(tpl[0] + 1)
    return indexes


def search(chars):
    if len(chars) == 0:
        return True
    assert_right_count(chars)
    if len(chars) == 2:
        if Abc.is_same(chars[0], chars[1]):
            return True
        else:
            raise Exception("Two brackets should be same: " + "".join(chars))

    if is_even(len(chars)) and Abc.all_same(chars):
        return True

    indexes = find_enclosing_indexes(chars)
    result_ind = []
    at_least_one_good = False
    for ind in indexes:
        try:
            to_investigate = chars[1:ind]
            if search(to_investigate):
                at_least_one_good = True
            result_ind.append(ind)
        except:
            pass

    if not at_least_one_good and len(result_ind) == 0:
        raise Exception("No candidates for closing bracket found")

    for ind in result_ind:
        if (ind + 1) < len(chars):
            search(chars[0:ind + 1])
        search(chars[ind + 1:])


# literal = '[[[(])'
# literal = 'hocyG43uyh3mU2p9DSWFvanOerDvBdGpypCnga3Rv1jmkmfRDdH2eCT73DCYmvVEdGc2VpiYbCAtDT73RsmGe2YQMDZefxex0T[4vYERXKBtAsJAcEWq4IMW0ab8PBXsFK2IXfvIn3mOCkJ4lFIXOD0pjTkkEt7EhM05RxAnCP4iVf8arpLgl8Ls6aiWhU3iixfIk[k4VpRHvEh5RHRwpcnlhIIOGDDTjc8OVmwqfMZ76hVpWU2YLPKsF8FoZYl4hmI43sI7Yr5TFF7JRTif6Iy3MdedD6lH3YxP3y1u[u5wVfwsXg5CtFjCzLTAm79UZQAU1WLBg3JCFGYcMElUrUT7JH4UCgfR69MWGU0by8kcROI7Br8SRXWNOlUcxeG0Sv4FoPLVA3C[y1X3ljg1ge8VEAc7n7Ka0g0rOHLQZkTdTkYDQgSD8067E4t42IRvNUHIB9YVpqSotUq2fRIn2R1nyArHatDFcq08u2sD0DRkwh[va2dyDikyWV9IXgm8RTSXZTGVybMWWDV1EqpZkWZrwrmlyN3wwPtU1YaR0PHFiJ26mn2xvnvpVB0BfewOcDV0EjNVgtIl5lJt2[KNPGxIG0ucQget26S0WoKzvOwVF9zLG8mT6rS7q5fcC66qwE7oY27NWmNE0r0wg953rS31F8GwoYrVS0x50Ge7WX2DbAHY3cRL[cHqRnCAARri7lj9VPLidkTVnldJuVIYdCKanuJJMGzMyZZejvsEflBHjJ7HlkjjWsVvFMgKwoDRRbGlj1PFE8zv8oOUCAGZV7A[mxOVxoVdsuBRWXyMRUlbNyNhwKfeb8EUdugS8OPmP4fsB8F2nMLrHd1WYPCEQZBH3C3v5tod6BvQdaLKh1mBaCI6bDugnfCc6v[Cw5YQoGjdzuQpT6yrN6jRCo9AIGTftwfxfMCI3Qwo1SDkQKBstI9mecQ8tmInjJJkoWb9sWou7fJ4TpgOS4Dg47rCEj3VJIaWR[FCgcBtCF91lNXJ2GoDjVCyu33QBUr5rrMiCaMfztHfjhFuVWOYS5Ncoam2XPjqXjI59cuimsKCOhbYOUR6OigqvnZZTs1GKIvD[5kaINE6oEN3KUrZbSjPNuwmyzFHzH2e8UDzt1cywrFTFinsatWrKs0TPz27o575wzhr8OqVI74cUX4NWQKvQ7OvUH3PY4Vm8Vp[QfhrYKgLSsB6kUvngbEV97SK15Eohnms6JVxihirFk6szxTmo2HUrhwO8Lrkb6jq4KpQXDyxIxPuQ8iv7YQ0Rvoa2NKMFfJdMu[nIqm3kqNX4WTkRiSK7TwwYWMHscHDeqgijze0CJPjPAjFjPnKB60uksm5LhUwPddeKBu5Ap3zqhACCm1Ft4h7HKZmpXRmkOpL9[aFz622frOHipN1uCZUkc6H4ShfGwAhmhkh5xERYCmhg0heQcjqxhzH4z1ENKx7yXg1CarMhHJbG6AZ5Fxooua5qDtcFywwSxAq[NP68bqrKKN0Y8As2aSoXsxf3jrQSzAqPDf5aHGiZtU6CybEJhZMGHqgfO0MCxbaJCh4oX4EU8Pd5OTDU2CLrrdLyI9hl0nSYX2[CxA85jk0tCFfq3xNjW6T0AKQEvLF6lzSKdW5AIlte00mntgEACoYewJVJlF0gkKkMEoMx6Z2yfrSHsHeWMmgYqaq06N6E6icgu[lVndffKumHMb5SmB6RiKLFEx8pcFZB8UB8QBNqF5vFEnnOhNX5ANbeEJpkmRcby0n6PCPMPt9n26tXnXP2DdoI2s7bjIHMVBqJ[0EQKyAsSgTkY8viJRK2tIAv2oEAefUCppzIAfUxv6m8LOtdCeUxKAaq3YP7PAK6WnuV6tqxsVALakpJDdBGLOr2O1eARlYP4Ay[B8fuSEBjic1d6AqrynaRSeapAGyCZWhxIgfdm3BisHjetLql8niAjGGCGxwev8nyWSrOesZ6BxJF39kYPVd4FETJ3jkwws2LA7[XELtit6mDsWZNp4l0QyoLgbatQf4UtpAlxoKrVfuIgJCQyrK6gTpSBAfEi1oRW7fEEAix2sv0cE6NtJAB1ay4FkZ0raax683bM[GSlfBSq9CDL2p5ZVSmzaJVPvvPrvxs9HeG4nymgPWdlMOYOx2aasuUDgaOV8uj2DToKR5iL2qKuWsq1W15kxR2vmdqxtprjMsG(HHISwKApKx0LBkMwsxKF51ge0a8ABSJ8A1sneAUNBP3IjY00lslIw3kEcbun7IOwnM996HNxDBzU2YPWcCzAJJLn7HeCz4aBBK[73HDKpxlXZFR9wrx2v09WIrOJi8hS59DwS0g1wQLbF0YLsAlYHDS8TijiXezqlPnkUsXLo0cY6vaETHH7ZTK4fsMPUNrR6dF1y(yFIQrX1JlXOywhY3jFdpdotsWHR03HXQpzbQaFTuJfMmhkngtIxAN6DDcFVT03nyF5SMN4D6npkbsWlBSzY1ac4E1bnvxFtTKG'
# literal = '<{[(abc)]}>'
# literal = '<>()'
# literal = '<{[(abc>}])'
# ln = filter(Abc.filter_brackets, list(literal))
# search(ln)
# ----------
# Input
# ----------
n = int(raw_input())
lines = []
for i in xrange(n):
    line = filter(Abc.filter_brackets, list(raw_input()))
    lines.append("".join(line))
for i in xrange(n):
    try:
        ln = filter(Abc.filter_brackets, list(lines[i]))
        search(ln)
        print "true"
    except:
        print "false"
