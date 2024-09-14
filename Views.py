import sqlite3 as lite

# Conexão com o banco de dados
con = lite.connect('DATA.db')

# Função de inserção ---------

# Inserir categorias
def insert_categories(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categories (nome) VALUES (?)"
        cur.execute(query, (i,)) 

# Inserir receita
def insert_Income(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Income (categoria, adicionado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)  

# Inserir despesas
def insert_Expenses(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Expenses (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i) 
# Funções de deleção ---------

# Deletar receita
def delete_Income(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Income WHERE id=?"  
        cur.execute(query, (i,))  

# Deletar despesas
def delete_Expenses(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Expenses WHERE id=?"  
        cur.execute(query, (i,)) 

# Função para visualizar dados ---------

# Visualizar categorias
def view_Categories():
    Item_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categories")
        linha = cur.fetchall()
        for l in linha:
            Item_list.append(l)
    
    return Item_list


# ver a renda
def view_Income():
    Item_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Income")
        linha = cur.fetchall()
        for l in linha:
            Item_list.append(l)
    
    return Item_list

# ver a Expenses
def view_Expenses():
    Item_list = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Expenses")
        linha = cur.fetchall()
        for l in linha:
            Item_list.append(l)
    
    return Item_list


