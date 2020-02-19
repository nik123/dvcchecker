import argparse
import sys
import os

from yaml import load, Loader


def count_missing_outs_in_stage(stage, repo) -> int:
    with open(stage, "r") as f:
        content = load(f, Loader=Loader)
    outs = content["outs"]
    count = 0
    for i in outs:
        md5sum = i["md5"]
        outs_path = i["path"]
        cache = i["cache"]
        if not cache:
            continue
        path = os.path.join(repo, md5sum[0:2], md5sum[2:])
        if not os.path.exists(path):
            print(
                "'{}': cached value '{}' not found in dvc remote".format(
                    outs_path, md5sum
                )
            )

            count += 1

    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, help="Path to dvc stage file")
    parser.add_argument("--repo", required=True, help="Path to dvc repository")
    args = parser.parse_args()
    stage = args.stage
    repo = args.repo

    if not os.path.exists(stage):
        raise ValueError("File '{}' doesn't exist".format(stage))
    if not os.path.exists(repo):
        raise ValueError("File '{}' doesn't exist".format(repo))

    stage_count = 0
    count = 0

    if os.path.isdir(stage):
        for dirpath, _, filenames in os.walk(stage):
            for filename in filenames:
                _, ext = os.path.splitext(filename)
                if ext.lower() != '.dvc':
                    continue
                count += count_missing_outs_in_stage(
                    os.path.join(stage, dirpath, filename),
                    repo
                )
                stage_count += 1
    else:
        _, ext = os.path.splitext(stage)
        if ext.lower() != '.dvc':
            raise ValueError("'{}' is not a *.dvc file!".format(stage))

        count += count_missing_outs_in_stage(stage, repo)
        stage_count += 1

    if count:
        exit(1)
    else:
        print("Checked {} stage files. Everything is ok".format(stage_count))


if __name__ == "__main__":
    main()
