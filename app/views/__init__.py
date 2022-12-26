from app.views import students
from tornado.web import StaticFileHandler
from app.config import settings as s
# from tornado.web import url

handlers = [
    (r"/", students.RootHandler),
    (r"/student/([0-9]+)/", students.StudentHandler),
    (r"/login/", students.LoginHandler),
    (r"/(img\.png)", StaticFileHandler, {'path': s.STATIC_PATH}),
    (r"/signin/", students.SigninHandler),
    (r"/logout/", students.LogoutHandler)
]

routes = [
#     url(r"/logon/(.*)/", students.LogonHandler, name='antonio')
]
