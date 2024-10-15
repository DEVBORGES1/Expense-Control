import sqlite3 as lite

# Database connection
con = lite.connect('DATA.db')

# Insert functions ---------

# Insert categories
def insert_categories(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categories (nome) VALUES (?)"
        cur.execute(query, (i)) 

# Insert income
def insert_Income(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Income (categoria, adicionado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)  

# Insert expenses
def insert_Expenses(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Expenses (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i) 

# Delete functions ---------

# Delete income
def delete_Income(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Income WHERE id=?"  
        cur.execute(query, (i))  

# Delete expenses
def delete_Expenses(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Expenses WHERE id=?"  
        cur.execute(query, (i)) 

# Functions to view data ---------

# View categories
def view_Categories():
    Item_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categories")
        rows = cur.fetchall()
        for row in rows:
            Item_list.append(row)
    
    return Item_list

# View income
def view_Income():
    Item_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Income")
        rows = cur.fetchall()
        for row in rows:
            Item_list.append(row)
    
    return Item_list

# View expenses
def view_Expenses():
    Item_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Expenses")
        rows = cur.fetchall()
        for row in rows:
            Item_list.append(row)
    
    return Item_list

# Combine expenses and income
def tabela():
    expenses = view_Expenses()
    income = view_Income()

    tabela_lista = []  

    for item in expenses:
        tabela_lista.append(item)
    
    for item in income:
        tabela_lista.append(item)

    return tabela_lista 

# Function to return income values for bar chart
def bar_valores():
    incomes = view_Income()  
    income_list = []  

    for item in incomes:
        income_list.append(item[3])  

    income_total = sum(income_list)  

    # Total das despesas
    Expenses = view_Expenses()  
    expenses_list = []  

    for item in Expenses:
        expenses_list.append(item[3])  

    expenses_total = sum(expenses_list) 

    # Total na conta (balanço)
    balance_total = income_total - expenses_total

    return [income_list, expenses_list, expenses_total, balance_total]
