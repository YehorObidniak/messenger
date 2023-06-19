import mysql.connector

class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def renew_connection(func):
        def inner(self, *args, **kwargs):
            self.conn = mysql.connector.connect(user='yehor', password='4vRes4^9mH', host='mysqlserver3.mysql.database.azure.com', database='messenger')
            self.cursor = self.conn.cursor()
            func(self, *args, **kwargs)
            self.cursor.close()
            self.conn.close()
        return inner

    @renew_connection
    def insert_message(self, tgid, from_user, text, chat_id, departmentName):
        insertion = 'INSERT INTO chats_message(tgid, from_user, text, chat_id, departmentName) VALUES(%s, %s, %s, %s, %s)'
        values = (tgid, from_user, text, chat_id, departmentName)
        self.cursor.execute(insertion, values)
        self.conn.commit()

    @renew_connection
    def insert_chat(self, id, chat_name):
        insertion = 'INSERT IGNORE INTO chats_chat(id, chat_name) VALUES(%s, %s)'
        values = (id, chat_name)
        self.cursor.execute(insertion, values)
        self.conn.commit()