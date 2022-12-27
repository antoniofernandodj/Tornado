# Tornado

Este repositório é uma tentativa com o framework Tornado!

Tornado é um framework escalável, assíncrono e não-bloqueante, projetado para lidar com solicitações de alta carga.
Projetado para escalar para dezenas de milhares de conexões abertas, tornando-o ideal para aplicações que exigem conexões como websockets ou long polling.

O que eu tinha em mente quando criei este repositório era: Como projetar uma arquitetura robusta o suficiente para lidar com um grande site? Com muitos recursos?
Conexão com múltiplos bancos de dados caso necessário? Múltiplas views para atender a vários tipos de models, para cada classe de usuários,
como um módulo para lidar com usuários simples, alunos, outro para lidar com professores, outro para lidar com o diretor da escola? Você entendeu.

O que eu tinha em mãos no momento da criação? Muita experiência em Flask e alguma em Django, e quase nenhuma experiência no assunto async/await.
Então, decidi criar isso para aprender durante o código.

## O reconhecimento de padrões

A primeira coisa que decidi fazer foi entrar na documentação e ver o aspecto do hello world.
Então, reconhecendo as responsabilidades dos componentes no código pude separá-los em seus pacotes/módulos específicos.

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

### Os Handlers
À primeira vista notei algumas coisas.
Existe uma lista de tuplas contendo pares (url, Handler) como parametro do método contrutor da classe Application.
Cada uma destas classes 'Handler' é responsável em lidar com as requisições HTTP e seus verbos pelo que a estrutura sugere,
dado que o Tornado é contruído em cima do http.server, e também pelo fato de eles estarem ligados a urls na lista em questão.
Isso me dá um sinal de que será útil separar em um módulo todos os (url, Handlers) que tenho em meu servidor,
bem como as classes "Handlers", como a imediatamente acima (da qual falarei mais adiante).
Mas, se eu tiver várias classes de usuários?

Me ocorreu então criar um pacote 'views' para as classes de usuario/visualização.
Dentro deste pacote eu criarei N pacotes, cada pacote com um __init__.py, seus statics e seus templates.
A estrutura emergiu de forma natural apontando para esta estrutura, e não para uma unica pasta de templates.
Se eu precisasse usar uma pasta unica e centralizada para os templates eu teria que carregar uma variável de
ambiente apontando o diretório da pasta de templates para usá-la em todos os pacotes de 'views'. Por isso
preferi manter a estrutura atual, também pelo fato de que cada pasta de template isolaria bem as responsabilidades
de cada módulo.

Em cada pacote dentro de views o arquivo __init__.py teria uma lista de handlers de cada contexto de visualização,
Enquando que o pacote pai 'views' teria um arquivo __init__.py que acumularia por assim dizer todos os handlers de
todas as views.

```
|
├─ app
|   ├─ models
|   |
|   ├─ views
|   |   |
|   |   ├─ students
|   |   |   |
|   |   |   ├─ static
|   |   |   |   ├ ...
|   |   |   |   ...
|   |   |   |
|   |   |   ├─ templates
|   |   |   |   ├ ...
|   |   |   |   ...
|   |   |   |
|   |   |   ├─ __init__.py
|   |   |   |
|   |   |   └─ students.py  <- Armazena os handlers students
|   |   |   
|   |   ├─ foo ...
|   |   |   └─ ... <- Armazena os handlers foo
|   |   |
|   |   ├─ bar ...
|   |   |   └─ ... <- Armazena os handlers bar
|   |   |  
|   |   └─ __init__.py
|   |   
|   ...
.
|   └─ __init__.py

```

No __init___.py do 'views':

```
from app.views import students
from app.views import foo
from app.views import bar

handlers = [
    *students.handlers,
    *students.foo,
    *students.bar
]

```

### As views

### Os statics

### O(s) database(s)

### A autentticação

### O processo de excecussão process
