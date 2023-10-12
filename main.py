import requests
from bs4 import BeautifulSoup
import sqlite3


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            link TEXT
        )
    ''')


def iskat(query, conn):
    search_url = f"https://www.google.com/search?q={'+'.join(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        soxranit(links, conn)
        return links

    return []


def soxranit(links, conn):
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO results (link) VALUES (?)', [(link,) for link in links])
    conn.commit()


def vzyat_rezultati(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT link FROM results')
    return [row[0] for row in cursor.fetchall()]


if __name__ == "__main__":
    conn = sqlite3.connect('search_results.db')
    create_table(conn)

    while True:
        print("1. Выполнить поиск в Google")
        print("2. Показать сохраненные результаты")
        print("3. Выйти")
        print("4. Очистить базу данных")

        choice = input("Выберите действие: ")

        if choice == '1':
            query = input("Введите запрос: ")
            search_results = iskat([query], conn)
            print("Результаты поиска:")
            for link in enumerate(search_results):
                print(link)
        elif choice == '2':
            saved_results = vzyat_rezultati(conn)
            print("Сохраненные результаты:")
            for i, link in enumerate(saved_results):
                print(f"{i + 1}. {link}")
        elif choice == '3':
            conn.close()
            exit()
        elif choice == '4':
            cursor = conn.cursor()
            cursor.execute("DELETE FROM websites")
            conn.commit()