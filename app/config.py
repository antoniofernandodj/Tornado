from collections import namedtuple
import os


Config = namedtuple(
    'Config', (
        'TORNADO_PORT', 'TORNADO_DEBUG', 'MYSQL_PORT',
        'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_HOSTNAME',
        'MYSQL_DATABASE',
    )
)

config = Config(
    TORNADO_PORT=8888,
    TORNADO_DEBUG=True,
    MYSQL_PORT=3306,
    MYSQL_USER='antonio',
    MYSQL_PASSWORD='senha1234',
    MYSQL_HOSTNAME='localhost',
    MYSQL_DATABASE='database'
)

settings = {
    "static_path": os.path.join(
        os.path.dirname(__file__),
        'views',
        "static"
    ),
    "cookie_secret": "rJtbZZG8M0n1pZOeedI_bG7ymVWezC_sKxb7mk3Uo0whUsCOhtPRRIxyCk2IJME1gg0",
    "login_url": "/login",
    "xsrf_cookies": True,
}