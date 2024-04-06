class Teacher():
    def teach(self):
        print("Преподаватель учит")

class School():
    def __init__(self, new_teacher):
        self.teacher = new_teacher

    def conduct_class(self):
        self.teacher.teach()


my_teacher = Teacher()
my_school = School(my_teacher)
my_school.conduct_class()

