from .config import config, settings
from .handlers import handlers
from tornado.web import Application


app = Application(
    handlers=handlers,
    debug=config.TORNADO_DEBUG,
    **settings
)