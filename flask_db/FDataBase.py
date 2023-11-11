import math
import sqlite3
import time
import re
from flask import url_for


class FDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def getMenu(self):
        sql = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Error reading from DataBase")
        return []
    

    def addPost(self, title, text, url):
        try:
            self.__cur.execute( f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'" )
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("The article with this URL already exists.")
                return False
            
            base = url_for('static', filename='pic')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>", "\\g<tag>" + base + "/\\g<url>>" + ".files", text)

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", \
                               (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding article to DataBase " + str(e))
            return False
        
        return True
    

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error retrieving article from DataBase " + str(e))

        return (False, False)
    

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Error retrieving article from DataBase " + str(e))

        return []
    

    def addFeedback(self, username, email, message):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO feedbacks VALUES(NULL, ?, ?, ?, ?)", (username, email, message, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error adding feedback to DataBase " + str(e))
            return False
        
        return True


    def getFeedback(self, feedbackId):
        try:
            self.__cur.execute(f"SELECT username, email, message, tm FROM feedbacks WHERE id = {feedbackId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error retrieving faadbacks from DataBase " + str(e))

        return (False, False, False, False)

    
    def getFeedbacksAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, username, email, message FROM feedbacks ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                print(res)
                return res
        except sqlite3.Error as e:
            print(f"Error retrieving feedbacks from DataBase " + str(e))

        return []
    

    def addUser(self, username, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` from users WHERE email like '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("A user with this email already exists")
                return False
    
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", \
                            (username, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error when adding a user to the DataBase" + str(e))
            return False

        return True
    

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
    
            return res
        except sqlite3.Error as e:
            print("Error when getting a user from the DataBase" + str(e))
        
        return False
    

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("User not found")
                return False
            
            return res
        except sqlite3.Error as e:
            print("Error when getting userdata from the DataBase" + str(e))

        return False
            

