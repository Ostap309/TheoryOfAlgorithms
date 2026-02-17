import sys
from collections import defaultdict

names_dict = defaultdict(int)
people = []
for person in sys.stdin:
    people.append(person.strip())

    name = people[-1].split()[1]

    names_dict[name] += 1

print('\n'.join([f"{person} {names_dict[person.split()[1]]}" for person in people]))
