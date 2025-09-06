"""A script to add words from given file to dictionary
"""
import sys


def words(*filenames):
    for filename in filenames:
        with open(filename) as f:
            for line in f:
                yield from line.split()


def unique(items):
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            yield item


def take(n, seq):
    return [next(seq) for i in range(n)]


def chunks(seq, n):
    try:
        while True:
            yield take(seq, n)
    except StopIteration as e:
        pass


def add_to_dictionary(dictfile, *inputfiles):
    with open(dictfile, "w") as d:
        for c in chunks(10, unique(words(*inputfiles))):
            d.write(" ".join(c))
            d.write("\n")


if __name__ == "__main__":
    dictfile = sys.argv[1]
    add_to_dictionary(dictfile, *sys.argv[2:])
