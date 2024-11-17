from config.config import config
from src.DBManager import DBManager
from src.Vacancy import Vacancy
from src.hh_info import HH


def main() -> None:
    """Функция сборки проекта"""
    params = config()
    bd_user = input("Напиши названия своей базы данных ")
    db = DBManager(bd_user, params)
    hh = HH()
    user_vacancies = input("Введи слово, по которому искать вакансии ")
    vacancies = []
    for vacancy in hh.vacancies:
        vacancies.append(Vacancy.vacancy_from_hh(vacancy))
    db.add_vacancies(vacancies)

    if input("Тебе надо посчитать количество вакансий у каждой компании? [y/n]").lower().strip() == "y":
        print(db.get_companies_and_vacancies_count())

    if input("Тебе надо вывести название, зарплату и ссылку вакансии? [y/n]").lower().strip() == "y":
        print(db.get_all_vacancies())

    if input("Тебе надо вывести среднюю зарплату по вакансиям? [y/n]").lower().strip() == "y":
        print(db.get_avg_salary())

    if input("Тебе надо вывести вакансии, у которых зп выше средней? [y/n]").lower().strip() == "y":
        print(db.get_vacancies_with_higher_salary())

    if input("Тебе надо вывести вакансии, в названии которых есть введенное слово? [y/n]").lower().strip() == "y":
        print(db.get_vacancies_with_keyword(input("Введи слово: ")))


if __name__ == '__main__':
    main()
