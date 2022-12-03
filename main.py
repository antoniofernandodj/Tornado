from app import app, models
from app.config import config as c
from tornado.ioloop import IOLoop

models.init_all_dbs()

if __name__ == "__main__":
    print(f'Inicianto o servidor http://localhost:{c.TORNADO_PORT}')
    app.listen(c.TORNADO_PORT)
    IOLoop.instance().start()

