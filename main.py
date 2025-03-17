import os
import requests
import argparse
from dotenv import load_dotenv
from terminaltables import AsciiTable



def get_hh_vacancies(text="программист", area=1, per_page=100):
    vacancies = []
    page = 0
    while True:
        try:
            params = {"text": text, "area": area, "per_page": per_page, "page": page}
            response = requests.get(hh_url, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            if not items:
                break
            vacancies.extend(items)
            page += 1
            if page > 19:
                break
        except requests.HTTPError as http_err:
            print(f"HTTP ошибка при запросе к HeadHunter1: {http_err}")
            break
        except requests.ConnectionError as conn_err:
            print(f"Ошибка соединения при запросе к HeadHunter: {conn_err}")
            break
        except requests.Timeout as timeout_err:
            print(f"Таймаут при запросе к HeadHunter: {timeout_err}")
            break
        except requests.RequestException as req_err:
            print(f"Ошибка запроса к HeadHunter: {req_err}")
            break
    return vacancies

def get_sj_vacancies(city="Москва", keyword="программист", count=100):
    vacancies = []
    page = 0
    while True:
        try:
            params = {"keyword": keyword, "town": city, "count": count, "page": page}
            response = requests.get(sj_url, headers=sj_headers, params=params)
            response.raise_for_status()
            data = response.json()
            objects = data.get("objects", [])
            if not objects:
                break
            vacancies.extend(objects)
            page += 1
        except requests.HTTPError as http_err:
            print(f"HTTP ошибка при запросе к SuperJob: {http_err}")
            break
        except requests.ConnectionError as conn_err:
            print(f"Ошибка соединения при запросе к SuperJob: {conn_err}")
            break
        except requests.Timeout as timeout_err:
            print(f"Таймаут при запросе к SuperJob: {timeout_err}")
            break
        except requests.RequestException as req_err:
            print(f"Ошибка запроса к SuperJob: {req_err}")
            break
    return vacancies

def predict_salary(salary_from, salary_to):
    try:
        if salary_from and salary_to:
            return (salary_from + salary_to) / 2
        elif salary_from:
            return salary_from * 1.2
        elif salary_to:
            return salary_to * 0.8
    except TypeError as type_err:
        print(f"Ошибка обработки зарплаты: {type_err}")

def predict_rub_salary_hh(vacancy):
    salary_info = vacancy.get("salary")
    if not salary_info or not salary_info.get("currency") == 'RUR':
        return None
    return predict_salary(salary_info.get("from"), salary_info.get("to"))

def predict_rub_salary_sj(vacancy):
    payment_from = vacancy.get("payment_from")
    payment_to = vacancy.get("payment_to")
    currency = vacancy.get("currency")
    if not currency == "rub":
        return None
    return predict_salary(payment_from, payment_to)
    

def calculate_average_salary_for_languages(languages, source, predict_func):
    average_salaries = {}
    for lang in languages:
        try:
            vacancies = source(lang)
            if vacancies:
                total_salary = 0
                vacancies_processed = 0
                for vacancy in vacancies:
                    salary = predict_func(vacancy)
                    if salary:
                        total_salary += salary
                        vacancies_processed += 1
                average_salary = int(total_salary / vacancies_processed) if vacancies_processed else 0
                average_salaries[lang] = {
                    "vacancies_found": len(vacancies),
                    "vacancies_processed": vacancies_processed,
                    "average_salary": average_salary,
                }
        except ZeroDivisionError as zero_err:
            print(f"Ошибка деления на ноль при обработке данных для {lang}: {zero_err}")
        except TypeError as type_err:
            print(f"Ошибка типа данных при обработке данных для {lang}: {type_err}")
    return average_salaries

def print_salary_table(statistics, source_name):
    table_data = [
        ["Язык", "Найдено вакансий", "Обработано вакансий", "Средняя зарплата (руб.)"]
    ]
    for lang, data in statistics.items():
        table_data.append([lang, data["vacancies_found"], data["vacancies_processed"], data["average_salary"]])
    
    table = AsciiTable(table_data)
    print(f"\nСредние зарплаты по языкам программирования ({source_name}):")
    print(table.table)

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Парсер вакансий с HeadHunter и SuperJob")
    parser.add_argument("--sj_key", help="API ключ SuperJob (можно задать через переменную окружения SJ_KEY)")
    args = parser.parse_args()
    
    sj_api_key = args.sj_key or os.getenv("SJ_KEY")
    if not sj_api_key:
        print("Ошибка: необходимо указать API ключ SuperJob через аргумент --sj_api_key или переменную окружения SJ_KEY")
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
