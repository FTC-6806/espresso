from argparse import ArgumentParser
import yaml

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Path to config file',
        metavar='path'
    )
    return parser.parse_args()

def main():
    args = parse_args()

if __name__ == '__main__':
    main()
