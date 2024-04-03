from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

# engine = create_engine('sqlite:///dbase.db')
SQLALCHEMY_DATABASE_URL = "postgresql://vanische:17032001os@localhost/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


class Users: ...
class Teacher: ...
class Subjects:...
class Feedback: ...
class Feedback2: ...
class Timetable: ...


class Feedback(Base):
    __tablename__ = 'feedback'
    
    fb_id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    text = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="feedback")


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    teacher_name = Column(String)
    subject = Column(String)
    teacher_password = Column(String)
    feedback = relationship("Feedback", back_populates="teacher")

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    grade = Column(Integer)

class Subjects(Base):
    __tablename__ = 'subjects'

    subj_id = Column(Integer, primary_key=True)
    subject = Column(String)
    teacher = Column(String)
    grade = Column(Integer)

class Timetable(Base):
    __tablename__ = 'timetables'

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    teacher_name = Column(String)
    grade = Column(Integer)
    wd = Column(String)
    numb = Column(Integer)

    feedback2 = relationship("Feedback2", back_populates="timetable")

class Feedback2(Base):
    __tablename__ = 'feedback2'

    id = Column(Integer, primary_key=True)
    tt_id = Column(Integer)
    rate0 = Column(Integer)

    timetable_id = Column(Integer, ForeignKey('timetables.id'))
    timetable = relationship('Timetable', 
                             back_populates='feedback2', 
                             primaryjoin="Feedback2.timetable_id == Timetable.id"
                             ) 

Base.metadata.create_all(engine)
