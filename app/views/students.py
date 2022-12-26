import json
import os
from abc import ABC
from typing import Any

import tornado.web
from sqlalchemy.orm import Session
from tornado.httputil import HTTPServerRequest
from tornado.web import Application
from bcrypt import gensalt, hashpw, checkpw
from app.models.students import students_engine

from app import models


def login_required(method):
    def inner(self, *args, **kwargs):
        student = self.current_user
        if not student:
            self.set_status(401)
            self.finish('Usuário desconectado!')
        else:
            method(self, *args, **kwargs)
    return inner


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

    @property
    def current_user(self):
        user_id = self.get_secure_cookie('user_id')
        user_id = int(user_id.decode('utf-8')) if user_id else None
        if not user_id:
            return None
        with Session(students_engine) as db:
            student = db.query(models.students.User).filter_by(id=user_id).first()
            return student
            
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None


class StudentHandler(Base, ABC):
    
    @login_required
    def get(self, id):
        student = self.current_user

        self.render_template(
            "base.html",
            student=student
        )
        
            
    @login_required
    def post(self):
        self.set_header("X-Ola", "Mundo")
        mensagem = self.get_body_argument("message")

        self.render_template(
            "mensagem.html",
            mensagem=mensagem
        )


class LoginHandler(Base, ABC):
    def get(self):
        self.render_template(
            'login.html'
        )
        
    def post(self):
        user = self.get_body_argument('user')
        senha = self.get_body_argument('senha')
        
        with Session(students_engine) as db:
            user = db.query(models.students.User).filter_by(user=user).first()
            
        if user and checkpw(senha.encode('utf-8'), user.senha.encode('utf-8')):
            self.set_secure_cookie("user_id", str(user.id))
        
        self.redirect(f"/student/{user.id}/")


class LogoutHandler(Base, ABC):
    def get(self):
        self.set_cookie('user_id', '')
        self.redirect("/login/")


class SigninHandler(Base, ABC):
    def get(self):        
        
        self.render_template(
            'logon.html'
        )
        
    def post(self):
        self.set_header("X-Ola", "Mundo")
        nome = self.get_body_argument("nome")
        user = self.get_body_argument("user")
        senha = self.get_body_argument("senha")
        
        salt = gensalt()
        
        user = models.students.User(
            nome=nome, user=user, senha=hashpw(senha.encode('utf-8'), salt)
        )
        
        with Session(students_engine) as db:
            db.add(user)
            db.commit()
        
        self.write('Usuario cadastrado com sucesso!')


class RootHandler(Base, ABC):
    def get(self):
        user = self.current_user
        if user:
            self.redirect(f"/student/{user.id}/")
        else:
            self.redirect(f"/login/")


class Favicon(Base, ABC):
    def get(self):
        self.write('')
