import logging
import yaml

from bot import Espresso

config = yaml.load(file('botconfig.yaml', 'r'))

logging.basicConfig(level=getattr(logging, config['logging']['level']),
    format="%(levelname)s from %(filename)s at %(asctime)s | %(message)s")
logging.debug("config is %s", config)

robot = Espresso(config)
