from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
import datetime


Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    
    group: Mapped['Group'] = relationship(back_populates='students')
    grades: Mapped[list['Grade']] = relationship(back_populates='student')


class Group(Base):
    __tablename__ = 'groups'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
    students: Mapped[list['Student']] = relationship(back_populates='group')


class Teacher(Base):
    __tablename__ = 'teachers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
    subjects: Mapped[list['Subject']] = relationship(back_populates='teacher')


class Subject(Base):
    __tablename__ = 'subjects'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    
    teacher: Mapped['Teacher'] = relationship(back_populates='subjects')
    grades: Mapped[list['Grade']] = relationship(back_populates='subject')


class Grade(Base):
    __tablename__ = 'grades'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    grade: Mapped[float] = mapped_column(nullable=False)
    date_received: Mapped[datetime.date] = mapped_column(nullable=False)
    
    student: Mapped['Student'] = relationship(back_populates='grades')
    subject: Mapped['Subject'] = relationship(back_populates='grades')
