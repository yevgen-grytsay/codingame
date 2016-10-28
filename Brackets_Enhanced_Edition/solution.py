import functools
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


def search(chars, context, bracket_context=None, letter_context=None):
    while len(chars) > 0:
        c = chars.pop(0)
        if c.isalnum():
            letter_context = True
            continue

        if c in Abc.brackets:
            if bracket_context is None:
                bracket_context = Abc.to_opening(c)
                context.append(bracket_context)
                continue
            else:
                if Abc.is_same(bracket_context, c):
                    op = Abc.to_opening(c)
                    cs = Abc.flip(op)
                    c = first([
                        (op, functools.partial(search, chars[:], context[:] + [op], op, letter_context)),
                        (cs, functools.partial(search, chars[:], context[:-1], prev_context(context) or None, letter_context))
                    ])
                    if c == op:
                        bracket_context = c
                        context.append(c)
                    else:
                        bracket_context = prev_context(context)
                        context.pop()
                else:
                    bracket_context = Abc.to_opening(c)
                    context.append(bracket_context)
    if len(context) > 0:
        raise Exception("Wrong")
    return True


def prev_context(context):
    if len(context) > 1:
        return context[-2]
    return None


def first(tuples):
    result = []
    for ret, fnc in tuples:
        result.append(ret)
        try:
            fnc()
            return ret
        except:
            pass
    raise Exception("Not found: ")


literal = '<{[(abc)]}>'
search(list(literal), [])
