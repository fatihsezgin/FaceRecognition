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
