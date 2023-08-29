import os
from peewee import Model, SqliteDatabase, MySQLDatabase
from dotenv import load_dotenv


class Connector:
    @staticmethod
    def get_connection():
        load_dotenv()
        if os.getenv('DB_TYPE') == 'MySQL':
            return MySQLDatabase(
                host=os.getenv('MYSQL_HOST'),
                port=int(os.getenv('MYSQL_PORT')),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASS'),
                database=os.getenv('DB_FILE_NAME')
            )

        if os.getenv('DB_TYPE') == 'SQLite':
            return SqliteDatabase('database/%s.db' % os.getenv('DB_FILE_NAME'))

        raise RuntimeError('Set correct type database in your .env file')


class BaseModel(Model):
    class Meta:
        database = Connector.get_connection()
