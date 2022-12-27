from app.views.students import students
from tornado.web import StaticFileHandler
from app.config import settings as s


handlers = [
    (r"/", students.RootHandler),
    (r"/student/([0-9]+)/", students.StudentHandler),
    (r"/login/", students.LoginHandler),
    (r"/(img\.png)", StaticFileHandler, {'path': s.STATIC_PATH}),
    (r"/signin/", students.SigninHandler),
    (r"/logout/", students.LogoutHandler)
]