import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style
style.use('fivethirtyeight')

conn = sqlite3.connect('Revit_test.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS yoGaz_testing (testing1 TEXT, testing2 TEXT, testing3 TEXT, testing4 TEXT)')

create_table()


def dynamic_data_entry():
    t = 'testingdsds'
    y = 'fdshsjfgsjfgshdfg'
    j = 'python'
    k = random.randrange(0,10)
    c.execute("INSERT INTO yoGaz_testing (testing1, testing2, testing3, testing4) VALUES (?, ?, ?, ?)",
              (t, y, j, k))
    conn.commit()


for i in range(0,30):
    dynamic_data_entry()

c.close()
conn.close()

