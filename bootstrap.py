from git import Repo
import sys
from os import path

def main():
    url = 'https://github.com/ksgyeung/surveillance-pi.git'
    target = path.join(path.dirname(__name__), 'servenillance-pi')

    if path.exists(target):
        repo = Repo(target)
    else:
        repo = Repo.clone_from(url, target)

    origin = repo.remotes.origin
    origin.pull()

if __name__ == '__main__':
    main()