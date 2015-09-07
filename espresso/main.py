from argparse import ArgumentParser
import yaml
import logging

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
    config = yaml.load(file(args.config or 'botconfig.yaml', 'r'))
    logging.basicConfig(level=getattr(logging, config['logging']['level']), format="%(levelname)s from %(filename)s at %(asctime)s | %(message)s")
    logging.debug(config)

if __name__ == '__main__':
    main()
