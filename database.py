import sqlite3 as sqlite


# db = sqlite.connect('database.db') #GNU/Linux

class database():
    def __init__(self):
        super(database, self).__init__()
        # dbpath = '/home/fatih/Desktop/Python/SoftwareDesingApplicationsFinal/FaceRecognition/database.db'
        self.dbName = 'database.db'
        self.connection = sqlite.connect(self.dbName)

    def insertStudent(self, studentName, studentSurname, studentNumber, faculty, department, imgPath):
        with sqlite.connect(self.dbName) as db:
            list = (studentName, studentSurname, studentNumber, faculty, department, imgPath)
            cursor = db.cursor()
            query = "INSERT INTO students VALUES (null,?,?,?,?,?,?)"
            result = cursor.execute(query, list)
            self.connection.commit()
            return result

    def insertCourse(self, courseName, teacherName):
        with sqlite.connect(self.dbName) as db:
            list = (courseName, teacherName)
            cursor = db.cursor()
            query = "INSERT INTO courses VALUES (null,?,?)"
            result = cursor.execute(query, list)
            self.connection.commit()
            return result

    def getCourses(self):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            cursor.execute("Select * from courses")
            courseList = []
            cur = cursor.fetchall()
            for i in range(len(cur)):
                courseList.append(cur[i][1])
            return courseList

    def getCourseId(self, courseName):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            cursor.execute("Select * from courses where coursename =?", (courseName,))
            cur = cursor.fetchall()
            return cur[0][0]

    def insertCourseStudent(self, courseId, studentId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("INSERT INTO course_student VALUES (null,?,?)", (courseId, studentId,))

    def getStudentsForCourse(self, courseId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("select * from course_student inner join students on "
                           "students.studentID = course_student.studentid where course_student.courseid = ?",
                           (courseId,))
