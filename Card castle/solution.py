h = int(raw_input())
lines = []
for i in xrange(h):
    s = raw_input()
    lines.append(s)

castle = "\n".join(lines)
castle_rot = "\n".join(map(lambda t: "".join(t), zip(*lines)))
if castle.find('.\\') > -1 \
        or castle.find('/.') > -1 \
        or castle.find('//') > -1 \
        or castle.find('\\\\') > -1 \
        or castle_rot.find('\.') > -1 \
        or castle_rot.find('/.') > -1 \
        or castle_rot.find('//') > -1 \
        or castle_rot.find('\\\\') > -1:
    print 'UNSTABLE'
else:
    print 'STABLE'
