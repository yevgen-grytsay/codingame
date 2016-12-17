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
    for ind in reversed(indexes):
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


def reduce_brackets(chars):
    result = []
    while len(chars) > 1:
        a = chars.pop(0)
        b = chars[0]
        if Abc.is_same(a, b):
            chars.pop(0)
        else:
            result.append(a)

    if len(chars) == 1:
        result.append(chars[0])

    return result

# literal = '[[[(])'
# literal = 'GhkbuzCI10Y<HB>8JG43ZYTbO9OPfeSZRAbmyfYe>gKEc<M}jT{4Z4s9Ujp5OCqJOSS5}}3Ah8Elb7InaepQxzSSFkyZCD6v7cq0[z]6hcN2>DPi2qOGrdDbcW4ZB>ugXtvZZlac>0RvTK0zQu0]j)rDQ9woKPbGShXT]KycP3Qt5i4I5[5pxcQ6alM4u(jpxmdGA7Ste8ROnHOy3n}UQG0M8VldiPl9sd3xSAgZISrZQkavYTm{lXXkR0Quw)EYD3uf8TFCbyQ0JZiC2TJoAKggNHki7dzKejCRNie1tfywZKiDWWVfOte2EqtdKxkK8q)OY94X72tt8q(yDIhP3)DYqg70cO[2bWnlRHUzfV9nvXChZIJzp90ICv<9y5ApOUDo]OiytI[O2kwREjb]bYg[TwmArlgkfhuyGycOsurvjYoNLImC8H]wCKhmP4aPY9hnUrWC58C8zX3J0Hdau8wDJOekS8QN7pjT[hU6ArSnpycm8uMJhtuTxZqVuRaLQ2YU4iSa8nkT7>U((BXBaHA]d[ar9mHa2tHpogfvdbxo2ltP>>nPIqKZE8SK9tEzM9W6NUizB3A7gPFelKzAhGjJUqwqtJ1ug)JnFFFJYnZuz2ZVT(p8hMl4yg7exJr6zP<mx>vTiDHZhL<]CQ4OG6N3w0suWMEdyUFt70hf2jcfD2dCCG]G3E21uPD0PfDAK<ETc842WMlQ{(DuTDCqVV5zPYGQzwGOj9(F4bDDiiWqae7QN4n8MYnUjMrDNCn6BAVxsf51GJFB)LMimEFgu2]axvukJkfIljsmryLKWCaLYlQO[McS9(6sw4neTawktu{nqG6QArQiwD4XVo>z0JUdz0qLjZ8VASFi>>kv)M5FRREaErBBG2v0nbYAEbYCEzuxYuVAL31FyUC(v3E6Sp(ZPgIt][Vr9XF[OV[dcUkbeEd[oJUsEgW[9Bm8qHsRL5gSWkegfxV1cDYVF6z8yXvMr)e2v((m1XRt)34sjiTwoxWnkrPu>iFpYvAvSWVommXM3fVYwmZjhdl8loFkH9>d6G6bpfI73ZMaRyQYbTVke)7j1DSzev9kNY(D)xx]nMVq5rWRmrXac3e1ITiLF6p]1or02Gc01Z6FSQR)E6u6RZP(MyEnwE2q6QDSe(xaKaM(Yi3pgTDt)K5oK51pJ4VFf9JE5O0M7QZGx218FmnnOxh<)tGB7(s3UFn>va3cKTnJzUYYIt<IzrTbqJBvl>POWXDkiieZeG7ewoFNzXpy4czNXlcusItGShw7vQZO5y7>[PLiOEKG38l]SiekkcOts>QodmfyzRSwUsWkjbYOEUBST)>giuJ]WMtYyetR51Cvaq3Ovk2o4kicN>VPPvzR3Alny7pcUw>TI[2ii55JbUigGHT>GmO1M2ROeVqH1b9ZDhuMXdeLXNgCpiRYv4dtPuq4VjN56ffjIJm2eIKvz';
# literal = 'pry7bJf6ustlbh}BRnKkF6r(ej(BsGw}IUW7sj9MzpvmDW9jiroLLsoJKcKC[JrK0TMYkK1TCCQNzihgpK6wkMlRWNEX2)0npwazEm7StfYjJgN81VWFAtN(ha5}rPKK}jtrUOIXg86GAiJKb0DQ]Ags0wydkajXAQSFZjcY1SYCKl]S5177{4GMFHVI9gwu3HquvFs4mkWysLMF9KMGj35D8CsbqMejPxaQ67lC1}EqjFGL0fbSdXUA0VEeogOqs7mUtcyJc1h}xZVdhRQr8JQ{hnLMHwUrUHwFLKwI2wdJrndBajEVHfhahT8UQg7XWiJL8]JbHcT96SXkL2TGsz8Z0ClZ4tThDY)GTcgBeFWHo8MBz<Ttbaidi7}NLQDh81vsjyPVcRUfS9{>iido2WUCnZFeDH54CONFpZ7EgkPapLdR7N2zfhMLutOhgeLIQEYujs4PFxmPyYHtgNYFq9WOdmJe>9Y4naTMXINwa<3f0dC0pahzpvt{TU53L1nhkd6PulnKLDVSXBg3V13w2ph0Ww54AZvFhdleuyEc9cueWy<stlkrxTUt3X5>QekeMb7eayeqRLoCmX8Op6rj9nTteod8TwIOFpzH{W01UlJrilKfn72BFEooqWfEhIhhmK5lQPLnHZ072IzRX}f8Ke848h7S8ntN0Bjl5KXyyhFwyHa}SKpPzsuDG5GPvczesuw2lG4GOnZvOLFJQczCNN836spub[Tccn]GuB}GWzXiYG0ZWaJN7]1RmpGnUlI2Jb7EN20noccaeqaG5hAEab8FMCoUUBggu8TTfiV[h3q4ZE5wqmu9TJoUZV4C4SL{MenIuRnPV6w>7o76gdkxqvqS3ngJbkn2ba1zd3IGyG<zIJYYn4EyEDk1)ceMLcIGxs9vGu937xojcKj5ztabeu9BHuj9(Fv5aIP3AIoXeiOqm)A)nZhcg>uEIBcR1Ui7GybBJgcbrSiJKj>[jXbyMXFk2Wv6xogZvFbhcUDEZ>jFjtmTahe8uArPWZwc6R3OH4tLa6QL<oMYRKfpYitYcTAZOau0sq[EEbSjQVt4DfJ53PGSAayszCnePOxsEVxcEwfv8B0c1PNvWpZopDeFMs0NlpJW<c>e55oimnifiahd)3fOGz6myRnZrjgXvb9mzIBKeCR93n9zjcNnQKwiMycMoeS8R3zRYv0a1UrLDPd8RkWgjR9JmXdNoQB76J{w3R5IpOj56VbKpF0zqutc8mNGq7P}ftUz}CbAvZ>zVaXZ31ab5jG3hB1wZSHS<3GLeSGRWkWVt2c0z7Rcse9R36v2ST0P}8IdYAsmxf5Q26x6K5Hrt}}b6B3Fv(InRPgMc7wbqVNOVid2U0wI2nf59sl2EnFVK3LxU33wW2IwskxDnQE5XjaJbOSyWw)Ozyn0z6S4foXGX'
# literal = 'g9UeXKMJaH2Jzr3TvZz4gKh4koqa6N]1ZT8lxTEG2avAzqc44I2g0Unk4lQ04GLWNSIPUB0SLnqkAZxnKMSPwWfNpMiAvB8aneiG]uQaSMlKXEXI8JiIMn[0KVaNYfFUDHPVkbhkqCXKGX0Sbk4QbW1AN[QadwOPsHNZNNgu47dlz0xNnHSyfD[bVqTFZamddOhbdoHCEcaFC4D3bpt8WUPTZv9ohSt[7EYyjplSqAHvLx6A7w8Ks}O5A8bxP8GudGlFSbKi9ASb1eOqzOJXj03XqYun7H9[KnH7jJaWXJ]NThhfaJVOLEYVR{F8m8J1fVO7AySiMkrio0xElNPlKIYRwAnuakoSyi]KRP]pRDACVdAzfxJO]zwzANwJg2cu1WXN<PgDQcUdb<Ju6xcaBrVTX4hjMW6lGBj8j}zXtbJeOcdaX7J8omuWckj6PyRXDnsX4y5W6SrrbH4n7mr90MSq3}3<bO9QJeGs0ZXKG4YA4T8}Xlna6jeddtYXstZExdojLN62fCQ9vqwnEVNwHtne2nQQS6940cUyj>CuUAaYhvV<1Bnffhh6bvqb0WTk6OJR88PrcgJolMkO4etVSPZ1SDK9VX5zf}y<vOvwuuChQJcZYyBYPVUwfhMaZcpviYYyYDaD}S4DheTudFP4FT7KWMfkMhtNa6TzlYBi7Yc(j7humLHG1PkqJOt73IzL4ywRvaBCRECeG)GaxrPh{ekW9whxA12tY}YSHhcgNNmZ2pZuFmpZ92AC9nfNNE35VEq1uih77yYlEb6L0Wl4Arr8BlbnHL2U4Aiwjfc{JgFEARotsnXJ1jaVUruzQyq)qde4RE9GFzPavevMrLaKVurp9x6rvbjBS4hXR3S7FPO9ERrqpdTGxHcxFyOCnxVQLqkGwO8VYZnP)xQEtm97c8hESCNqOUg8uO0geHesoHYw2A6k7GBHWFrP0WSWB1ZfCVyQBDzJMcgNok5qJzSTC9X3VLnIv<NY1M}KDq7i{vGBkD5P5KD2AsVKpPs3g3wkeqwK2KLlbsCzsZ56woVEkNjApSOhjd7yvQAO{TZZU04lBuyM0U[X4ssn15aZgZ]O7w8MzLxyvVwlbLsodeF0jF6RtR6{XVwaBSQk8EokxVAFDcv3Ks9kwOfvBVg{KSdUduNPOHD70JAQUqocIsPuu52GN7YGrpjRfuee9THlBM}XXdOCZWKNdyH{8s(wKDr5)SI2K9kFs7WDN6kPFqjP0Q1bTnKhiSYiQFB6SZhfJZWHbHx}k1Rn5csGU3I7EgTBRVILG3andgHi8wDUD>v]M9NT8Um55HrYT2DSI1DMgsRsJqNwzuiNO30vJYarxn8q7u)05XVrVjmJHPaOER4YWKjWSQaUlnSwVBEquAD7(RHhE6LXpnJa)r)e035PE8p'
# literal = 'hocyG43uyh3mU2p9DSWFvanOerDvBdGpypCnga3Rv1jmkmfRDdH2eCT73DCYmvVEdGc2VpiYbCAtDT73RsmGe2YQMDZefxex0T[4vYERXKBtAsJAcEWq4IMW0ab8PBXsFK2IXfvIn3mOCkJ4lFIXOD0pjTkkEt7EhM05RxAnCP4iVf8arpLgl8Ls6aiWhU3iixfIk[k4VpRHvEh5RHRwpcnlhIIOGDDTjc8OVmwqfMZ76hVpWU2YLPKsF8FoZYl4hmI43sI7Yr5TFF7JRTif6Iy3MdedD6lH3YxP3y1u[u5wVfwsXg5CtFjCzLTAm79UZQAU1WLBg3JCFGYcMElUrUT7JH4UCgfR69MWGU0by8kcROI7Br8SRXWNOlUcxeG0Sv4FoPLVA3C[y1X3ljg1ge8VEAc7n7Ka0g0rOHLQZkTdTkYDQgSD8067E4t42IRvNUHIB9YVpqSotUq2fRIn2R1nyArHatDFcq08u2sD0DRkwh[va2dyDikyWV9IXgm8RTSXZTGVybMWWDV1EqpZkWZrwrmlyN3wwPtU1YaR0PHFiJ26mn2xvnvpVB0BfewOcDV0EjNVgtIl5lJt2[KNPGxIG0ucQget26S0WoKzvOwVF9zLG8mT6rS7q5fcC66qwE7oY27NWmNE0r0wg953rS31F8GwoYrVS0x50Ge7WX2DbAHY3cRL[cHqRnCAARri7lj9VPLidkTVnldJuVIYdCKanuJJMGzMyZZejvsEflBHjJ7HlkjjWsVvFMgKwoDRRbGlj1PFE8zv8oOUCAGZV7A[mxOVxoVdsuBRWXyMRUlbNyNhwKfeb8EUdugS8OPmP4fsB8F2nMLrHd1WYPCEQZBH3C3v5tod6BvQdaLKh1mBaCI6bDugnfCc6v[Cw5YQoGjdzuQpT6yrN6jRCo9AIGTftwfxfMCI3Qwo1SDkQKBstI9mecQ8tmInjJJkoWb9sWou7fJ4TpgOS4Dg47rCEj3VJIaWR[FCgcBtCF91lNXJ2GoDjVCyu33QBUr5rrMiCaMfztHfjhFuVWOYS5Ncoam2XPjqXjI59cuimsKCOhbYOUR6OigqvnZZTs1GKIvD[5kaINE6oEN3KUrZbSjPNuwmyzFHzH2e8UDzt1cywrFTFinsatWrKs0TPz27o575wzhr8OqVI74cUX4NWQKvQ7OvUH3PY4Vm8Vp[QfhrYKgLSsB6kUvngbEV97SK15Eohnms6JVxihirFk6szxTmo2HUrhwO8Lrkb6jq4KpQXDyxIxPuQ8iv7YQ0Rvoa2NKMFfJdMu[nIqm3kqNX4WTkRiSK7TwwYWMHscHDeqgijze0CJPjPAjFjPnKB60uksm5LhUwPddeKBu5Ap3zqhACCm1Ft4h7HKZmpXRmkOpL9[aFz622frOHipN1uCZUkc6H4ShfGwAhmhkh5xERYCmhg0heQcjqxhzH4z1ENKx7yXg1CarMhHJbG6AZ5Fxooua5qDtcFywwSxAq[NP68bqrKKN0Y8As2aSoXsxf3jrQSzAqPDf5aHGiZtU6CybEJhZMGHqgfO0MCxbaJCh4oX4EU8Pd5OTDU2CLrrdLyI9hl0nSYX2[CxA85jk0tCFfq3xNjW6T0AKQEvLF6lzSKdW5AIlte00mntgEACoYewJVJlF0gkKkMEoMx6Z2yfrSHsHeWMmgYqaq06N6E6icgu[lVndffKumHMb5SmB6RiKLFEx8pcFZB8UB8QBNqF5vFEnnOhNX5ANbeEJpkmRcby0n6PCPMPt9n26tXnXP2DdoI2s7bjIHMVBqJ[0EQKyAsSgTkY8viJRK2tIAv2oEAefUCppzIAfUxv6m8LOtdCeUxKAaq3YP7PAK6WnuV6tqxsVALakpJDdBGLOr2O1eARlYP4Ay[B8fuSEBjic1d6AqrynaRSeapAGyCZWhxIgfdm3BisHjetLql8niAjGGCGxwev8nyWSrOesZ6BxJF39kYPVd4FETJ3jkwws2LA7[XELtit6mDsWZNp4l0QyoLgbatQf4UtpAlxoKrVfuIgJCQyrK6gTpSBAfEi1oRW7fEEAix2sv0cE6NtJAB1ay4FkZ0raax683bM[GSlfBSq9CDL2p5ZVSmzaJVPvvPrvxs9HeG4nymgPWdlMOYOx2aasuUDgaOV8uj2DToKR5iL2qKuWsq1W15kxR2vmdqxtprjMsG(HHISwKApKx0LBkMwsxKF51ge0a8ABSJ8A1sneAUNBP3IjY00lslIw3kEcbun7IOwnM996HNxDBzU2YPWcCzAJJLn7HeCz4aBBK[73HDKpxlXZFR9wrx2v09WIrOJi8hS59DwS0g1wQLbF0YLsAlYHDS8TijiXezqlPnkUsXLo0cY6vaETHH7ZTK4fsMPUNrR6dF1y(yFIQrX1JlXOywhY3jFdpdotsWHR03HXQpzbQaFTuJfMmhkngtIxAN6DDcFVT03nyF5SMN4D6npkbsWlBSzY1ac4E1bnvxFtTKG'
# literal = '<{[(abc)]}>'
# literal = '<>()'
# literal = '<{[(abc>}])'
# ln = filter(Abc.filter_brackets, list(literal))
# ln = reduce_brackets(ln)
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
        ln = reduce_brackets(ln)
        search(ln)
        print "true"
    except:
        print "false"
