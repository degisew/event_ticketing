import socket
from config.settings.base import *  # noqa


INSTALLED_APPS += ['drf_spectacular', 'debug_toolbar']

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware",]


# Since we're in Docker, we do this to match the machine address of Docker
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
