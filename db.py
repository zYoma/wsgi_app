# -*- coding: utf-8 -*-
import sqlite3
import os

DB_FILE_NAME = 'DB.db'

def check_db():
    """Функция проверяет наличие файла БД в директории с проектом.
       Возвращает булевое значение в зависимости от результата.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    fullname = os.path.join(BASE_DIR, DB_FILE_NAME)
    if os.path.exists(fullname):
        return True

    return False


def create_db(cursor):
    """Функция создает основные таблицы для работы приложения"""
    cursor.execute('''CREATE TABLE region
        (region_id INTEGER PRIMARY KEY,
        name varchar(30) NOT NULL)''')

    cursor.execute('''CREATE TABLE city
        (city_id INTEGER PRIMARY KEY,
        name varchar(30) NOT NULL,
        region INTEGER NOT NULL,
        FOREIGN KEY(region) REFERENCES region(region_id))''')

    cursor.execute('''CREATE TABLE comments
        (comment_id INTEGER PRIMARY KEY,
        first_name varchar(30) NOT NULL,
        last_name varchar(30) NOT NULL,
        patronymic varchar(30),
        tel varchar(30),
        email varchar(30),
        comment text NOT NULL,
        region INTEGER,
        city INTEGER,
        FOREIGN KEY(region) REFERENCES region(region_id),
        FOREIGN KEY(city) REFERENCES city(city_id))''')


def create_citys_and_regions(conn, cursor):
    """Функция наполняет таблицы region и city исходными данными."""
    conn.text_factory = str
    regions = [
        (1, 'Краснодарский край'),
        (2, 'Ростовская область'),
        (3, 'Ставропольский край'),
    ]

    citys = [
        (1, 'Краснодар', 1),
        (2, 'Кропоткин', 1),
        (3, 'Славянск', 1),
        (4, 'Ростов', 2),
        (5, 'Шахты', 2),
        (6, 'Батайск', 2),
        (7, 'Ставрополь', 3),
        (8, 'Пятигорск', 3),
        (9, 'Кисловодск', 3),
    ]
     
    cursor.executemany("INSERT INTO region (region_id, name) VALUES (?, ?)", regions)
    cursor.executemany("INSERT INTO city (city_id, name, region) VALUES (?, ?, ?)", citys)
    conn.commit()


def connect():
    """Подключение к БД"""
    return sqlite3.connect(DB_FILE_NAME)

def DBconnect():
    """При обращении, функция проверяет, существует ли БД.
       Если БД нет, создает ее и наполняет исходными данными.
       Если БД существует, возвращает объект соеденения с БД для дальнейшего использования.
    """
    is_exsist = check_db()
    if is_exsist:
        conn = connect()
        return conn
    else:
        conn = connect()
        cursor = conn.cursor()
        create_db(cursor)
        create_citys_and_regions(conn, cursor)
        return conn


if __name__ == '__main__':
    DBconnect()