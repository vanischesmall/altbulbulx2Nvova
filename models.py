# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from database import Base
SQLALCHEMY_DATABASE_URL = "postgresql://vanische:17032001os@localhost/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Base = declarative_base()

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rating = Column(Integer)

    feedback = relationship("Feedback", back_populates="teacher")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    comment = Column(String)

    teacher = relationship("Teacher", back_populates="feedback")

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    grade = Column(Integer)