# import socket
from config.settings.base import *  # noqa F403

from config.settings.base import (
    INSTALLED_APPS,
    MIDDLEWARE,
    REST_FRAMEWORK,
    ALLOWED_HOSTS,
)

REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []

INSTALLED_APPS += [
    "drf_spectacular",
    "silk",
    # "debug_toolbar"
]

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


# # Since we're in Docker, we do this to match the machine address of Docker
# hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
# INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
