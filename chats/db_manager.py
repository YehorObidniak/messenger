import mysql.connector
from time import time

class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def renew_connection(func):
        def inner(self, *args, **kwargs):
            self.conn = mysql.connector.connect(user='yehor', password='4vRes4^9mH', host='mysqlserver3.mysql.database.azure.com', database='messenger')
            self.cursor = self.conn.cursor()
            res = func(self, *args, **kwargs)
            self.cursor.close()
            self.conn.close()
            return res
        return inner

    @renew_connection
    def insert_message(self, tgid, from_user, text, chat_id, departmentName, typeOfMessage):
        insertion = 'INSERT INTO chats_message(tgid, from_user, text, chat_id, departmentName, typeOfMessage, time) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        values = (tgid, from_user, text, chat_id, departmentName, typeOfMessage, time())
        try:
            self.cursor.execute(insertion, values)
            self.conn.commit()
        except:
            print("message was not sended")

    @renew_connection
    def insert_chat(self, id, chat_name):
        insertion = 'INSERT IGNORE INTO chats_chat(id, chat_name) VALUES(%s, %s)'
        values = (id, chat_name)
        try:
            self.cursor.execute(insertion, values)
            self.conn.commit()
        except:
            print("chat was not created")

    @renew_connection
    def get_active_issues_by_chat(self, chat_id):
        query = f"SELECT id FROM chats_issue WHERE chat_id = {int(chat_id)} AND active = {1}"
        self.cursor.execute(query)
        try:
            res = [row[0] for row in self.cursor.fetchall()]
            return res
        except:
            print("can't get active issues")

    @renew_connection
    def get_responsiblePerson_by_issue(self, issue_id:list):
        tup = str(tuple(issue_id))
        query = f"SELECT responsiblePerson_id FROM chats_issue WHERE id IN {tup[:-2]+tup[-1:]}"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except:
            print("can't get responsible persons")

    @renew_connection
    def get_tgid_by_user_id(self, user_id):
        query = f"SELECT tgid FROM chats_users WHERE id = {user_id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    @renew_connection
    def get_chat_name_by_id(self, chat_id):
        query = f"SELECT chat_name FROM chats_chat WHERE id = {int(chat_id)}"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
