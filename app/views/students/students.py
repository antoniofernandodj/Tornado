import json
import os
from abc import ABC
from typing import Any
from tornado_sqlalchemy import SessionMixin, as_future
import asyncio
from tornado.gen import coroutine

import tornado.web
from sqlalchemy.orm import Session
from tornado.httputil import HTTPServerRequest
from tornado.web import Application
from bcrypt import gensalt, hashpw, checkpw
import bcrypt
from app.models.students import students_engine

from app import models


def login_required(method):
    async def inner(self, *args, **kwargs):
        student = await self.current_user
        if not student:
            self.set_status(401)
            self.finish('Usuário desconectado!')
        else:
            await method(self, *args, **kwargs)
    return inner


class Base(tornado.web.RequestHandler, SessionMixin, ABC):
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
    async def current_user(self):
        user_id = self.get_secure_cookie('user_id')
        user_id = int(user_id.decode('utf-8')) if user_id else None
        if not user_id:
            return None
        with self.make_session() as db:
            student = await as_future(db.query(models.students.Student).filter_by(id=user_id).first)
        return student
            
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None
        # self.form_data = {
        #     key: [val.decode('utf8') for val in val_list]
        #     for key, val_list in self.request.arguments.items()
        # }
            
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        # self.set_header("Content-Type", 'application/json; charset="utf-8"')
        
    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))


class StudentHandler(Base, ABC):
    
    @login_required
    async def get(self, id):
        student = await self.current_user

        self.render_template("base.html", student=student)
            
    @login_required
    async def post(self):
        self.set_header("X-Ola", "Mundo")
        mensagem = self.get_body_argument("message")

        self.render_template(
            "mensagem.html",
            mensagem=mensagem
        )


class LoginHandler(Base, ABC):
    def get(self):
        self.render_template('login.html')
        
    async def post(self):
        user = self.get_body_argument('user')
        senha = self.get_body_argument('senha')
        
        
        with self.make_session() as db:
            student = await as_future(db.query(models.students.Student).filter_by(user=user).first)
            
            hashpw = student.password.encode()
            pw = senha.encode()
            print(pw, hashpw)
        
            if student and bcrypt.checkpw(pw, hashpw):
                sucess = True
                user_id = student.id
                self.set_secure_cookie("user_id", str(user_id))
            else:
                sucess = False
                
        if sucess:
            self.redirect(f"/student/{user_id}/")
        else:
            self.write('Credenciais inválidas!')


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
        name = self.get_body_argument("nome")
        user = self.get_body_argument("user")
        password = self.get_body_argument("senha")
        code = self.get_body_argument('code')
        
        hashpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        student = models.students.Student(
            name=name,
            user=user,
            password=hashpw,
            code=code
        )
        
        with self.make_session() as db:
            db.add(student)
            db.commit()
            
        self.write('Usuario cadastrado com sucesso!')


class RootHandler(Base, ABC):
    
    @login_required
    async def get(self):
        user = await self.current_user
        
        if user:
            self.redirect(f"/student/{user.id}/")
        else:
            self.redirect(f"/login/")
