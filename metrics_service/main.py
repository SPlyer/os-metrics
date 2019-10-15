import logging

import daemon

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("/var/log/metrics_service.log")
logger.addHandler(fh)

context = daemon.DaemonContext(files_preserve=[fh.stream])

with context:
    pass