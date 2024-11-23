from LLM.db.client.client import MySQLConnection
from LLM.db.models.models import Base, User


class DBInteraction:
    def __init__(self, port, host, database, user, password, rebuild_db=False):
        self.mysql_connection = MySQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            rebuild_db=rebuild_db
        )
        self.engine = self.mysql_connection.connection.engine

        if rebuild_db:
            self.create_tables()

    def create_tables(self):
        try:
            Base.metadata.create_all(self.engine)  # Создаёт все таблицы
            print("All tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

    def add_user(self, username, password, email):
        user = User(
            username=username,
            password=password,
            email=email
        )
        self.mysql_connection.session.add(user)
        self.mysql_connection.session.commit()  # Фиксируем изменения
        return True
