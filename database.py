import sqlite3 as sqlite


#db = sqlite.connect('database.db') #GNU/Linux

class database():
    def __init__(self):
        super(database,self).__init__()
        #dbpath = '/home/fatih/Desktop/Python/SoftwareDesingApplicationsFinal/FaceRecognition/database.db'
        self.dbName = 'database.db'
        self.connection = sqlite.connect(self.dbName)

    def insertStudent(self,studentName,studentSurname,studentNumber,faculty,department):
        with sqlite.connect(self.dbName) as db:
            list= (studentName,studentSurname,studentNumber,faculty,department)
            cursor = db.cursor()
            query = "INSERT INTO students VALUES (null,?,?,?,?,?)"
            result = cursor.execute(query,list)
            self.connection.commit()
            return result
        '''
        try:

            list= (studentName,studentSurname,studentNumber,faculty,department)
            cursor = self.connection.cursor()
            query = "INSERT INTO students VALUES (null,?,?,?,?,?)"
            cursor.execute(query,list)
            self.connection.commit()
            cursor.close()
        except sqlite.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
        finally:
            if (self.connection):
                self.connection.close()
                print("The SQLite connection is closed")    
        '''
    
