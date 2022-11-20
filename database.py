import sqlite3


class Database:
    def __init__(self, file_path: str):
        try:
            self.connection = sqlite3.connect(file_path)
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS penalties (id INTEGER PRIMARY KEY AUTOINCREMENT, type INTEGER NOT NULL, server_id INTEGER NOT NULL, user_id INTEGER NOT NULL , moderator_id INTEGER NOT NULL, reason TEXT NOT NULL, end_date INTEGER);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_penalty(self, type: int, server_id: int, user_id: int, moderator_id: int, reason: str):
        print(f'Create with reason: {reason}')
        cursor = self.connection.cursor()
        cursor.execute(
            f'INSERT INTO penalties (type, server_id, user_id, moderator_id, reason, end_date) VALUES ({type}, {server_id}, {user_id}, {moderator_id}, \'{reason}\', 0);')
        self.connection.commit()

    def delete_penalty(self, type: int, server_id: int, user_id: int):
        cursor = self.connection.cursor()
        cursor.execute(
            f'DELETE FROM penalties WHERE id IN (SELECT id FROM penalties WHERE type={type} AND server_id={server_id} AND user_id={user_id} ORDER BY id DESC LIMIT 1) ;')
        self.connection.commit()

    def get_penalties_by_user(self, server_id: int, user_id: int):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM penalties WHERE server_id={server_id} AND user_id={user_id} ORDER BY id DESC LIMIT 25;').fetchall()
