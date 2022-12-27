from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from tornado_sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Text
from app.config import settings as s
from time import sleep
from sqlalchemy.orm import relationship

from tornado_sqlalchemy import SQLAlchemy

Base = declarative_base()

# pip install psycopg2-binary
students_engine = create_engine(s.DATABASE_URI)
# db = SQLAlchemy(s.DATABASE_URI)


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
    password = Column(Text)


class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user = Column(String(100))
    password = Column(Text)
    code = Column(String(100))
    homeworks = relationship("Homework", back_populates="teacher")
    students = relationship("Student", secondary=student_teacher, back_populates="teachers")
    academic_discipline = relationship("AcademicDiscipline", back_populates="teacher", uselist="false")
    
    def __repr__(self):
        return f"<Teacher(id='{self.id}', name='{self.name}')>"


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user = Column(String(100))
    password = Column(Text)
    code = Column(String(100))
    teachers = relationship("Teacher", secondary=student_teacher, back_populates="students")


    def __repr__(self):
        return f"<Student(id='{self.id}', name='{self.name}')>"


class AcademicDiscipline(Base):
    __tablename__ = "academic_discipline"
    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    name = Column(String(100))
    teacher = relationship("Teacher", back_populates="academic_discipline")
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    books = relationship("Book", back_populates="academic_discipline")
    homeworks = relationship("Homework", back_populates="academic_discipline")
    exams = relationship("Exam", back_populates="academic_discipline")
    


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    name = Column(String(100))
    academic_discipline = relationship("AcademicDiscipline", back_populates="books")
    academic_discipline_id = Column(Integer, ForeignKey("academic_discipline.id"))
    homeworks = relationship("Homework", back_populates="book")
    exams = relationship("Exam", back_populates="book")


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
