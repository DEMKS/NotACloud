# -*- coding: utf-8 -*-
import sqlite3
#Подключение к базе
conn = sqlite3.connect('NotADevs.db')
#Создание курсора
c = conn.cursor()
#Создание таблицы
c.execute('''DROP TABLE users''')
c.execute('''DROP TABLE tokens''')
c.execute('''CREATE TABLE users (id  INTEGER PRIMARY KEY ,login string, password string, space INTEGER DEFAULT 51200)''')
c.execute('''CREATE TABLE tokens (id INTEGER PRIMARY KEY ,token string, time string, user_id)''')
#Подтверждение отправки данных в базу
conn.commit()
c.close()
conn.close()