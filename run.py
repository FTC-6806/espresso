import daemon

from espresso.main import config
from espresso.main import robot

if config.has_key('daemonized'):
    if config['daemonized']:
        with daemon.DaemonContext():
            robot.brew()

robot.brew()
