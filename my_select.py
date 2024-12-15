from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import Student, Grade, Subject, Teacher, Group
from sqlalchemy import create_engine


engine = create_engine('postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/mydb')

def select_1(session: Session):
    return session.query(
        Student.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()

def select_2(session: Session, subject_name: str):
    return session.query(
        Student.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Student.id).order_by(desc('average_grade')).first()

def select_3(session: Session, subject_name: str):
    return session.query(
        Group.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Student, Student.group_id == Group.id).join(Grade, Grade.student_id == Student.id).join(Subject, Grade.subject_id == Subject.id).filter(Subject.name == subject_name).group_by(Group.id).all()

def select_4(session: Session):
    return session.query(func.avg(Grade.grade).label('average_grade')).scalar()

def select_5(session: Session, teacher_name: str):
    return session.query(Subject.name).join(Teacher).filter(Teacher.name == teacher_name).all()

def select_6(session: Session, group_name: str):
    return session.query(Student.name).join(Group).filter(Group.name == group_name).all()

def select_7(session: Session, group_name: str, subject_name: str):
    return session.query(
        Student.name,
        Grade.grade
    ).join(Group).join(Grade).join(Subject).filter(Group.name == group_name, Subject.name == subject_name).all()

def select_8(session: Session, teacher_name: str):
    return session.query(
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject).join(Teacher).filter(Teacher.name == teacher_name).scalar()

def select_9(session: Session, student_name: str):
    return session.query(Subject.name).join(Grade).join(Student).filter(Student.name == student_name).distinct().all()

def select_10(session: Session, student_name: str, teacher_name: str):
    return session.query(Subject.name).join(Grade, Grade.subject_id == Subject.id) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.name == student_name, Teacher.name == teacher_name).distinct().all()


if __name__ == "__main__":    
    with Session(engine) as session:
        print("1. 5 студентів із найбільшим середнім балом з усіх предметів:")
        print(select_1(session))
        
        print("\n2. Студента із найвищим середнім балом з певного предмета:")
        print(select_2(session, subject_name="Mathematics"))
    
        print("\n3. Середній бал у групах з певного предмета:")
        print(select_3(session, subject_name="Mathematics"))

        print("\n4. Середній бал на потоці (по всій таблиці оцінок):")
        print(select_4(session))

        print("\n5. Курси які читає певний викладач:")
        print(select_5(session, teacher_name="Eric Clark"))

        print("\n6. Список студентів у певній групі:")
        print(select_6(session, group_name="Group C"))

        print("\n7. Оцінки студентів у окремій групі з певного предмета:")
        print(select_7(session, group_name="Group A", subject_name="Chemistry"))

        print("\n8.Середній бал, який ставить певний викладач зі своїх предметів:")
        print(select_8(session, teacher_name="Darren Pearson"))

        print("\n9. Список курсів, які відвідує певний студент:")
        print(select_9(session, student_name="Ashley Henderson"))

        print("\n10. Список курсів, які певному студенту читає певний викладач:")
        print(select_10(session, student_name="Dawn Aguilar", teacher_name="Courtney Cruz"))
