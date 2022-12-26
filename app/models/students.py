from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from tornado_sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from app.config import settings as s
from time import sleep
from sqlalchemy.orm import relationship


Base = declarative_base()
login = f'{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}'

try:
    socket = f'{s.POSTGRES_HOSTNAME}:{s.POSTGRES_PORT}'
except AttributeError:
    socket = f'localhost:{s.POSTGRES_PORT}'


# pip install psycopg2-binary
students_engine = create_engine(f"postgresql+psycopg2://{login}@{socket}/{s.POSTGRES_DB}")


student_teacher = Table(
    "student_teacher", Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("teacher_id", ForeignKey("teacher.id"), primary_key=True),
)


student_exam = Table(
    "student_exam", Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("exam_id", ForeignKey("exam.id"), primary_key=True),
)


class Admin(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user = Column(String(100))
    senha = Column(String(100))


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user = Column(String(100))
    password = Column(String(100))
    code = Column(String(100))
    students = relationship("Student", secondary=student_teacher, back_populates="teachers")
    academic_discipline = relationship("AcademicDiscipline", back_populates="teacher", uselist="false")


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user = Column(String(100))
    password = Column(String(100))
    code = Column(String(100))
    teachers = relationship("Teacher", secondary=student_teacher, back_populates="students")


    def __repr__(self):
        return f"<User(id='{self.id}', nome='{self.nome}')>"


class AcademicDiscipline(Base):
    __tablename__ = "academic_discipline"
    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    name = Column(String(100))
    teacher = relationship("Teacher", back_populates="academic_discipline")
    teacher_id = Column(Integer, ForeignKey("teacher.id"))


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    name = Column(String(100))
    academic_discipline = relationship("AcademicDiscipline", back_populates="books")
    academic_discipline_id = Column(Integer, ForeignKey("academic_discipline.id"))


class Homework(Base):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    academic_discipline = relationship("AcademicDiscipline", back_populates="homeworks")
    academic_discipline_id = Column(Integer, ForeignKey("academic_discipline.id"))
    teacher = relationship("Teacher", back_populates="homeworks")
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    book = relationship("Book", back_populates="homeworks")
    book_id = Column(Integer, ForeignKey("book.id"))
    date = Column(DateTime)


class Exam(Base):
    __tablename__ = "exam"
    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    academic_discipline = relationship("AcademicDiscipline", back_populates="exams")
    academic_discipline_id = Column(Integer, ForeignKey('academic_discipline.id'))
    book = relationship("Book", back_populates="exams")
    book_id = Column(Integer, ForeignKey("book.id"))
    date = Column(DateTime)


def init_db():
    loop = True
    while loop:
        try:
            Base.metadata.create_all(students_engine)
            loop = False
        except OperationalError as e:
            print(e)
            sleep(5)
