# Tornado

This repo is a try on tornado framework!

Tornado is a scalable, asynchronous and non-blocking framework, designed to handle high load requests.
Designed to scale to tens of thousands of open connections, making it ideal for applications that require long connections like long-pooling or websockets.

What a had in mind when I created this was how to create a robust architecture to handle a large website? With many features? Connection with multiples databases if necessary? Multiple views to serve multiple kinds of templates, to each class of users, like one module to handle simple users students, other to handle teachers, other to handle the school principal? You got it.

What I had in hands at the creation time? Lots of experience in Flask and some in Django, and almost no experience in the async/await subject. So, i decided tho create this to learn while code.

## Learning

I used a book, the official documentation and some YT videos in brazillian portuguese and english to learn about the framework
- https://www.tornadoweb.org/en/stable/
- https://www.youtube.com/watch?v=-gJ21qzpieA
- https://www.youtube.com/watch?v=8Gt2vHgp7As
- https://www.youtube.com/watch?v=MUWy-NSrvNQ
- https://www.youtube.com/watch?v=NKPHP5p0WXA
- https://www.youtube.com/watch?v=uQmWfGs3qeA
- https://www.youtube.com/watch?v=kCoD6rGpDoE
- https://www.youtube.com/watch?v=3BYN3ouwkRA
- https://www.youtube.com/watch?v=4Ztq-Yz1ero


## The pattern-recognition

The first thing I decided to do was get into the documentation and see the face of the hello world.
So, I think I might regognize component responsabilies in the code to separethe them in their specific packages/modules


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
### The handlers
At first sight I noticed some things. There is a list of tuples containing pairs (url, Class) in the Application class. This give me a sign that will be usefull to separate in a package all the (url, handlers) I have in my server, as well the "Handle" classes, like the immediately above (wich i will talk later). But, if I have multiple classes of users? Came in my mind to create a package handlers with as .py files I need in my project, and a __init__.py file accumulating all the different class of handlers in a list, and the main file import that list with  all server handlers:

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

in the __init___:

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

### The views

### The statics

### The database(s)

### The run app process
