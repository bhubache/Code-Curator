from __future__ import annotations

import argparse
import subprocess

def main():
    args = parse_args()
    cwd = args.cwd
    align_cmd: list[str] = 'mfa align --clean input/ /home/brandon/Documents/MFA/pretrained_models/dictionary/english_us_arpa.dict english_us_arpa output'.split()

    subprocess.run(align_cmd, cwd=cwd)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cwd', required=True, type=str)

    return parser.parse_args()


if __name__ == '__main__':
    main()
