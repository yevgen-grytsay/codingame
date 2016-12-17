import re

# https://www.codingame.com/training/community/cards-castle/solution?id=5363833

castle = [raw_input() for i in range(input())]
unstable = any(re.search(r"\.\\|/\.|\\\\|//", r) for r in castle) or \
    any(re.search(r"\\\.|/\.|\\\\|//", "".join(v)) for v in zip(*castle))
print("UNSTABLE" if unstable else "STABLE")