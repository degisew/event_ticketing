import socket
from config.settings.base import *  # noqa F403
from config.settings.base import INSTALLED_APPS, MIDDLEWARE, ALLOWED_HOSTS

INSTALLED_APPS += ["drf_spectacular", "silk", "debug_toolbar"]

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # Disable profiling panel due to an issue with Python 3.12:
        # https://github.com/jazzband/django-debug-toolbar/issues/1875
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}


# Since we're in Docker, we do this to match the machine address of Docker
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
