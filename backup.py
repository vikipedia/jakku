import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import functools

print = functools.partial(print, flush=True)


def rsync_(*options, src=None, dest=None):
    cmd = " ".join(["rsync"] + list(options) + [src, dest])
    print(cmd)
    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)


def rsync(src, dest):
    return rsync_("-raz", src=src, dest=dest)


def backup():
    source_location = "/home/vikrant"
    target_location = "/media/vikrant/mozart-home"

    exceptions = ["Downloads", "Music"]
    sources_ = [item for item in os.listdir(
        source_location) if item not in exceptions]

    sources = [os.path.join(source_location, s) for s in sources_]
    destinations = [os.path.join(target_location, s) for s in sources_]

    with ThreadPoolExecutor(max_workers=7) as executor:
        for src, dest in zip(sources, destinations):
            executor.submit(rsync, src, dest)


if __name__ == "__main__":
    backup()
