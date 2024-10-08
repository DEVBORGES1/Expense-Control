# Do an SQlITE import
import sqlite3 as lite

con = lite.connect('DATA.db')

# 1- Categories
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Categories(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

# 2- Income
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Income(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL)")

# 3- expenses
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Expenses(id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")

