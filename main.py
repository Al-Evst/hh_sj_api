import os
import requests
import argparse
from dotenv import load_dotenv
from terminaltables import AsciiTable

def get_hh_vacancies(text="программист", area=1, per_page=100):
    vacancies = []
    total_vacancies = 0
    page = 0
    total_pages = 1

    while page < total_pages:
        try:
            params = {"text": text, "area": area, "per_page": per_page, "page": page}
            response = requests.get(hh_url, params=params)
            response.raise_for_status()
            hh_response = response.json()

            hh_vacancies = hh_response.get("items", [])
            total_vacancies = hh_response.get("found", 0)
            total_pages = hh_response.get("pages", 1)

            if not hh_vacancies:
                break

            vacancies.extend(hh_vacancies)
            page += 1
        except requests.RequestException as req_err:
            print(f"Ошибка запроса к HeadHunter: {req_err}")
            break

    return vacancies, total_vacancies

def get_sj_vacancies(city="Москва", keyword="программист", count=100):
    vacancies = []
    total_vacancies = 0
    page = 0

    while True:
        try:
            params = {"keyword": keyword, "town": city, "count": count, "page": page}
            response = requests.get(sj_url, headers=sj_headers, params=params)
            response.raise_for_status()
            sj_response = response.json()

            sj_vacancies = sj_response.get("objects", [])
            total_vacancies = sj_response.get("total", 0)

            if not sj_vacancies:
                break

            vacancies.extend(sj_vacancies)
            page += 1
        except requests.RequestException as req_err:
            print(f"Ошибка запроса к SuperJob: {req_err}")
            break

    return vacancies, total_vacancies

def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8

def predict_rub_salary_hh(vacancy):
    salary_details = vacancy.get("salary")
    if not salary_details or salary_details.get("currency") != 'RUR':
        return
    return predict_salary(salary_details.get("from"), salary_details.get("to"))

def predict_rub_salary_sj(vacancy):
    payment_from = vacancy.get("payment_from")
    payment_to = vacancy.get("payment_to")
    if vacancy.get("currency") != "rub":
        return
    return predict_salary(payment_from, payment_to)

def calculate_average_salary_for_languages(languages, vacancy_source, predict_func):
    average_salaries = {}

    for lang in languages:
        vacancies, total_vacancies = vacancy_source(lang)
        if not vacancies:
            continue

        total_salary = 0
        vacancies_processed = 0

        for vacancy in vacancies:
            salary = predict_func(vacancy)
            if salary:
                total_salary += salary
                vacancies_processed += 1

        average_salaries[lang] = {
            "vacancies_found": total_vacancies,
            "vacancies_processed": vacancies_processed,
            "average_salary": int(total_salary / vacancies_processed) if vacancies_processed else 0,
        }
    return average_salaries

def print_salary_table(statistics, source_name):
    table_data = [
        ["Язык", "Найдено вакансий", "Обработано вакансий", "Средняя зарплата (руб.)"]
    ]
    for lang, data in statistics.items():
        table_data.append([
            lang,
            data["vacancies_found"],
            data["vacancies_processed"],
            data["average_salary"]
        ])

    table = AsciiTable(table_data)
    print(f"\nСредние зарплаты по языкам программирования ({source_name}):")
    print(table.table)

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Парсер вакансий с HeadHunter и SuperJob")
    parser.add_argument(
        "--sj_key",
        help="API ключ SuperJob (можно задать через переменную окружения SJ_KEY)",
        default=os.getenv("SJ_KEY")
    )
    args = parser.parse_args()

    sj_api_key = args.sj_key
    if not sj_api_key:
        print("Ошибка: необходимо указать API ключ SuperJob через аргумент --sj_key или переменную окружения SJ_KEY")
        exit(1)

    hh_url = "https://api.hh.ru/vacancies"
    sj_url = "https://api.superjob.ru/2.0/vacancies/"
    sj_headers = {"X-Api-App-Id": sj_api_key}

    languages = [
        "Python", "Java", "JavaScript", "C++", "C#", "PHP", "Go", "Swift", "Kotlin", "Ruby"
    ]

    hh_salaries = calculate_average_salary_for_languages(languages, get_hh_vacancies, predict_rub_salary_hh)
    print_salary_table(hh_salaries, "HeadHunter")

    sj_salaries = calculate_average_salary_for_languages(languages, get_sj_vacancies, predict_rub_salary_sj)
    print_salary_table(sj_salaries, "SuperJob")
