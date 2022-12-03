from abc import ABC
import tornado.web
import json
from sqlalchemy.orm import Session
from typing import Any
from .. import models
from tornado.web import Application
from tornado.httputil import HTTPServerRequest
import os


class Base(tornado.web.RequestHandler, ABC):
    def __init__(
            self,
            application: Application,
            request: HTTPServerRequest
    ):
        super().__init__(application, request)
        self.json_args = None

    def render_template(self, template_name: str, **kwargs: Any):
        path = os.path.join('templates', template_name)
        self.render(path, **kwargs)

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None


class StudentHandler(Base, ABC):
    def get(self):
        with Session(models.students.engine) as db:
            students = db.query(models.students.User).all()

        self.render_template(
            "base.html",
            students=students
        )

    def post(self):
        self.set_header("X-Ola", "Mundo")
        mensagem = self.get_body_argument("message")

        self.render_template(
            "mensagem.html",
            mensagem=mensagem
        )


class BoldHandler(Base, ABC):
    def get(self):
        # with Session(models.students.engine) as db:
        #     students = db.query(models.students.User).all()

        try:
            db = Session(models.students.engine)
            students = db.query(models.students.User).all()
        finally:
            db.close()

        self.render_template(
            "bold.html",
            students=students
        )

    def post(self):
        self.set_header("X-Ola", "Mundo")
        mensagem = self.get_body_argument("message")

        self.render_template(
            "mensagem.html",
            mensagem=mensagem
        )


class MainHandler(Base, ABC):
    def get(self):
        self.render_template(
            "helloworld.html"
        )