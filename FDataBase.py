import sqlite3
from flask import flash

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def create(self, title, price, description):
        try:
            self.__cur.execute("INSERT INTO vechicle (title, description, price) VALUES(?,?,?)",
                               (title, description, price))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления автомобиля" + str(e))
            return False
        return True

    def get_cars(self):
        sql = '''SELECT * FROM vechicle'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addUser(self, name, email, password):
        try:
            self.__cur.execute(f"SELECT COUNT() AS 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False
            else:
                self.__cur.execute("INSERT INTO users VALUES(NULL, ?,?,?, NULL)", (name, email, password))
                self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя" + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных" + str(e))
        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE EMAIL = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных' + str(e))
        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar =? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления аватара в БД: " + str(e))
            return False
        return True

