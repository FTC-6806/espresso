import daemon

from espresso.main import config
from espresso.main import robot

if 'daemonized' in config:
    if config['daemonized']:
        with daemon.DaemonContext():
            robot.brew()

robot.brew()
