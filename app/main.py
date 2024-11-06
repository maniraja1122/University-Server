from db import engine,Base,get_db
from models import Student,Subject,Enrolled


Base.metadata.create_all(engine)
session=get_db()
# Creating a new student
new_student = Student(name='Alice', dob='2000-01-01')

# Creating a new subject
new_subject = Subject(title='Mathematics', credithours=3)

# Enrolling the student in the subject
enrollment = Enrolled(student=new_student, subject=new_subject)

# Adding to the session
session.add(new_student)
session.add(new_subject)
session.add(enrollment)
session.commit()

# Accessing the student's subjects
print(new_student.subjects)  # [<Subject(title='Mathematics')>]

# Accessing students enrolled in a subject
print(new_subject.students)  # [<Student(name='Alice')>]