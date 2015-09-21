from espresso.main import config
from espresso.main import robot

if 'daemonized' in config:
    if config['daemonized']:
    	import daemon
        with daemon.DaemonContext():
            robot.brew()

robot.brew()
