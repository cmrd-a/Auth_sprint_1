from gevent import monkey

monkey.patch_all()

from app import create_app  # noqa
