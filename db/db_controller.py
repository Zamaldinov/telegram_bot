from typing import List, Any

import sqlalchemy as db
from db.utils import get_time_now


class DB_Controller:
    """Класс для БД, создаю в нем три БД, история, регионы и юзеры"""
    def __init__(self):
        self.engine = db.create_engine('sqlite:///database.db')
        self.conn = self.engine.connect()

    metadata = db.MetaData()

    history = db.Table('history', metadata,
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer, nullable=False),
                       db.Column('created_at', db.Date, nullable=False, default=get_time_now()),
                       db.Column('command', db.String, nullable=False))

    regions = db.Table('region', metadata,
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('name_region', db.String, nullable=False, unique=True))

    users = db.Table('user', metadata,
                     db.Column('id', db.Integer, unique=True),
                     db.Column('region_id', db.Integer, default=1))

    def get_all_regions(self):
        """Возвращает все регионы, которые имеются в БД"""
        select_table_regions = db.select(self.regions)
        result = self.conn.execute(select_table_regions)
        return result.fetchall()

    def create_all_tables(self):
        """Добавление регионов в БД regions"""
        try:
            self.metadata.create_all(self.conn)
            insertion_query = self.regions.insert().values([{'name_region': 'world'},
                                                        {'name_region': 'russia'},
                                                        {'name_region': 'ukraine'},
                                                        {'name_region': 'belarus'},
                                                        {'name_region': 'kazakhstan'}])
            self.conn.execute(insertion_query)
            self.conn.commit()
        except db.exc.IntegrityError:
            pass

    def add_history(self, user_id: int, command: str) -> None:
        """Добавление записи в БД history, об использованных командах"""
        self.delete_history(user_id)
        insertion_query = self.history.insert().values([{'user_id': user_id, 'command': command}])
        self.conn.execute(insertion_query)
        self.conn.commit()

    def add_user(self, user_id):
        """Добавление ID пользователя в БД users"""
        try:
            insertion_user = self.users.insert().values([{'id': user_id}])
            self.conn.execute(insertion_user)
            self.conn.commit()
        except db.exc.IntegrityError:
            pass

    def get_user_region(self, user_id: int):
        """Получаем из БД регион, который указан у пользователя"""
        select_user_result = self.get_user(user_id)
        select_region = db.select(self.regions).where(self.regions.columns.name_region == select_user_result[0][1])
        select_region_result = self.conn.execute(select_region)
        return select_region_result.fetchall()[0][1]

    def get_user_history(self, user_id: int) -> Any:
        """Получаем историю об использованных командах"""
        select_user_history = db.select(self.history).where(self.history.columns.user_id == user_id)
        select_result = self.conn.execute(select_user_history)
        return_result = ''
        count_line = 1
        for i_line in select_result.fetchall():
            return_result += str(count_line) + '. ' + i_line[3] + '\n'
            count_line += 1
        return return_result

    def change_region(self, user_id: int, region_id: int) -> None:
        """Смена региона у пользователя"""
        update_region_user = self.users.update().where(self.users.columns.id == user_id).values(region_id=region_id)
        self.conn.execute(update_region_user)
        self.conn.commit()

    def delete_history(self, user_id: int) -> None:
        """Удаление самой старой записи из истории, если размер истории составляет 10 записей"""
        select_table_history = db.select(self.history).where(self.history.columns.user_id == user_id)
        select_results = self.conn.execute(select_table_history)
        select_list = select_results.fetchall()
        select_size = len(select_list)
        if select_size == 10:
            first_id = select_list[0].id
            delete_query = db.delete(self.history).where(self.history.columns.id == first_id)
            self.conn.execute(delete_query)
            self.conn.commit()

    def delete_all_history(self, user_id):
        """Удаляет всю историю юзера, ее не стал реализовывать для общего доступа, написал просто для собственного удобства"""
        delete = db.delete(self.history).where(self.history.columns.user_id == user_id)
        self.conn.execute(delete)
        self.conn.commit()

    def get_all_users(self):
        """Возвращает всех юзеров из БД, тоже сдалал для собственного удобства"""
        select_table_regions = db.select(self.users)
        result = self.conn.execute(select_table_regions)
        for i in result.fetchall():
            print(i)
        return result.fetchall()

    def get_user(self, user_id):
        """Возвращает юзера"""
        select_user = db.select(self.users).where(self.users.columns.id == user_id)
        res = self.conn.execute(select_user)
        res = res.fetchall()
        return res
