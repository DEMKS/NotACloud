# -*- coding: utf-8 -*-
import sqlite3
#Подключение к базе
conn = sqlite3.connect('../NotADevs.db')
#Создание курсора
c = conn.cursor()
#Создание таблицы
try:
    c.execute('''DROP TABLE users''')
except:
    print("Таблица users не найдена")
try:
    c.execute('''DROP TABLE tokens''')
except:
    print("Таблица tokens не найдена")
c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, login VARCHAR(200), password VARCHAR(200), login_unhashed VARCHAR(200),space INTEGER DEFAULT 100);''')
c.execute('''CREATE TABLE tokens (id INTEGER PRIMARY KEY, token string, ttime string, user_id)''')
#Подтверждение отправки данных в базу
conn.commit()
c.close()
conn.close()