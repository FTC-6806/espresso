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

if __name__ == '__main__':
	args = parse_args()
	config = yaml.load(file(args.config or 'botconfig.yaml', 'r'))