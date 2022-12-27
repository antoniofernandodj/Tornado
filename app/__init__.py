from app.config import settings as s
from app.config import app_settings
from app.views import handlers #, routes
from tornado.web import Application
from tornado_sqlalchemy import SQLAlchemy

def make_app() -> Application:
    app = Application(
        db=SQLAlchemy(s.DATABASE_URI),
        handlers=handlers,
        # routes=routes,
        debug=s.TORNADO_DEBUG,
        **app_settings
    )
    return app
