from app import make_app, models
from app.config import settings as s
# from tornado.ioloop import IOLoop
import asyncio

models.init_all_dbs()

# if __name__ == "__main__":
#     app = make_app()
#     print(f'Inicianto o servidor http://localhost:{s.TORNADO_PORT}')
#     app.listen(s.TORNADO_PORT)
#     IOLoop.instance().start()


async def main():
    app = make_app()
    app.listen(s.TORNADO_PORT, reuse_port=True)
    await asyncio.Event().wait()
    
if __name__ == '__main__':
    asyncio.run(main())