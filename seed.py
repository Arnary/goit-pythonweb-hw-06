from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from models import Base, Student, Group, Teacher, Subject, Grade

fake = Faker()

engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/mydb')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

def create_groups():
    groups = []
    group_names = ["Group A", "Group B", "Group C"]
    for name in group_names:
        group = Group(name=name)
        session.add(group)
        groups.append(group)
    session.commit()
    return groups

def create_teachers():
    teachers = []
    for _ in range(random.randint(3, 5)):
        teacher = Teacher(name=fake.name())
        session.add(teacher)
        teachers.append(teacher)
    session.commit()
    return teachers

def create_subjects(teachers):
    subjects = []
    subject_names = ["Mathematics", "Physics", "Chemistry", "Literature", "Biology", "History", "Geography", "Computer Science"]
    for name in subject_names[:random.randint(5, 8)]:
        subject = Subject(name=name, teacher=random.choice(teachers))
        session.add(subject)
        subjects.append(subject)
    session.commit()
    return subjects

def create_students(groups):
    students = []
    for _ in range(random.randint(30, 50)):
        student = Student(name=fake.name(), group=random.choice(groups))
        session.add(student)
        students.append(student)
    session.commit()
    return students

def create_grades(students, subjects):
    for student in students:
        num_grades = random.randint(10, 20) 
        for _ in range(num_grades):
            grade = Grade(
                student=student,
                subject=random.choice(subjects),
                grade=round(random.uniform(3.0, 5.0), 2),
                date_received=fake.date_this_decade()
            )
            session.add(grade)
    session.commit()

def seed_database():
    print("Створення груп...")
    groups = create_groups()

    print("Створення викладачів...")
    teachers = create_teachers()

    print("Створення предметів...")
    subjects = create_subjects(teachers)

    print("Створення студентів...")
    students = create_students(groups)

    print("Створення оцінок...")
    create_grades(students, subjects)

    print("База даних успішно заповнена випадковими даними.")

if __name__ == "__main__":
    seed_database()
