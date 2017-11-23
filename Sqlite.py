import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')

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



def read_from_db():
    c.execute("SELECT * FROM stufftoplot WHERE value > 2")
    for row in c.fetchall():
        print (row)


def graph_date():
    c.execute('SELECT unix, value FROM stufftoplot')
    dates = []
    value = []
    for row in c.fetchall():
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        value.append(row[1])

    plt.plot_date(dates,value, '-')
    plt.show()


def del_and_update():
    c.execute("SELECT * FROM stufftoplot")
    [print(row) for row in c.fetchall()]

    c.execute("UPDATE stufftoplot SET value = 99 WHERE value = 6.0")
    conn.commit()

    c.execute("SELECT * FROM stufftoplot")
    [print(row) for row in c.fetchall()]



del_and_update()


# create_table()
# for i in range(0,10):
#     dynamic_data_entry()
#     time.sleep(1)
#read_from_db()
# graph_date()

c.close()
conn.close()

