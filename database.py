import sqlite3 as sqlite
from datetime import datetime


class database():
    def __init__(self):
        super(database, self).__init__()
        self.dbName = 'database.db'
        # a sql connection object
        self.connection = sqlite.connect(self.dbName)

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        with sqlite.connect(self.dbName) as db:
            try:
                c = db.cursor()
                c.execute(create_table_sql)
            except sqlite.Error as e:
                print(e)

    def createTableQueries(self):
        createTableQueries = [
            """ CREATE TABLE IF NOT EXISTS "students" ( `studentID` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, `surname` TEXT, `schoolnumber` TEXT, `faculty` TEXT, `department` TEXT, `imgPath` TEXT ); """,
            """CREATE TABLE IF NOT EXISTS "courses" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `coursename` TEXT, `teacher` TEXT )""",
            """CREATE TABLE IF NOT EXISTS "course_student" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `courseid` INTEGER, `studentid` INTEGER, FOREIGN KEY(`courseid`) REFERENCES courses(`id`), FOREIGN KEY(studentid) REFERENCES students(studentID) )""",
            """CREATE TABLE IF NOT EXISTS `session` ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `courseid` INTEGER, `createdAt` TEXT, FOREIGN KEY(`courseid`) REFERENCES courses(`id`))""",
            """CREATE TABLE IF NOT EXISTS `session_student` ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `sessionid` INTEGER, `studentid` INTEGER , FOREIGN KEY(`sessionid`) REFERENCES session(`id`), FOREIGN KEY(studentid) REFERENCES students(studentID) )"""]

        for i in range(len(createTableQueries)):
            self.create_table(createTableQueries[i])

    # Inserts a student into students table
    def insertStudent(self, studentName, studentSurname, studentNumber, faculty, department, imgPath):
        with sqlite.connect(self.dbName) as db:
            list = (studentName, studentSurname, studentNumber, faculty, department, imgPath)
            cursor = db.cursor()
            query = "INSERT INTO students VALUES (null,?,?,?,?,?,?)"
            result = cursor.execute(query, list)
            self.connection.commit()
            return result

    # Inserts a course into courses table
    def insertCourse(self, courseName, teacherName):
        with sqlite.connect(self.dbName) as db:
            list = (courseName, teacherName)
            cursor = db.cursor()
            query = "INSERT INTO courses VALUES (null,?,?)"
            result = cursor.execute(query, list)
            self.connection.commit()
            return result

    # Returns a student within given id
    def studentById(self, studentId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("Select * from students where studentID=?", (studentId,)).fetchone()

    # returns a list of courses that is recorded
    def getCourses(self):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            cursor.execute("Select * from courses")
            courseList = []
            cur = cursor.fetchall()
            for i in range(len(cur)):
                courseList.append(cur[i][1])
            return courseList

    # returns the course id within course name
    def getCourseId(self, courseName):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            cursor.execute("Select * from courses where coursename =?", (courseName,))
            cur = cursor.fetchone()
            return cur[0]


    def getSessionId(self, date):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            print('date '+date)
            cursor.execute("Select * from session where createdAt =?", (date,))
            cur = cursor.fetchall()
            return cur[0][0]

    # inserts a student into course
    def insertCourseStudent(self, courseId, studentId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("INSERT INTO course_student VALUES (null,?,?)", (courseId, studentId,))

    # returns the students for the given course id
    def getStudentsForCourse(self, courseId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("select * from course_student inner join students on "
                                  "students.studentID = course_student.studentid where course_student.courseid = ?",
                                  (courseId,)).fetchall()

    # returns the column names for student
    def getStudentsTableHeaders(self):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA table_info(students)")
            cur = cursor.fetchall()
            headers = []
            for i in range(len(cur)):
                headers.append(cur[i][1])
            return headers

    # selects the all records in student table
    def getAllStudents(self):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("Select * from students").fetchall()

    # returns school number of attendees that given course id
    def getStudentIdsForCourse(self, courseId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("select students.schoolnumber from course_student inner join students on "
                                  "students.studentID = course_student.studentid where course_student.courseid = ?",
                                  (courseId,)).fetchall()

    # create new session record with courseid
    def createSession(self, courseId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            now = datetime.now()
            return cursor.execute("Insert Into session values (null,?,?)",
                                  (courseId, now.strftime("%d/%m/%Y %H:%M:%S"),))

    # returns the last inserted id in session table
    def getLastSessionId(self):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("Select MAX(id) From session").fetchone()

    # inserts a student into session
    def insertSessionStudent(self, sessionId, studentId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("INSERT INTO session_student VALUES (null,?,?)", (int(sessionId), int(studentId),))

    def getSessionByCourseId(self, courseID):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            cur = cursor.execute("Select * from session where courseid = ?",(courseID,)).fetchall()
            sessionList = []
            for i in range(len(cur)):
                sessionList.append(cur[i][2])
            return sessionList

    def getStudentsBySession(self, sessionId):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            print('session id '+str(sessionId))
            cur = cursor.execute("Select * from session_student where sessionid = ?",(sessionId,)).fetchall()
            studentList = []
            print(cur)
            for i in range(len(cur)):
                student = self.studentById(cur[i][2])[0]
                studentName = student[1] + ' ' + student[2]
                studentList.append(studentName)
            return studentList

    def getStudentByStudentNo(self, studentNo):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("Select * from students where schoolnumber=?", (studentNo,)).fetchall()

    def getStudentIdBySchoolNo(self, no):
        with sqlite.connect(self.dbName) as db:
            cursor = db.cursor()
            return cursor.execute("Select studentId from students where schoolnumber=?", (no,)).fetchall()