
from dynaconf import Dynaconf
from os import path
from pathlib import Path

current_directory = (Path(__file__).parent)

settings = Dynaconf(
    envvar_prefix="TORNADO",
    settings_files=[
        path.join(current_directory, 'settings.toml'),
        path.join(current_directory, '.secrets.toml')
    ],
)


settings.STATIC_PATH = path.join(path.dirname(__file__), 'views', 'static')
# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.


app_settings = {
    "static_path": settings.STATIC_PATH,
    "cookie_secret": settings.COOKIE_SECRET,
    "login_url": settings.LOGIN_URL,
    "xsrf_cookies": settings.XSRF_COOKIES,
}
