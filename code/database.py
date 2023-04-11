import datetime
import sqlite3


class Database:
    def __init__(self, file_path: str):
        try:
            self.connection = sqlite3.connect(file_path)
        except Exception as ex:
            print(f'EXCEPTION: {ex}')


# Moderation

    def create_moderation_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS penalties (id INTEGER PRIMARY KEY AUTOINCREMENT, type INTEGER NOT NULL, server_id INTEGER NOT NULL, user_id INTEGER NOT NULL , moderator_id INTEGER NOT NULL, reason TEXT NOT NULL, end_date INTEGER);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_penalty(self, type: int, server_id: int, user_id: int, moderator_id: int, reason: str, penalty_end: datetime.datetime = None):
        # {(', end_date' if penalty_end != None else '')} / f', {penalty_end}' if penalty_end != None else ''}
        cursor = self.connection.cursor()

        if penalty_end != None:
            cursor.execute(
                f'INSERT INTO penalties (type, server_id, user_id, moderator_id, reason, end_date) VALUES ({type}, {server_id}, {user_id}, {moderator_id}, \'{reason}\', {penalty_end.timestamp()});')
        else:
            cursor.execute(
                f'INSERT INTO penalties (type, server_id, user_id, moderator_id, reason) VALUES ({type}, {server_id}, {user_id}, {moderator_id}, \'{reason}\');')
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


# Teammember

    def create_team_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS team (id INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER NOT NULL, role TEXT NOT NULL);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_member(self, userid: int, role: str):
        cursor = self.connection.cursor()

        cursor.execute(
            f'INSERT INTO team (userid, role) VALUES (?, ?);', (userid, role))
        self.connection.commit()

    def delete_member(self, userid: int):
        cursor = self.connection.cursor()
        cursor.execute(
            f'DELETE FROM team WHERE userid={userid};')
        self.connection.commit()

    def get_member_by_coowner(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_admin(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_manager(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_eventmanager(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_headmod(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_mod(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_supp(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_builder(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_cutter(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_member_by_designer(self, role: str):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team WHERE role=?', (role,)).fetchall()

    def get_all_member(self):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM team ').fetchall()


# Ticket


    def drop_ticketdb(self):
        cursor = self.connection.cursor()

        cursor.execute(
            f'DROP TABLE tickets;')
        self.connection.commit()

    def create_ticket_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_channel_id BIGINT, user_id INTEGER NOT NULL, moderator_id INTEGER, create_date INTEGER);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_ticket(self, user_id: int, create_date: int):
        cursor = self.connection.cursor()

        cursor.execute(
            f'INSERT INTO tickets (user_id, create_date) VALUES (?, ?);', (user_id, create_date))
        self.connection.commit()

    def update_ticket(self, ticket_channel_id: int, id: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE tickets SET ticket_channel_id=? WHERE id=?;', (ticket_channel_id, id))
        self.connection.commit()

    def update_claimed_ticket(self, moderator_id: int, ticket_channel_id: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE tickets SET moderator_id=? WHERE ticket_channel_id=?;', (moderator_id, ticket_channel_id))
        self.connection.commit()

    def get_ticket_id(self, create_date: int) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT id FROM tickets WHERE create_date={create_date};').fetchone()[0]

    def get_ticket_id_by_channel_id(self, channel_id: int) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT id FROM tickets WHERE ticket_channel_id={channel_id};').fetchone()[0]

    def get_ticket_info(self, id: int):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM tickets WHERE id=?;', (id, )).fetchone()


# Entbannungsanträge


    def drop_appealdb(self):
        cursor = self.connection.cursor()

        cursor.execute(
            f'DROP TABLE appeals;')
        self.connection.commit()

    def create_appeal_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS appeals (id INTEGER PRIMARY KEY AUTOINCREMENT, appeal_channel_id BIGINT, user_id INTEGER NOT NULL, moderator_id INTEGER, create_date INTEGER);')

            self.connection.commit()
        except Exception as ex:
            print(f'EXCEPTION: {ex}')

    def create_appeal(self, user_id: int, create_date: int):
        cursor = self.connection.cursor()

        cursor.execute(
            f'INSERT INTO appeals (user_id, create_date) VALUES (?, ?);', (user_id, create_date))
        self.connection.commit()

    def update_appeal(self, appeal_channel_id: int, id: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE appeals SET appeal_channel_id=? WHERE id=?;', (appeal_channel_id, id))
        self.connection.commit()

    def update_claimed_appeal(self, moderator_id: int, appeal_channel_id: int):
        cursor = self.connection.cursor()

        cursor.execute(
            'UPDATE appeals SET moderator_id=? WHERE appeal_channel_id=?;', (moderator_id, appeal_channel_id))
        self.connection.commit()

    def get_appeal_id(self, create_date: int) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT id FROM appeals WHERE create_date={create_date};').fetchone()[0]

    def get_appeal_id_by_channel_id(self, channel_id: int) -> int:
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT id FROM appeals WHERE appeal_channel_id={channel_id};').fetchone()[0]

    def get_appeal_info(self, id: int):
        cursor = self.connection.cursor()
        return cursor.execute(
            f'SELECT * FROM appeals WHERE id=?;', (id, )).fetchone()
