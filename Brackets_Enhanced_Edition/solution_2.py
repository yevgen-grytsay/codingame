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
    initial_length = len(chars)
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

    if len(result) <> initial_length:
        result = reduce_brackets(result)

    return result

literal = 'lUWWud[b()DM7Pdki(pF8tUb3lSqnBjl97slQJxhbl)ADCEYJdGYcr7EXa2N1rJLCNxi08)8iETg)(GqiUT}NmpDo4NpDftn91ZNCy1wuW7XhSZaxdp5Hj4KizFVlb}Oz<phDlTtV3DsgxWpniyBp7BJ2jrOngeRsE4mfqI45csblQ<fQ1Xm60<KJHzRRqilKxjm8MmBb5ooL15jFi>keTtzW4fBSoWgCkum9DsM51]BZQ[Oxd)B0a(zDG1hxXaCj67SE8AyIN2nYZbhIAo2CEbxqx2fMIGhgU7DXNwsQB)HuxwBUkSWZI4Xt8v()SGH{aTNBHoFyHP5rjBfHnZTwIWF8lUOjQHGVA8{5Ni1xq3E1S6rSpJeTuodfrwih]jry7HSQnp1Ufhkr9SZ4VhA7o0xKPj]3Zh6kd]03XLKZAEXxvRbhmzeHVqox1xW2Bo]6]C2DEajmDBime>lThGDnlFa55Vs0mM8LvxTYnXvRmTCYRu17ZNMvKfuGueVTFCk]Vqt<DtHOdhwf3HmmjdINueDTwb7pQABfwS1WNnJE1Oxi5Fl<witt7oY[6nhLf0ZqbhAo4JBYFGzpJRtL]E5bn4sXqkvTPC2ZQSfVL0oOB1mjP1LwrjT0t<6iepaspP4Y9TLM8EpJMIH2IrfaB2t)SJNHP)2)L3Ugyedv3g6sROPCkKgHZqiVmQwwjt(HDJpW7PeL7unpIabVtciktGlCal3p<VkC30nldY22kQO0IftfUEfTlAl3tI4u3w6Kt9KF1mt2Ywop{4m6p2CxBOO58G0rlxQtxckiORNy(2Dd2mw9C8h1LjJ{NWpKMzQcouG9phYyQ9lW1}TDIfWtfVsp5E)UZ9OcijZ1zwp32LzWY66x4u5rwgr}T3b41JCsavoH9w5[YWCKFnoyXpSOwyrYLiO5PJYUpllEmqWy2UNbiGHWXlo]d057Po][ZjzoxDQBrEyLy1v3sPZXn0cH2BC7wt73Zc4807g34KHSBMaq9vuS8l6QFAGqZcrhCgLx5LrEqLNUPmpum6lFnc4TqqVDTVOk7SiS9C]QCW]XARC0HaWOA7ng7RXmJn[jkT]cTrtO5IsqdbcQT1hJ8Dhg5owGkljdWdwl3oLyxfhuK]]sN4tqI4KwQMp8LG)G31VXXUpSxq0Gv3yv(80PYXmp9fM3fVD}86iBPJt}FcvEEsvIr}ax<mTc5IdSfM4QTdaWD<sBnN3vmQvo0wsmC}7TK[V5ErFhiUbzXeuMUMi5hhMj0yVMLlvxMLIvWXhgygr816foGHqe]Qblyvw(sF9g)5uSZU3uL(Id)VQLGPr[s9nNy6YFWeJckTdwldO[RjdtG1lIxDt5FVPxriqpaU(Fdb(}Ma4Dn9DBf{ui]ClVsDEYN6guV0ePHfhbkmdOEgRxjhOGOx6>gD1HHie1skTZgY>DckOs8HHllyDlj0RlnygQ(prxEOFQYMyYw(xC3EkMd1XPf3q2NpqIfvbYUmue1mQ(toRRHhKJFgIMEspA2uP24Tpoq)s1ENFP65Dhjpi4CRqqI9tOBfccGhvVpH2nZ8h5pQf3wCefrtostYaF4L0Frx12pl}M8zWGm{TDS83eHpAjb8zfnH1QhjAgEQzjlHlgPbFltGAaerl8XseYVARpUVw>NN4g1q]cNwzK3eEhlFIXKL8f8hekR2wT[D7dV4NuW<sANhKWquhvnDq<bzfqQw2ktt0OeLVdrg5yfETGIYKVZDl9bSdcdIf}5WkjGNiCylmLZdFyKHluzYsWCPU9{tW4d1}UuKe6ExJLSHW3lYMpgDzSZCaC8dTJ6ff6Kjmvqq4vQZQRi4wH{S9>JC2CRrqQHxAHMlDp<CBP7vLIYPp>n<audq26CmBQbBT9sE<AEv6FvwQ)0FeWVupBjM2Fe14bdFOr2x73qC(hpV}F10yMzqQbSTRyzW5ZLbdzk1pE}HTApl(8PbzX54IaDF]iS[XIBsBElxFdrCcWo11lbt(kirRHAXTfsP83bF3Ris3Wzw5wgE8Rii2HKo1G8)482vSQ55fLr3Ny9eT0qJagrpU74kxJduciFOAO0OBRubTDJltxED29wH4GXJRh1Z>DucamZEH0ncWxR4OEiCDyl]taLrjeXEiO7qv9ITTS[auejyI7GaNdeU<9zFwuO72r[bPrFYZ]J(Kz3YstelyM8Fad7DCqi0bibUAWSx9Dk0R)QpiOxNn7x7FIn3TMBvM2WflPBWP}neu2BP5KyJemhx2x1kJQrey9vxXT7R3KlujzzxmMt{TmhKX0R6c7m99(C2n1P9ZwZ58)lxOwKbzZt8KAiGH2E1UbfKzUpC3L>l]N7dyRDu2xuWtzyX9Nzg]3mof<ymXPYvEO<Fkk0VPiw5ACei<qhO3caVkBIk1rsOKEsg6wR3sJ}KDeAnFCOK6LKJ5SClUGpZnNeIuhFDfCXwmrUEuVu6b]tBFjjocSQ5[vPXX9a0Gk6qrBMGCbKCUxLsP9tK<v<(m1df(baYNi7(BJ(sbcrlLtOi80Mk6gpT3nh3ltUKDrQLuO{eLhRVo173akSKaF{A3[bwsakm3n[bGw13{NFdE1IjxZgWWzupjsch<<IE5GcNPKyhdMaBjLOembAFnqpmyEv2XAyu[Y](ir<E)wGEBVj2WIOhnZF12)03vgKzRHcu7RXSUqw9HrhMiXQ7mOQPGgHbwkLl2dAfK4)jGFLh[A2lab2TBHPWR1gIDUwkuzDbDDYtEZ09]RXQlevctkF3KZG9QdxMbg4MzmqhIdUPj48ckokqlgdmbysn4(jfunixdGZZ7lq6lgIoc9TDkXsrNQcknaZK6Joc331()TCMQ7IMp24ltehAz3Jak)mDuVD)NZn8OgrHMnNXJM6gC)QU4KMy)k5rA28QJ65>Uban68uJurOS7EEjZ0RpTjli2yH8WJ4ZmYLwrA4ZhCRkSYdNmWPgLRTQvPIxmT4oOYQMGs)n>j>S7UmIHW}I{XQBxj>>fSEkhvJiLSyiVW6iXF)leRKcbVrlVNHP3T)HfiPND2vKEk7LkqpcWGbfKJj8YaOuSETg9TxWLYkMUBN4uoGKJ0FXlKQHtL7S2y7qR7Oej>qfS<o5>RMJgX>8tTBaomQynCSHn)m7lbcENoRzvEIrtaiBN]PExxHxswcsZ1mDLhCyA]QUgbd2}E5iDO4yZVoWgh7vDp)Ru6LAQcmq8beRgm4hnRIceGyPhB26a(sp8MBnHbbPvepLo3<5k{9u1NVj{dHjcUVwb9y<kbXAVaRLjLsTQhk6xYh7vPgmwn2EHVoaqBW44H5s5qLLtFe7BdzZfDMTaPoM5QQgC7NBTgYdX>NZ5yy86WogxFuUQwabEg(my0G(A9eIsOiMuPRmFFAB8dugQUKC3lh3fJ3VRg7NMWXfQFALSyVNm4dDrA<aZ][9uOGT<Hvuojv9gMX1p9msjQF8LYSpQfMkyknXOyUF(fbZYkinNmh)zyWl)Mi0GC1KzJF3UN4Gw)tXjBgOeaVE1tQ6u5RVU><9adV>s8WFAIzv4jCUuaDPlAVoUWpJrGnLA0<STVlQnkbqf2DW6aOhsfcco<PO93QjhsXSJjWIsGs13p3KD2<68da0PGT}GjO9hCZdNB8dE8OYP1<N3zyrjdX3>s7n0THmDEwJ>05x9HZtT2U6pFM47uwRRkHSWJ9rmedbgQwtq<6bO42p6E46Hn8Ga31>UYCpIm<c0jKifbGAHoSdIAqjqUIVsq36E1lB21avr9beY4Nms6Vn78CKExs(JOVoP(BrTpreuXYE{PcPu7VRDsTVcqZF}Q{h8az[q[LBO1{amw3jRMx0FEeWlHlNHjFHONgDO{D>HjWzu16uBXrDiVnBv5PcJIlKycSI0bdjguKgp712MlNuOh1MXar7vmRjWRDnxReV4zPgXni>ZyaXJ(4iYJ0(Rj833ZGOilPrYELV)7AreUWTSUE3Ji3xQJSVVdmkcSceO4WcytzBFbuiPnmWIHkaPUj2jIHhjlzx67D>443wp{6ZXdcJS4UAOsyv4cQGuTGvfQO{WWYIk2t6znzPAgyrfa25bYaa7P7vIZ}A8{OdbChvxSeXKG3oX7L1fD<i2GG5Tu8JfOwlrP1NFeAnN2OR50nYpwh3zFOKV}WLAJF9nCENid6m}B}686VFjR)bhlOuWgRRF9ae){qrxPFwzs}xbI2ok15wGY3iuAIAqEJUgg{{TquiKEuvaUvKEC6nP}SQTLES{WRZ7kixClf5iEC9nutkTrbH<yekW6B><hu9<dS<U1E}ENY3mkycLrbKC3VqRaTS5{MnF3aTdcfKLPOCNi6rDyT4XSEfwRP3v0GsPH[6Ny3NRndXF5uIF5c]qd6DcE}BM99j2UB4caH2Fz7namdyebyKxfEDcFwdB4wqtPoQ0RuNfuTXV{4QIiSU>80vhgGb<4SIh7>pR8jhSM3A1vxUoIF9YQ)8PzjIYaXPBpKbPH)Cz0qwd6M4jhQ7SO0MRGnKLulhWWGSnu14Rl}hIZUZF1ulZmxsfeO[5tYXy4xbW5AOxwVgkENjKxBV1NWVUQ2hsD6fJgfkkwIvdZWrukQgIMf6XpxzIls0[4sK7NDsS1WTh0rXAxPJRhVAnYXqCv8BdTiqCdr(3Cms3vCNRibSL8LTjrYS7m5KHvNfSc(5pOQe7vQSFt9LXz3s4)1oez}pjDfC77Xco77W4pMHeMx3YDa4BtCrXnbLOGHBynLVJV5awZF6tWeReIkIekMHWDB4h}iJdVIJWvmmVarZM)Vjtdh4pfxWvHPQI(kqvMi<3bH33yoBDA1QSxlYbDmmaYJA2d8U33O5tmxHM1bWNR1kP3WnA6FswFbVz4S3m4DTeUJP6wuHWW0NhPS0CDIMYDqqmABh>nREoe7KdB89vp6P>FEn3o}RxSEwkP5ro0dhIft4WPoFGSQghkt}J>zZHVrIRB)CGvR[Ab1XvGp[XceGNwLcPbYxymfF6WwwVkxhyJJFZWk0mNWzQM0FhpGwRlhuiGYNCqcBwy)Ep2SUp681fH5LDrJblcnBGXiexKjX2k01vNyFiUXkG(Lb)cHQh7{XlVl8mKZ0vnTTCTA4a1J}ijyUWcvxF3mVdomGRD<GuLrUMw3AfWjzLURUrDU1QyLJvpLK3fqnsvGwktYQEtn5GdeYa}D3k4tcuD7<>ALBW60UtUpzmmrxVzg10VGc22s56VV9w8SIHaQGY84iFa{LXKF6ELSmRcXZvavjJSHOOO{L3CH4TpwANRrlbI]XAUiln1iFyu[I6otSmZ2uXZ16ryb<uS2>rYP{ptStuE1}PdCdN<AjKlKEbIoPmaYhZLHL>f2VoK<MUyozMI(xuPppnX6R8u72eMgSMhRm9jrJ1JfQ8)Us0gb7O61LePIALz9hWgldCe4cXH}JkW3UAyA}0w[nV5d9fXIA]IoI3aaBDqUBT{gfMuzCtBMv1Ks4p5jgNM71cA2je5pYQBS9DdH9IbKMKOBDwEMjlFRNvv8LObNkLr}URBKuPfMkqakgYUe7qx8[bqFBu1R[XgH0CkIrzvNEZ67mmNbez6EbxQs971cmWewm7{4SL{HvyCw2PJd[r1uN(eu4cu5kIU14vqZ3lLjmGMsZuEbwdPQvKbrOTajBKLoSJkc15hWxNjWFzKqCOPSW4pQXlfwGT2jeOONy9UnyuOEF(K6A[RKl(orfnLn00PaJbs4Vc33k3dQCcyHcazHxVzom8TYC7tKpj(EkkhSBJ8zwpgm6RUwro9YqAoRE)>pP[6[5j9g36cq5BybdhAxFGC8eZTfBnsICPtl>UyH3J1ejRRG1)]2DjLC8x]2dOi81eQa]xbCdCFD3mikPBtxIryEjiCFVr8JBYhwTTm01L4feXUZ7qBXDqyb6rRwP]P3573SM8NYZ9rU4Ko4bGPRbjqfgXmuPf{oGKKgplhmdIH{FeuGcCzxT><LFG1Vj(Rws1a(O5z7cbsI6BGAFPYpbUaIEI9U4qA9GCEvWspgf5]OXYYI0oZckLultDmD8R]rGGaYdcBIj380kCKRdKsl77UZK7VSGeebFoFNawE8mQPV8FWY3HU9jkM1boGKa{9libt4Y}hOKIzDv7eJ{9yVXocmdbBW3208TBbEKwBCsb)5dso(LwIoW{30QRaYteiamgLGUWvYpoRX4lkH09n1kYpwuOomjo03VI[hlevrWZfGsmSotiEpqolh[jZo0wO3QAalo7Eehd0T>EgsoyUXjZ2cckGSgJHAK86Y8QzsvY3ahF>4zu5sGlmt0n8xHktLhfiYOtDqx6K1sFJJl<IiUR3k6wNyfei5ASdO5{KPfKhYWZ0LLmtg4IWB9E0EqRpigCZLV0QN8WUHnxuW2EhMKR8odPpa75yn6{qAYZtfwFWQGFeIG3u6{OcUZRdtSmrUeStrHqTZHdyhQlopd2hZt}94HrHLoK6N4Sxm4lm<RqgEmgh6F6SyR55RN6rdWJF8V88pbFYrwk4Zdb(bo)MI9HUPrUdqBfc7qoTPF9r[a0Shpu3Czz7vRuro1Gx1m]tUTYfJrc4am<CX9RpbAt4ZXTsV6OOCUgaMhczWZqccSc3Pshd9iV2YNV>ShW492kCgMoXYoQf<uID7gQJALrfdUyM]yHk170Gln0laFUWjfJwV1jc2779d8Hg8S42m0<iP8fYIrGbCst0pyEoMZQzTBFrBRzofv9niMitG5gY]Rg6NBs4uNa[7L4RKyAlSk1dwqwM5pzwrgHdV80vPOdFsCm6R5qXCl1jXJQ4U7td<AG7SYKr0FR2Mm8gRu[6gOYEB8Xxu}I}V4Q4ON4yoy9jGqDovQpZwwSvnn2h<yonl7bwg12T666E[[tTQVzAqTXhP9NTF7p6uEtj5V5HBJ<KVBykdwmAcZsWIb8l95RmqO[CDoxBOHS]1Dd<pw3gSsfQQ>nVkR<nd9GxtpRqL)J1Q115U2RqdlzooevZgLY72GrhO38T75sWXmjwqKEZ5mKr07GG)TXxk93M(LgyqmxyIo(kmV9IgBnPFPye1W[HFXWgtRVJ2HInYZE1sY27MRXDrCHzMTH9x]gAfk3RP51kfbzFRSR0h2XgoKLK0N90gNz0NVBtag6iUBOcisDhCzwX42GXtf<pRywdd2sB>AcAqWhiCxXLijFqkM1etd2FgRdyspNKp]zbSiAUqU2FNf4BTZyjILFB5HKSo6ccta]xkFcM800Uk6rX)l(b68NfFivBftQbLRBO459mF>SnffmnRhty(}en}gUzZi9Bg5bhkbo2UV8Szl39IgXfsXDBev66qPyJC)(upFrLKv3f6kj2JK(Ky9kBwyd5KscE9ICaFYP1ylYfzRX0TDuoMVvp5bbvVK>11CESPe3BUvOFfDx3KLx7muOx1nMuKpR2WFzyR4dKBpBgmlGGLsKBehCHbbXTe1OJi2TqPZCViygEqOrFYIuOEb5LT)jBoXcsnDTF7YmK9mhVOB(TxkHxU92qqj{gI1<R9eAyVItTwio>I5FPsEIzTYX}ejLRUUx0a5fPx2stFsueGzZtYF8Oqy]YERFQNXc62vj0QUElqCCyn1EaCrv6GIeGpgN4JwWDsw]vi0GupE5LnPv(UOyEgCWSwvAKGGPn7m([Du2uF9Ub6swFc7KhG604L92[kUbjXigjK3idQVTpFpDDf0iR2c9oo3A8iD2AqjI4d]70OAxNTal12gRnrrbXmlBViCS2S6xJYf]hTm3vq0C9vQzDefWiVQ5pv5fGMV81eCaAkmV9qMX6a)7Hriw2aXgJW7vSynnyKHNyiK)3yMXX7eIu7EYaWvJ3yldNaAhOwbTy<Y1fLZNmQA1zkkz2cUkBUpkPaIrBNE2af4QAlgjSvhHoWAH<1b42cQOSeYJkbqfYKORgLUT5P5loscwF37ABJheRWV5Uro1YANGVsChwx2CpY6kqdd2btghXN3UZLlcquqou>FgVnmflLvc01vUYE36>(mRT1RjuD3wbwgwGnsZXKRAyALgc5s5EJDavpMD7eE33)LCRYdDLWPCZf]xrCPwwFF4WG1Z5fV[CNh9qSzyRJQa28UGn6LVxiRii23XxYAglOPQWsgwD4VEDXtwfiVb4fUoqL5KhcBQhsMY3AxqOTwcc1D8qJuPzl3Jrj1dus2GPJlM08kcfV7lAOacSmix1vgiN8kmgo4iCiTxCbs95uUXAKViUJ0SQfa2a6pejL7cCk1votpJLkso4FBywZoCp9xXJoaq46DsNABI2}UsT5sMK3}MIUJ4wDmXpoQ17uID08m1DxiOu4kWtJq7LEPkdSb7G8Dv3AH1qkXM]867BqgNnTjOYX62yt4VXi6KD5ymSon5SUuTcubj9aj(EErsN5MURllQ6Io6h1y5kwVq}87IBHP{2hfMPvB4z)eKDeAEREQ2NdCQDuN8XbrmTnks9Agv5e0gMDBg0GJGCUbcMoHPSb0KmfXVtRfB0>ljYsvcD7LzhjUJs>ST]FYFuElUSNaD9SPmSJnV59In7jgdbH8W8vDlFr1pXYgnrTGehUfC845fnF2Q2SsoZEiE]OUCYifffEKhqwnBddhwBqnK6w78ZjGc00etMjMzMqLaE7JnbN9DfzUp3P>eWF5Wf8MdpqEqQnnb{0x2onXE56W78m6XQmv37No1Gf25BiQ1k9XAdeMCc6sxpF3QJHH5L9}lvbjU0BE0UDrmJr9mvSk5ckILfTKzWA3qfbM18X[uS>70i7IB8lVxAVzWAnyNUJi8ird8IbQ2t1HhKe2wEhV<1kh{eJnHdkQyRPxWGjQS}V{UR}T6Lg4Kwn6{3rE49vJerEawTqdhfSSJNJIwiWk1Hkb5ZCM4RER11WNz5A04aIo5u}qFdxQtvbbU5pkCrNSzeHMVwseO[jCQIfAX)PjDdydhvPdh)276ihaHU4ljd<m0lxqd5kEmqA3pBT0adSX6qFk3mTtlbyhIcm4sxTsdwQKzhmm8OzVXEhQ1VlNcZjKpqHEVmlUe6vIYYc04r0W)nBTTWnTxOvkMGdfVQSmwZFNRD6s8h)dX)kqW6T67Pnh)KB<0M6v0O5eK9ELBLaJ3Jmpn9UaAeLZ0NFb]L5b2nG4hKhgbkLuGTfFLz2E8xQIvFPHZ1ELe[ADO]c[PaTgHX4rRI1dKAK(pdFSLaqAJiUWGlNrfno2(6J52bwJlDDl({kZc3fkllYD)SJ(uHvFPFNxQQWPTzyeFBArgNBxUN72IgxlY0iqQCaoolwnBB}wjW745U02olvXUzx2k1ZjUf5{Tij{Agt[i43QmuUZwI83KqEffjty}Rm{5qgZ1RqCDZfuykz4zZTmWDxGiNt{Jrslc6CpHovTLvjpC{Rl3b]5e4eHgkLhu}vOc7MvkXy0Ue24Pk{D0Kmj5Gs)kFoLJeLgsuLaE56lxh6uivX6U1nP5vs7>yVGWgmAhaEcuZSpXcORv6AAopa8xO6vH1a>VLM6F05qs>lg5CisDpm8>fZZXF7FwXvIgh9FeZm0Ojo49[0djDHa0Vy7zaqS3orV0ijx34WM3zmdLzZNjQoYrpKGmJRo5QDcBcbfMiSwVQUnbpnwO]4GPd35907wpd0N>qdoSuQxBluq9vISDmIJ3VAkfQytg31nKPwg}YNk1zEGK}GZFhD6AbxlRiY0]NjY9[cuFzaH74GP012Qz[yjhzh4EihqvYB50xGeWkSKYm<0jF8f1y8hBQbwSIrzYAg5lIxeWhKmDz4c4V<aBmprSIs0YmNKmFa5FrI5TTlIXlzOkCWWAic5U]XO[Y>SNb65N39xDwYzFI6mJc4ebqe0T1kCQNsei7iC<W9t9oycQtxZ]i8jbPSWEZ3IR1gpv}Upz650Vak<lnZh<D>YKt9gL22f47xnL846wmodPZeRnKtdyfA7yV5WXLSRzT2pm5m08a2B9nUk4kGEAsH5K7837z>9GGsNl6BdU49{7)Bikb4cVz2nQd)ugbcSwUrVBWLEsOAnxrmt[Dqbg[yRPzEj]8kveWxok>reay3fudfSCA3fSO2wIBvUjG507OsF)NE3jP9CpOzmJGMP0(o48FRECT8SUC<4A4'
# literal = '[[[(])'
# literal = 'GhkbuzCI10Y<HB>8JG43ZYTbO9OPfeSZRAbmyfYe>gKEc<M}jT{4Z4s9Ujp5OCqJOSS5}}3Ah8Elb7InaepQxzSSFkyZCD6v7cq0[z]6hcN2>DPi2qOGrdDbcW4ZB>ugXtvZZlac>0RvTK0zQu0]j)rDQ9woKPbGShXT]KycP3Qt5i4I5[5pxcQ6alM4u(jpxmdGA7Ste8ROnHOy3n}UQG0M8VldiPl9sd3xSAgZISrZQkavYTm{lXXkR0Quw)EYD3uf8TFCbyQ0JZiC2TJoAKggNHki7dzKejCRNie1tfywZKiDWWVfOte2EqtdKxkK8q)OY94X72tt8q(yDIhP3)DYqg70cO[2bWnlRHUzfV9nvXChZIJzp90ICv<9y5ApOUDo]OiytI[O2kwREjb]bYg[TwmArlgkfhuyGycOsurvjYoNLImC8H]wCKhmP4aPY9hnUrWC58C8zX3J0Hdau8wDJOekS8QN7pjT[hU6ArSnpycm8uMJhtuTxZqVuRaLQ2YU4iSa8nkT7>U((BXBaHA]d[ar9mHa2tHpogfvdbxo2ltP>>nPIqKZE8SK9tEzM9W6NUizB3A7gPFelKzAhGjJUqwqtJ1ug)JnFFFJYnZuz2ZVT(p8hMl4yg7exJr6zP<mx>vTiDHZhL<]CQ4OG6N3w0suWMEdyUFt70hf2jcfD2dCCG]G3E21uPD0PfDAK<ETc842WMlQ{(DuTDCqVV5zPYGQzwGOj9(F4bDDiiWqae7QN4n8MYnUjMrDNCn6BAVxsf51GJFB)LMimEFgu2]axvukJkfIljsmryLKWCaLYlQO[McS9(6sw4neTawktu{nqG6QArQiwD4XVo>z0JUdz0qLjZ8VASFi>>kv)M5FRREaErBBG2v0nbYAEbYCEzuxYuVAL31FyUC(v3E6Sp(ZPgIt][Vr9XF[OV[dcUkbeEd[oJUsEgW[9Bm8qHsRL5gSWkegfxV1cDYVF6z8yXvMr)e2v((m1XRt)34sjiTwoxWnkrPu>iFpYvAvSWVommXM3fVYwmZjhdl8loFkH9>d6G6bpfI73ZMaRyQYbTVke)7j1DSzev9kNY(D)xx]nMVq5rWRmrXac3e1ITiLF6p]1or02Gc01Z6FSQR)E6u6RZP(MyEnwE2q6QDSe(xaKaM(Yi3pgTDt)K5oK51pJ4VFf9JE5O0M7QZGx218FmnnOxh<)tGB7(s3UFn>va3cKTnJzUYYIt<IzrTbqJBvl>POWXDkiieZeG7ewoFNzXpy4czNXlcusItGShw7vQZO5y7>[PLiOEKG38l]SiekkcOts>QodmfyzRSwUsWkjbYOEUBST)>giuJ]WMtYyetR51Cvaq3Ovk2o4kicN>VPPvzR3Alny7pcUw>TI[2ii55JbUigGHT>GmO1M2ROeVqH1b9ZDhuMXdeLXNgCpiRYv4dtPuq4VjN56ffjIJm2eIKvz';
# literal = 'pry7bJf6ustlbh}BRnKkF6r(ej(BsGw}IUW7sj9MzpvmDW9jiroLLsoJKcKC[JrK0TMYkK1TCCQNzihgpK6wkMlRWNEX2)0npwazEm7StfYjJgN81VWFAtN(ha5}rPKK}jtrUOIXg86GAiJKb0DQ]Ags0wydkajXAQSFZjcY1SYCKl]S5177{4GMFHVI9gwu3HquvFs4mkWysLMF9KMGj35D8CsbqMejPxaQ67lC1}EqjFGL0fbSdXUA0VEeogOqs7mUtcyJc1h}xZVdhRQr8JQ{hnLMHwUrUHwFLKwI2wdJrndBajEVHfhahT8UQg7XWiJL8]JbHcT96SXkL2TGsz8Z0ClZ4tThDY)GTcgBeFWHo8MBz<Ttbaidi7}NLQDh81vsjyPVcRUfS9{>iido2WUCnZFeDH54CONFpZ7EgkPapLdR7N2zfhMLutOhgeLIQEYujs4PFxmPyYHtgNYFq9WOdmJe>9Y4naTMXINwa<3f0dC0pahzpvt{TU53L1nhkd6PulnKLDVSXBg3V13w2ph0Ww54AZvFhdleuyEc9cueWy<stlkrxTUt3X5>QekeMb7eayeqRLoCmX8Op6rj9nTteod8TwIOFpzH{W01UlJrilKfn72BFEooqWfEhIhhmK5lQPLnHZ072IzRX}f8Ke848h7S8ntN0Bjl5KXyyhFwyHa}SKpPzsuDG5GPvczesuw2lG4GOnZvOLFJQczCNN836spub[Tccn]GuB}GWzXiYG0ZWaJN7]1RmpGnUlI2Jb7EN20noccaeqaG5hAEab8FMCoUUBggu8TTfiV[h3q4ZE5wqmu9TJoUZV4C4SL{MenIuRnPV6w>7o76gdkxqvqS3ngJbkn2ba1zd3IGyG<zIJYYn4EyEDk1)ceMLcIGxs9vGu937xojcKj5ztabeu9BHuj9(Fv5aIP3AIoXeiOqm)A)nZhcg>uEIBcR1Ui7GybBJgcbrSiJKj>[jXbyMXFk2Wv6xogZvFbhcUDEZ>jFjtmTahe8uArPWZwc6R3OH4tLa6QL<oMYRKfpYitYcTAZOau0sq[EEbSjQVt4DfJ53PGSAayszCnePOxsEVxcEwfv8B0c1PNvWpZopDeFMs0NlpJW<c>e55oimnifiahd)3fOGz6myRnZrjgXvb9mzIBKeCR93n9zjcNnQKwiMycMoeS8R3zRYv0a1UrLDPd8RkWgjR9JmXdNoQB76J{w3R5IpOj56VbKpF0zqutc8mNGq7P}ftUz}CbAvZ>zVaXZ31ab5jG3hB1wZSHS<3GLeSGRWkWVt2c0z7Rcse9R36v2ST0P}8IdYAsmxf5Q26x6K5Hrt}}b6B3Fv(InRPgMc7wbqVNOVid2U0wI2nf59sl2EnFVK3LxU33wW2IwskxDnQE5XjaJbOSyWw)Ozyn0z6S4foXGX'
# literal = 'g9UeXKMJaH2Jzr3TvZz4gKh4koqa6N]1ZT8lxTEG2avAzqc44I2g0Unk4lQ04GLWNSIPUB0SLnqkAZxnKMSPwWfNpMiAvB8aneiG]uQaSMlKXEXI8JiIMn[0KVaNYfFUDHPVkbhkqCXKGX0Sbk4QbW1AN[QadwOPsHNZNNgu47dlz0xNnHSyfD[bVqTFZamddOhbdoHCEcaFC4D3bpt8WUPTZv9ohSt[7EYyjplSqAHvLx6A7w8Ks}O5A8bxP8GudGlFSbKi9ASb1eOqzOJXj03XqYun7H9[KnH7jJaWXJ]NThhfaJVOLEYVR{F8m8J1fVO7AySiMkrio0xElNPlKIYRwAnuakoSyi]KRP]pRDACVdAzfxJO]zwzANwJg2cu1WXN<PgDQcUdb<Ju6xcaBrVTX4hjMW6lGBj8j}zXtbJeOcdaX7J8omuWckj6PyRXDnsX4y5W6SrrbH4n7mr90MSq3}3<bO9QJeGs0ZXKG4YA4T8}Xlna6jeddtYXstZExdojLN62fCQ9vqwnEVNwHtne2nQQS6940cUyj>CuUAaYhvV<1Bnffhh6bvqb0WTk6OJR88PrcgJolMkO4etVSPZ1SDK9VX5zf}y<vOvwuuChQJcZYyBYPVUwfhMaZcpviYYyYDaD}S4DheTudFP4FT7KWMfkMhtNa6TzlYBi7Yc(j7humLHG1PkqJOt73IzL4ywRvaBCRECeG)GaxrPh{ekW9whxA12tY}YSHhcgNNmZ2pZuFmpZ92AC9nfNNE35VEq1uih77yYlEb6L0Wl4Arr8BlbnHL2U4Aiwjfc{JgFEARotsnXJ1jaVUruzQyq)qde4RE9GFzPavevMrLaKVurp9x6rvbjBS4hXR3S7FPO9ERrqpdTGxHcxFyOCnxVQLqkGwO8VYZnP)xQEtm97c8hESCNqOUg8uO0geHesoHYw2A6k7GBHWFrP0WSWB1ZfCVyQBDzJMcgNok5qJzSTC9X3VLnIv<NY1M}KDq7i{vGBkD5P5KD2AsVKpPs3g3wkeqwK2KLlbsCzsZ56woVEkNjApSOhjd7yvQAO{TZZU04lBuyM0U[X4ssn15aZgZ]O7w8MzLxyvVwlbLsodeF0jF6RtR6{XVwaBSQk8EokxVAFDcv3Ks9kwOfvBVg{KSdUduNPOHD70JAQUqocIsPuu52GN7YGrpjRfuee9THlBM}XXdOCZWKNdyH{8s(wKDr5)SI2K9kFs7WDN6kPFqjP0Q1bTnKhiSYiQFB6SZhfJZWHbHx}k1Rn5csGU3I7EgTBRVILG3andgHi8wDUD>v]M9NT8Um55HrYT2DSI1DMgsRsJqNwzuiNO30vJYarxn8q7u)05XVrVjmJHPaOER4YWKjWSQaUlnSwVBEquAD7(RHhE6LXpnJa)r)e035PE8p'
# literal = 'hocyG43uyh3mU2p9DSWFvanOerDvBdGpypCnga3Rv1jmkmfRDdH2eCT73DCYmvVEdGc2VpiYbCAtDT73RsmGe2YQMDZefxex0T[4vYERXKBtAsJAcEWq4IMW0ab8PBXsFK2IXfvIn3mOCkJ4lFIXOD0pjTkkEt7EhM05RxAnCP4iVf8arpLgl8Ls6aiWhU3iixfIk[k4VpRHvEh5RHRwpcnlhIIOGDDTjc8OVmwqfMZ76hVpWU2YLPKsF8FoZYl4hmI43sI7Yr5TFF7JRTif6Iy3MdedD6lH3YxP3y1u[u5wVfwsXg5CtFjCzLTAm79UZQAU1WLBg3JCFGYcMElUrUT7JH4UCgfR69MWGU0by8kcROI7Br8SRXWNOlUcxeG0Sv4FoPLVA3C[y1X3ljg1ge8VEAc7n7Ka0g0rOHLQZkTdTkYDQgSD8067E4t42IRvNUHIB9YVpqSotUq2fRIn2R1nyArHatDFcq08u2sD0DRkwh[va2dyDikyWV9IXgm8RTSXZTGVybMWWDV1EqpZkWZrwrmlyN3wwPtU1YaR0PHFiJ26mn2xvnvpVB0BfewOcDV0EjNVgtIl5lJt2[KNPGxIG0ucQget26S0WoKzvOwVF9zLG8mT6rS7q5fcC66qwE7oY27NWmNE0r0wg953rS31F8GwoYrVS0x50Ge7WX2DbAHY3cRL[cHqRnCAARri7lj9VPLidkTVnldJuVIYdCKanuJJMGzMyZZejvsEflBHjJ7HlkjjWsVvFMgKwoDRRbGlj1PFE8zv8oOUCAGZV7A[mxOVxoVdsuBRWXyMRUlbNyNhwKfeb8EUdugS8OPmP4fsB8F2nMLrHd1WYPCEQZBH3C3v5tod6BvQdaLKh1mBaCI6bDugnfCc6v[Cw5YQoGjdzuQpT6yrN6jRCo9AIGTftwfxfMCI3Qwo1SDkQKBstI9mecQ8tmInjJJkoWb9sWou7fJ4TpgOS4Dg47rCEj3VJIaWR[FCgcBtCF91lNXJ2GoDjVCyu33QBUr5rrMiCaMfztHfjhFuVWOYS5Ncoam2XPjqXjI59cuimsKCOhbYOUR6OigqvnZZTs1GKIvD[5kaINE6oEN3KUrZbSjPNuwmyzFHzH2e8UDzt1cywrFTFinsatWrKs0TPz27o575wzhr8OqVI74cUX4NWQKvQ7OvUH3PY4Vm8Vp[QfhrYKgLSsB6kUvngbEV97SK15Eohnms6JVxihirFk6szxTmo2HUrhwO8Lrkb6jq4KpQXDyxIxPuQ8iv7YQ0Rvoa2NKMFfJdMu[nIqm3kqNX4WTkRiSK7TwwYWMHscHDeqgijze0CJPjPAjFjPnKB60uksm5LhUwPddeKBu5Ap3zqhACCm1Ft4h7HKZmpXRmkOpL9[aFz622frOHipN1uCZUkc6H4ShfGwAhmhkh5xERYCmhg0heQcjqxhzH4z1ENKx7yXg1CarMhHJbG6AZ5Fxooua5qDtcFywwSxAq[NP68bqrKKN0Y8As2aSoXsxf3jrQSzAqPDf5aHGiZtU6CybEJhZMGHqgfO0MCxbaJCh4oX4EU8Pd5OTDU2CLrrdLyI9hl0nSYX2[CxA85jk0tCFfq3xNjW6T0AKQEvLF6lzSKdW5AIlte00mntgEACoYewJVJlF0gkKkMEoMx6Z2yfrSHsHeWMmgYqaq06N6E6icgu[lVndffKumHMb5SmB6RiKLFEx8pcFZB8UB8QBNqF5vFEnnOhNX5ANbeEJpkmRcby0n6PCPMPt9n26tXnXP2DdoI2s7bjIHMVBqJ[0EQKyAsSgTkY8viJRK2tIAv2oEAefUCppzIAfUxv6m8LOtdCeUxKAaq3YP7PAK6WnuV6tqxsVALakpJDdBGLOr2O1eARlYP4Ay[B8fuSEBjic1d6AqrynaRSeapAGyCZWhxIgfdm3BisHjetLql8niAjGGCGxwev8nyWSrOesZ6BxJF39kYPVd4FETJ3jkwws2LA7[XELtit6mDsWZNp4l0QyoLgbatQf4UtpAlxoKrVfuIgJCQyrK6gTpSBAfEi1oRW7fEEAix2sv0cE6NtJAB1ay4FkZ0raax683bM[GSlfBSq9CDL2p5ZVSmzaJVPvvPrvxs9HeG4nymgPWdlMOYOx2aasuUDgaOV8uj2DToKR5iL2qKuWsq1W15kxR2vmdqxtprjMsG(HHISwKApKx0LBkMwsxKF51ge0a8ABSJ8A1sneAUNBP3IjY00lslIw3kEcbun7IOwnM996HNxDBzU2YPWcCzAJJLn7HeCz4aBBK[73HDKpxlXZFR9wrx2v09WIrOJi8hS59DwS0g1wQLbF0YLsAlYHDS8TijiXezqlPnkUsXLo0cY6vaETHH7ZTK4fsMPUNrR6dF1y(yFIQrX1JlXOywhY3jFdpdotsWHR03HXQpzbQaFTuJfMmhkngtIxAN6DDcFVT03nyF5SMN4D6npkbsWlBSzY1ac4E1bnvxFtTKG'
# literal = '<{[(abc)]}>'
# literal = '<>()'
# literal = '<{[(abc>}])'
ln = filter(Abc.filter_brackets, list(literal))
ln = reduce_brackets(ln)
search(ln)
# ----------
# Input
# ----------
# n = int(raw_input())
# lines = []
# for i in xrange(n):
#     line = filter(Abc.filter_brackets, list(raw_input()))
#     lines.append("".join(line))
# for i in xrange(n):
#     try:
#         ln = filter(Abc.filter_brackets, list(lines[i]))
#         ln = reduce_brackets(ln)
#         search(ln)
#         print "true"
#     except:
#         print "false"
