import os
import time
import argparse

status = "git status"
add = "git add ."
commit = "git commit -m 'Automated save' "
push = "git push"


def has_changes():
    run = os.popen(status)
    for line in run.readlines():
        if line.find("Untracked") >= 0 or line.find("Changes not staged") >= 0:
            return True
    return False


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='timeout', type=int, default=120)
    args = parser.parse_args()
    return args.timeout


def save():
    os.popen(add)
    os.popen(commit)
    os.popen(push)


if __name__ == '__main__':
    tout = get_args() or 60

    while True:
        if has_changes():
            save()
        time.sleep(tout)
