from tornado.web import StaticFileHandler
from .. import settings
from ..views import (
    students
)

handlers = [
    (r"/", students.MainHandler),
    (r"/students/", students.StudentHandler),
    (r"/bold/", students.BoldHandler),
    (r"/(img\.png)", StaticFileHandler, {'path': settings['static_path']}),
]
