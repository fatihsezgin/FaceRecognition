import sqlite3 as sqlite


#db = sqlite.connect('database.db') #GNU/Linux

class database():
    def __init__(self):
        super(database,self).__init__()
        self.connection = sqlite.connect('/home/fatih/Desktop/Python/SoftwareDesingApplicationsFinal/FaceRecognition/database.db')

    def insertStudent(self,studentName,studentSurname,studentNumber,faculty,department):
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

    
