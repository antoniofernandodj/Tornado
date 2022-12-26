from app.config import settings as s
from app.config import app_settings
from app.views import handlers #, routes
from tornado.web import Application

def make_app() -> Application:
    app = Application(
        handlers=handlers,
        # routes=routes,
        debug=s.TORNADO_DEBUG,
        **app_settings
    )
    return app
