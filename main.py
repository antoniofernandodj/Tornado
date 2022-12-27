from app import make_app, models
from app.config import settings as s
from tornado.ioloop import IOLoop
import asyncio
from os import system

models.init_all_dbs()

async def main():
    app = make_app()
    system('clear')
    print(f'Inicianto o servidor http://localhost:{s.PORT}')
    app.listen(s.PORT, reuse_port=True)
    await asyncio.Event().wait()
    
if __name__ == '__main__':
    asyncio.run(main())