import csv
import os
from os import walk

from optparse import OptionParser
...
parser = OptionParser()
parser.add_option("-P", type="int", dest="P", default=0)
parser.add_option("--TB", type="float", dest="TB", default=-1.0)
parser.add_option("--TE", type="float", dest="TE", default=-1.0)
(options, args) = parser.parse_args()
class Student:

    def __init__(self, name, number):
        self._name = name
        self._number = number


class Lecture(Student):

    def __init__(self, timeAttended, lecture, state, numOfMessages, name, number):
        super().__init__(name, number)
        self._timeAttended = timeAttended
        self._lecture = lecture
        self._state = state
        self._numOfMessages = numOfMessages


class Message(Lecture):

    def __init__(self, sender, hours, minutes, seconds, file, timeAttended, lecture, state, numOfMessages, name,
                 number):
        super().__init__(timeAttended, lecture, state, numOfMessages, name, number)
        self._sender = sender
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
        self._file = file


def readStudentList(studentsList, position):
    pos = 0
    with open(r'C:\Python\LastProject\ENCS3130-StudentList.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        crntRow = 0
        for line in csv_reader:
            if crntRow == 0:
                crntRow += 1
                continue
            line[1] = line[1].lstrip()
            line[1] = line[1].rstrip()
            crntStudent = [Student(line[1], line[0])]
            studentsList.append(crntStudent)
            position[line[1]] = pos
            pos += 1


def readAttedance(studentsList, position):
    for dirpath, dirnames, filenames in walk(r'C:\Python\LastProject\MeetingAttendanceReports'):
        for file in filenames:
            tmpList = "MeetingAttendanceReports\\" + file
            with open(tmpList) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                crntRow = 0
                for information in csv_reader:
                    if crntRow == 0:
                        crntRow += 1
                        continue
                    name = ""
                    for c in information[0]:
                        if c == '(':
                            name = ""
                        if c.isalpha() or c == ' ':
                            name += c
                    name = name.lstrip()
                    name = name.rstrip()
                    fullName = name.split(' ')
                    for person in studentsList:
                        cnt = 0
                        for subName in fullName:
                            if subName.lower() in person[0]._name.lower():
                                cnt += 1
                        if cnt == len(fullName):
                            filename = file[0:len(file) - 7]
                            list = [Lecture(information[1], filename, "", 0, person[0]._name, person[0]._number)]
                            studentsList[position[person[0]._name]].append(list)
                            break


def getMinutes(time):
    minutes = 0.0
    hour = int(time[0] + time[1])
    minutes += hour * 60
    minute = int(time[3] + time[4])
    minutes += minute
    second = int(time[6] + time[7])
    minutes += second / 60.0
    return minutes


def readParticipation(studentsList, TB, TE, messageCount):
    for dirpath, dirnames, filenames in walk(r'C:\Python\LastProject\MeetingParticipationReports'):
        for file in filenames:
            os.chdir(r'C:\Python\LastProject\MeetingParticipationReports')
            f = open(file, encoding="utf8")
            lines = f.readlines()
            firstHour = ""
            firstMinute = ""
            firstSecond = ""
            lastHour = ""
            lastMinute = ""
            lastSecond = ""
            cntt = 0
            for line in lines:
                time = line.split(':')
                if len(time) == 4:
                    lastHour = time[0]
                    lastMinute = time[1]
                    lastSecond = time[2][:2]
            for line in lines:
                time = line.split(':')
                if len(time) == 4:
                    hours = time[0]
                    minutes = time[1]
                    seconds = time[2][:2]
                    if cntt == 0:
                        firstHour = time[0]
                        firstMinute = time[1]
                        firstSecond = time[2][:2]
                        cntt += 1
                        continue
                    else:
                        first = getMinutes(firstHour + ':' + firstMinute + ':' + firstSecond)
                        second = getMinutes(hours + ':' + minutes + ':' + seconds)
                        if second - first <= TB:
                            continue
                        third = getMinutes(lastHour + ':' + lastMinute + ':' + lastSecond)
                        if third - second <= TE:
                            continue
                    result = line[line.find(" From ") + len(" From "): line.find(" to ")]
                    name = ""
                    for c in result:
                        if c == '(':
                            name = ""
                        if c.isalpha() or c == ' ':
                            name += c
                    name = name.lstrip()
                    name = name.rstrip()
                    fullName = name.split(' ')
                    for person in studentsList:
                        cnt = 0
                        for subName in fullName:
                            if subName.lower() in person[0]._name.lower():
                                cnt += 1
                        filename = file[0:len(file) - 7]
                        if cnt == len(fullName):
                            if len(person) == 1:
                                continue
                            for i in range(1, len(person)):
                                if person[i][0]._lecture == filename:
                                    person[i].append(
                                        Message(str(person[0]._name), str(hours), str(minutes), str(seconds),
                                                str(filename), person[i][0]._timeAttended, person[i][0]._lecture,
                                                "", 0, person[0]._name, person[0]._number, ))
                                    if person[0]._name in messageCount:
                                        if filename[9:] in messageCount[person[0]._name]:
                                            messageCount[person[0]._name][filename[9:]] += 1
                                        else:
                                            messageCount[person[0]._name][filename[9:]] = 1
                                    else:
                                        messageCount[person[0]._name] = {}
                                        messageCount[person[0]._name][filename[9:]] = 1


def setState(studentsList, P):
    for person in studentsList:
        if len(person) == 1:
            continue
        for i in range(1, len(person)):
            if int(person[i][0]._timeAttended) >= int(P):
                person[i][0]._state = "x"
            else:
                person[i][0]._state = "a"


studentsList = []
position = {}
messageCount = {}
parser.add_option("-t", "--tile", dest="TE",
                  help="write report to FILE", metavar="FILE")
readStudentList(studentsList, position)
for person in studentsList:
    print(person[0]._name + ', ' + person[0]._number)

readAttedance(studentsList, position)
TB = float(input("\nEnter the TB value: "))
TE = float(input("\nEnter the TE value: "))
readParticipation(studentsList, TB, TE, messageCount)
P = input("\nEnter the minimum attendance time: ")
setState(studentsList, P)

for person in studentsList:
    if len(person) == 1:
        continue
    print(person[0]._name + ', ' + person[0]._number)
    for i in range(1, len(person)):
        print(person[i][0]._lecture + ', ' + person[i][0]._timeAttended + ', ' + person[i][0]._state)
    for i in range(1, len(person)):
        for j in range(1, len(person[i])):
            print(person[i][j]._sender + ', ' + person[i][j]._hours + ':' + person[i][j]._minutes + ':' +
                  person[i][j]._seconds + ', ' + person[i][j]._file)
    print("---------------------------------------------------------------------------")

for person in messageCount:
    print(person)
    for files in messageCount[person]:
        print(files + ', ' + str(messageCount[person][files]))

