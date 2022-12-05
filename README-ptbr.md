# Tornado

Este repositório é uma tentativa do framework tornado!

Tornado é um framework escalável, assíncrono e não-bloqueante, projetado para lidar com solicitações de alta carga.
Estrutura escalável, assíncrona e projetada para lidar com solicitações de alta carga.
Projetado para escalar para dezenas de milhares de conexões abertas, tornando-o ideal para aplicações que exigem conexões longas, como websockets.

O que eu tinha em mente quando criei isso era: Como criar uma arquitetura robusta o suficiente para lidar com um grande site? Com muitos recursos?
Conexão com múltiplos bancos de dados se necessário? Múltiplas views para atender a vários tipos de models, para cada classe de usuários,
como um módulo para lidar com usuários simples, alunos, outro para lidar com professores, outro para lidar com o diretor da escola? Você entendeu.

O que eu tinha em mãos no momento da criação? Muita experiência em Flask e alguma em Django, e quase nenhuma experiência no assunto async/await.
Então, decidi criar isso para aprender durante o código.

## O reconhecimento de padrões

A primeira coisa que decidi fazer foi entrar na documentação e ver a cara do hello world.
Então, acho que posso reconhecer as responsabilidades dos componentes no código para separá-los em seus pacotes/módulos específicos.

```
import asyncio

import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```

### Os Handle
À primeira vista notei algumas coisas.
Existe uma lista de tuplas contendo pares (url, Class) na classe Application.
Isso me dá um sinal de que será útil separar em um pacote todos os (url, handlers) que tenho em meu servidor,
bem como as classes "Handle", como a imediatamente acima (da qual falarei mais adiante).
Mas, se eu tiver várias classes de usuários? Me ocorreu criar um pacote de manipuladores com os arquivos .py que preciso em meu projeto,
e um arquivo __init__.py acumulando todas as diferentes classes de manipuladores em uma lista,
e o arquivo principal do projeto importaria essa lista com todos os handlers de servidor e o registraria na classe Application:

```
|
--handlers--
|           |
|           --- __init__.py
|           |
|           --- student.py
|           |
|           --- ...etc...

```

No __init___.py:

```
from . import (
    student,
    teacher
)

handlers = [
    *student.handler,
    *student.handler,
    *etc.handlers
]
```

### As views

### Os statics

### O(s) database(s)

### O processo de excecussão process
