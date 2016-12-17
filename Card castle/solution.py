h = int(raw_input())
lines = []
for i in xrange(h):
    s = raw_input()
    lines.append(s)

castle = "\n".join(lines)
castle_rot = "\n".join(map(lambda t: "".join(t), zip(*lines)))
if '.\\' in castle \
        or '/.' in castle \
        or '//' in castle \
        or '\\\\' in castle \
        or '\.' in castle_rot \
        or '/.' in castle_rot \
        or '//' in castle_rot \
        or '\\\\' in castle_rot:
    print 'UNSTABLE'
else:
    print 'STABLE'
