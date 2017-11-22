import sqlite3
import time
import datetime
import random


conn = sqlite3.connect('tutorial.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stufftoplot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')

def data_entry():
    c.execute("INSERT INTO stufftoplot VALUES(10, '54544', 'python', 8)")
    conn.commit()
    c.close()
    conn.close()


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
    keyword = 'python'
    value = random.randrange(0,10)
    c.execute("INSERT INTO stufftoplot (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
              (unix, date, keyword, value))
    conn.commit()


create_table()
#data_entry()

for i in range(0,10):
    dynamic_data_entry()
    time.sleep(1)
c.close()
conn.close()

