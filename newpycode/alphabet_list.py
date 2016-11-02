from string import ascii_uppercase
import itertools

def iter_all_strings(size):
    # size = 1
    while size<=2:
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)
        # size +=1

for s in iter_all_strings(2):
    print (s)
    if s == 'AM':
        break

# for s in itertools.islice(iter_all_strings(), 54):
#     print (s)