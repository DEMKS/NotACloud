import mysql
from mysql import connector
DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
cursor = DB.cursor(buffered=True)
cursor.execute("use userinfo;")
cursor.execute('INSERT INTO users VALUES(2, "123", "123", "123", 123)')

DB.commit()
cursor.close()
DB.close()