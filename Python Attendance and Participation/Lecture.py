from project import Student


class Lecture(Student):

    def __init__(self, timeAttended, lecture):
        self.timeAttended = timeAttended
        self.lecture = lecture
