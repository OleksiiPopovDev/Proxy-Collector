from database.connector import Connector
from alive_progress import alive_bar
from view.view import View
from peewee import Model
from database.model.country_model import Country
from database.model.ip_model import IP
from database.model.status_model import Status
import os
import time


class Migration(Connector):
    __tables: dict[Model] = {
        'country': Country,
        'ip': IP,
        'status': Status
    }

    def run(self):
        if os.getenv('DB_TYPE') == 'SQLite':
            self.dump_sqlite_database()

        db = Connector.get_connection()
        db.drop_tables(self.__tables.values())

        with alive_bar(len(self.__tables)) as bar:
            for table_name in self.__tables:
                bar.title(
                    View.paint('\t{Yellow}Creating table{ColorOff} -> {BYellow}%s{ColorOff}' % table_name)
                )

                model = self.__tables[table_name]
                db.create_tables([model])

                print(View.paint(
                    '{Yellow}Created table {ColorOff} >> {BGreen}%s{ColorOff}' % table_name
                ))

                bar()
                time.sleep(0.3)

    @staticmethod
    def dump_sqlite_database():
        dump_directory: str = 'resources/dumps/'
        if not os.path.exists(dump_directory):
            os.makedirs(dump_directory)

        db_file: str = 'resources/%s.db' % os.getenv('DB_FILE_NAME')
        if os.path.isfile(db_file):
            os.rename(db_file, 'resources/dumps/%s_%s.db' % (os.getenv('DB_FILE_NAME'), time.time()))
