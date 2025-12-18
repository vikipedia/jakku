import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait, ALL_COMPLETED
import functools

print = functools.partial(print, flush=True)


def rsync_(*options, src=None, dest=None):
    cmd = " ".join(["rsync"] + list(options) + [src, dest])
    print(cmd)

    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    return p.returncode


def rsync(src, dest):
    return rsync_("-raz --delete", src=src, dest=dest)


def backup():
    source_location = "/home/vikrant"
    target_location = "/media/vikrant/mozart-home"

    hidden_exceptions = ['.cache', ".mozilla"]
    exceptions = ["Downloads", "Music"] + hidden_exceptions
    sources_ = [item for item in os.listdir(
        source_location) if item not in exceptions]

    sources = [os.path.join(source_location, s) for s in sources_]
    destinations = [target_location for s in sources_]

    with ThreadPoolExecutor(max_workers=7) as executor:
        results = executor.map(rsync, sources, destinations)
    print("finish!")


if __name__ == "__main__":
    backup()
