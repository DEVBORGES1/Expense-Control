import sqlite3 as lite
import pandas as pd

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
    incomes = view_Income()  # Recupera os valores de renda
    income_list = []  # Lista para armazenar os valores de renda

    for item in incomes:
        income_list.append(item[3])  # Acessa o valor de renda (ajuste conforme sua estrutura)

    income_total = sum(income_list)  # Calcula o total de renda

    # Total das despesas
    expenses = view_Expenses()  # Recupera os valores das despesas
    expenses_list = []  # Lista para armazenar os valores de despesas

    for item in expenses:
        expenses_list.append(item[3])  # Acessa o valor da despesa (ajuste conforme sua estrutura)

    expenses_total = sum(expenses_list)  # Calcula o total de despesas

    # Total na conta (balanço)
    balance_total = income_total - expenses_total

    # Certifique-se de retornar valores de forma que possam ser usados em um array ou gráfico
    return [income_total, expenses_total, balance_total]

#arrumando o grafico de pizza
def pie_valores():
    Expenses = view_Expenses()
    Table_list = []

    for i in Expenses:
        Table_list.append(i)


    DataFrame = pd.DataFrame(Table_list, columns = ['Id','Categoria','Data','Quantia'])
    DataFrame = DataFrame.groupby('Categoria')['Quantia'].sum()

    list_Amount = DataFrame.values.tolist()
    list_Category = []

    for i in DataFrame.index:
        list_Category.append(i)


    return([list_Category, list_Amount])