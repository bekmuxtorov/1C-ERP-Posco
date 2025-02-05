import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Users (
            username VARCHAR(255) NULL,
            password VARCHAR(255) NULL,
            phone_number VARCHAR(255) NOT NULL,
            language_code VARCHAR(10) NULL,
            chat_id VARCHAR(255) NOT NULL,
            PRIMARY KEY (chat_id)
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, username: str, password: str, language_code, phone_number: str, chat_id: str):
        try:
            sql = """
            INSERT INTO Users(username, password, language_code, phone_number, chat_id) VALUES(?, ?, ?, ?, ?)
            """
            self.execute(sql, parameters=(username, password,
                         language_code, phone_number, chat_id), commit=True)
            status = True
        except:
            status = False
        return status

    def add_employee(self, phone_number: str, language_code: str, chat_id: str):
        try:
            sql = """
                INSERT INTO Users(phone_number, language_code, chat_id) VALUES(?, ?, ?)
                """
            print()
            self.execute(sql, parameters=(
                phone_number, language_code, chat_id), commit=True)
            status = True
        except:
            status = False
        return status

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        response = self.execute(sql, parameters=parameters, fetchone=True)
        return {
            "username": response[0],
            "password": response[1],
            "phone_number": response[2],
            "language_code": response[3],
            "chat_id": response[4]
        } if response else None

    async def select_language_code(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        response = self.execute(sql, parameters=parameters, fetchone=True)
        return {
            "language_code": response[3],
        } if response else None

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    async def delete_user(self, **kwargs):
        sql = "DELETE FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        # self.execute(sql, parameters=parameters, fetchone=True)
        self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
