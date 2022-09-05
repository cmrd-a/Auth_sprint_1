from gevent import monkey

monkey.patch_all()

from Auth.app import create_app  # noqa
