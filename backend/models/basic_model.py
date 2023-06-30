from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import *
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, functions
from backend.models.settings import *
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('backend.models.config')
    db.app = app
    db.init_app(app)
    Migrate(app, db)
    return db


class Location(db.Model):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    platform_id = Column(Integer)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Role(db.Model):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)
    role = Column(String)
    type = Column(String)
    platform_id = Column(Integer)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    id = Column(Integer, primary_key=True)
    __tablename__ = "user"
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    image = Column(String)
    balance = Column(Integer)
    password = Column(String)
    platform_id = Column(Integer)
    student = relationship('Student', backref='user', order_by="Student.id", lazy="dynamic")
    teacher = relationship("Teacher", backref="user", order_by="Teacher.id", lazy="select")
    question_answers = relationship('QuestionAnswers', backref='user', order_by="QuestionAnswers.id", lazy="dynamic")
    question_answer_comment = relationship('QuestionAnswerComment', backref='user', order_by="QuestionAnswerComment.id",
                                           lazy="dynamic")
    location_id = Column(Integer, ForeignKey('location.id'))
    role_id = Column(Integer, ForeignKey('role.id'))
    certificate = relationship("Certificate", backref="user", order_by="Certificate.id")

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Student(db.Model):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    debtor = Column(Integer)
    student_question = relationship("StudentQuestion", lazy="select", order_by="StudentQuestion.id")
    donelesson = relationship("StudentExercise", backref="student", order_by="StudentExercise.id")
    groups = relationship("Group", secondary="student_group", backref="student", order_by="Group.id")
    studentlesson = relationship("StudentLesson", backref="student", order_by="StudentLesson.id")
    studentcourse = relationship("StudentCourse", backref="student", order_by="StudentCourse.id")
    studentsubject = relationship("StudentSubject", backref="student", order_by="StudentSubject.id")
    representative_name = Column(String)
    representative_surname = Column(String)

    def add_commit(self):
        db.session.add(self)
        db.session.commit()

    def commit(self):
        db.session.commit(self)


class Group(db.Model):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    subject_id = Column(Integer, ForeignKey("subject.id"))
    platform_id = Column(Integer)
    course_id = Column(Integer, ForeignKey("subject_level.id"))
    teacher_salary = Column(Integer)
    teacher_id = Column(Integer)
    location_id = Column(Integer, ForeignKey('location.id'))

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


db.Table('student_group',
         db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
         db.Column('student_id', db.Integer, db.ForeignKey('student.id'))
         )

db.Table('teacher_subject',
         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
         db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
         )

db.Table('teacher_group',
         db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id')),
         db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
         )


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    groups = relationship("Group", secondary="teacher_group", backref="teacher", order_by="Group.id")

    def add_commit(self):
        db.session.add(self)
        db.session.commit()


class Images(db.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    size = Column(String)
    subjects = relationship("Subject", backref="img", order_by="Subject.id")
    blocks = relationship("ExerciseBlock", backref="img", order_by="ExerciseBlock.id")
    exercise_answers = relationship("ExerciseAnswers", backref="img", order_by="ExerciseAnswers.id")
    lesson_block = relationship("LessonBlock", backref="img", order_by="LessonBlock.id")

    def add(self):
        db.session.add(self)
        db.session.commit()


from backend.basics.models import *
from backend.lessons.models import *
from backend.essay_funtions.models import *
from backend.question_answer.models import *
from backend.question_answer.models import *
from backend.certificate.models import *
