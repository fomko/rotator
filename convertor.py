import re

suffixes = "","k","m","g","t"
multipliers = {'{}b'.format(l): 1024**i for i,l in enumerate(suffixes) }
sre = re.compile("(\d+)({})".format("|".join(x+"b" for x in suffixes)), re.IGNORECASE)


def subfunc(m):
    return str(int(m.group(1))*multipliers[m.group(2).lower()])


def convert_size_to_bytes(size):
    return sre.sub(subfunc, size)