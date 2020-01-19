import argparse
import sys
import os

from yaml import load, Loader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', help='Path to dvc stage file')
    parser.add_argument('--repo', help='Path to dvc repository')
    args = parser.parse_args()
    stage = args.stage
    repo = args.repo

    if not os.path.exists(stage):
        raise ValueError("File '{}' doesn't exist".format(stage))
    if not os.path.exists(repo):
        raise ValueError("File '{}' doesn't exist".format(repo))

    with open(stage, 'r') as f:
        content = load(f, Loader=Loader)
    outs = content['outs']
    count = 0
    for i in outs:
        md5sum = i['md5']
        outs_path = i['path']
        cache = i['cache']
        if not cache:
            continue
        path = os.path.join(repo, md5sum[0:2], md5sum[2:])
        if not os.path.exists(path):
            print("'{}': cached value '{}' not found in dvc remote".
                  format(outs_path, md5sum))
            count += 1

    if count:
        exit(1)


if __name__ == '__main__':
    main()
