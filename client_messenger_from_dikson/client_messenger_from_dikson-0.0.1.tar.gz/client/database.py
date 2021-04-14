import datetime
import os

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientDatabase:
    """Класс работы с БД для клиентской части приложения, создает все необходимые таблицы"""

    class KnownUsers:
        """Класс для создания таблицы ВСЕХ ПОЛЬЗОВАТЕЛЕЙ"""

        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageStat:
        """Класс для создания таблицы СТАТИСТИКИ СООБЩЕНИЙ"""

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Класс для создания таблицы КОНТАКТОВ"""

        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        """Конструктор класса:
        Создание "движка" базы данных, каждый контакт должен иметь свою БД.
        Поскольку клиентская часть мультипоточная необходимо отключить
        проверки на подключения с разных потоков,
        иначе ОШИБКА - sqlite3.ProgrammingError"""
        path = os.getcwd()
        filename = f'client_{name}.db3'
        self.database_engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создание модели таблицы известных пользователей
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        # Создание модели таблицы истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        # Создание модели таблицы контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        # Создаём таблицы в БД
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.KnownUsers, users)
        mapper(self.MessageStat, history)
        mapper(self.Contacts, contacts)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Необходимо очистить таблицу контактов, т.к. при запуске они
        # подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """Метод для добавления КОНТАКТА в БД."""
        if not self.session.query(
                self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        """Метод для очистки таблицы со списком контактов."""
        self.session.query(self.Contacts).delete()

    def del_contact(self, contact):
        """Метод для удаления выбранного контакта."""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """Метод, заполняющий таблицу известных пользователей."""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """Метод, сохраняющий сообщения в базу данных."""
        message_row = self.MessageStat(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """Метод для получения списка всех контактов"""
        return [contact[0]
                for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """Метод получения списка всех имеющихся пользователей."""
        return [user[0]
                for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """Метод проверки - существует ли пользователь."""
        if self.session.query(
                self.KnownUsers).filter_by(username=user).count():
            return True
        return False

    def check_contact(self, contact):
        """Метод проверки на существование контакта"""
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        return False

    def get_history(self, contact):
        """Метод получения истории сообщений определенного пользователя."""
        query = self.session.query(
            self.MessageStat).filter_by(
            contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.date) for history_row in query.all()]


# тестирование
if __name__ == '__main__':
    test_db = ClientDatabase('user_test_1')
    print(sorted(test_db.get_history('user_test_2'), key=lambda item: item[3]))
