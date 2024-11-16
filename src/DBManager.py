import psycopg2

from src.Vacancy import Vacancy
from config.config import config


class DBManager:
    """Класс, который подключается к БД PostgreSQL"""

    def __init__(self, database_name: str, params: dict):
        """Метод инициализации"""
        self.database_name = database_name
        self.params = params

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE {database_name}')

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                           CREATE TABLE IF NOT EXISTS employers (
                               id SERIAL PRIMARY KEY,
                               employer_name TEXT NOT NULL UNIQUE
                           )
                       """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        link VARCHAR(255),
                        salary FLOAT,
                        requirement TEXT,
                        employer_id INTEGER REFERENCES employers(id)
                    )
                """)
        conn.commit()
        conn.close()

    def in_employers(self, employer_name: str) -> bool:
        """Функция проверки наличия компании"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()

        cur.execute(
            f"""
            SELECT EXISTS(SELECT 1 FROM employers WHERE employer_name = '{employer_name}');
            """
        )
        return cur.fetchone()[0]

    def add_vacancies(self, data: list[Vacancy]):
        """Метод добавления вакансий в БД"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        for vacancy in data:
            if not self.in_employers(vacancy.employer_name):
                cur.execute(
                    """
                    INSERT INTO employers (employer_name)
                    VALUES (%s)
                    RETURNING *
                    """, vacancy.employer_name)
                id_ = cur.fetchone()[0]
            else:
                cur.execute(
                    f"""
                    SELECT id FROM employers WHERE employer_name = '{vacancy.employer_name}'
                    """
                )
                id_ = cur.fetchone()[0]
            print(id_)
            cur.execute(
                """
                INSERT INTO vacancies (name, link, salary, requirement, employer_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """, [vacancy.name, vacancy.link, vacancy.salary, vacancy.requirement, id_])
        conn.commit()
        conn.close()


params = {"host": "localhost",
          "user": "postgres",
          "password": "7627",
          "port": "5432"}
bd_name = "python"
db = DBManager(bd_name, params)
db.add_vacancies([Vacancy("df", "sdf", 0, "sdf", "d"),
                  Vacancy("dfs", "sdf", 0, "fdg", "gf")])
