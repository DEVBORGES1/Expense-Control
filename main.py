from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox


#colors
from PIL import Image, ImageTk  # type: ignore

# import progress bar do tkinter

from tkinter.ttk import Progressbar

#import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt  
from matplotlib.figure import Figure  

#import tkcalendar 
from tkcalendar import Calendar, DateEntry
from datetime import date
from Views import  bar_valores, insert_Expenses,view_Categories, insert_categories, insert_Income, view_Income, tabela

co0 = "#000000"  #preto
co1 = "#16191c"  #cinza
co2 = "#ad1700"  #vermelho
co3 = "#38576b"  #valor
co4 = "#403d3d"  #letra
co5 = "#e06636"  # - profit
co6 = "#038cfc"  # azul
co7 = "#3fbfb9"  # verde
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde
co10 = "#FFFFFF" # branco

colors = ['#5588bb', '#66bbbb', '#99bb55', '#ee9944', '#444466', '#bb5555']

# create window
janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background=co0)
janela.resizable(width=False, height=False)

style= ttk.Style(janela)
style.theme_use('clam')

#create frames from division of screen
frameTop = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameTop.grid(row=0, column=0)

frameMid = Frame(janela, width=1043, height=361, bg=co0, pady=20, relief="raised")
frameMid.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameLow = Frame(janela, width=1043, height=300, bg=co0, relief="flat")
frameLow.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)



# working on the top frame
#accessing the image
app_img = Image.open('grafico-de-crescimento (1).png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label( frameTop, image=app_img, text= " Expense control", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co10,)
app_logo.place(x=0, y=0)


# aqui irei definir a tabela como global com a palavra  tree

global tree

def inserir_categoria_x():
    nome = e_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Faltou prencher algum campo')
            return
    
    insert_categories(lista_inserir)

    messagebox.showinfo('Deu boa', 'Os dados foram inseridos com sucesso')

    e_categoria.delete(0,'end')

    # com essa funçao vai me possibilitar de pegar os valores da categoria
    categorias_funcoes = view_Categories()
    categoria = []

    for i in categorias_funcoes:
        categoria.append(i[1])
    

    combo_categoria_despesas['values'] = (categoria)
    


# aqui irei inserir todas as receitas como na funçao acima
def inserir_faturamento_y():
    nome = 'faturamento'
    data = e_cal_faturamento.get()
    quantia =  e_valor_faturamento.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Faltou prencher algum campo')
            return
    
    insert_Income(lista_inserir)

    messagebox.showinfo('Deu boa', 'Os dados foram inseridos com sucesso')

    e_cal_faturamento.delete(0,'end')
    e_valor_faturamento.delete(0,'end')

def inserir_despesas_z():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get()
    quantia =  e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Deu pau', 'Faltou prencher algum campo')
            return
    
    insert_Expenses(lista_inserir)

    messagebox.showinfo('Deu boa', 'Os dados foram inseridos com sucesso')

    combo_categoria_despesas.delete(0, 'end')
    e_cal_despesas.delete(0,'end')
    e_valor_despesas.delete(0,'end')

 #atualizando
    show_income()
    porcentagem()
    grafico_bar()
    conta()
    grafico_pie()






# porcentagem -------------
def porcentagem():
    l_nome = Label(frameMid, text="Porcentagem da receita gasta no mês", height=1, anchor=NW, font=('Verdana 12 bold'), bg=co0, fg=co10,)
    l_nome.place(x=7, y=5)


    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background="#ad1700")
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(frameMid, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = 50

    valor= 50

    l_porcentagem = Label(frameMid, text="{:,.2f}%".format(valor) , anchor=NW, font=('Verdana 12'), bg=co0, fg=co10,)
    l_porcentagem.place(x=200, y=35)


#grafico de colunas sobre a renda, gastos e saldo com a def mostrando a variavel lista de valores
def grafico_bar():
    lista_categorias = ['Renda ', 'Gastos', 'Saldo']
    lista_valores = [3000, 2000, 1000]
    
    # Cores que deseja usar nas barras
    colors = ['#ad1700', '#8b008b', '#39ff14']

    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores, color=colors, width=0.9)

    c = 0
    for i in ax.patches:
        ax.text(i.get_x() - .001, i.get_height() + .5,
                str("{:,.0f}".format(lista_valores[c])), 
                fontsize=17, fontstyle='italic', verticalalignment='bottom', color='white')
        c += 1

    ax.set_xticklabels(lista_categorias, fontsize=16, color='white')

    ax.patch.set_facecolor('#000000')
    
    figura.patch.set_facecolor('#000000') 

    ax.spines['bottom'].set_color('#000000')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#000000')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.tick_params(bottom=False, left=False)

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#000000')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMid)
    canva.get_tk_widget().config(bg='black')  
    canva.get_tk_widget().place(x=10, y=70)

# Criando função de resumo total
def conta():
    valor = [3000, 2000, 1000]
#1
    l_linha = Label(frameMid, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#ad1700',  )
    l_linha.place(x=309, y=52)
    
    l_sumario = Label(frameMid, text="Total renda mensal      ".upper(), anchor=NW, font=('Verdana 12'),bg=co0 , fg=co10)
    l_sumario.place(x=309, y=35)

    l_sumario = Label(frameMid, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 17'),bg=co0 , fg='#ad1700')
    l_sumario.place(x=309, y=70)
#final
    l_linha = Label(frameMid, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#ad1700',  )
    l_linha.place(x=309, y=132)
    
    l_sumario = Label(frameMid, text="Total despesas mensais ".upper(), anchor=NW, font=('Verdana 12'),bg=co0 , fg=co10)
    l_sumario.place(x=309, y=115)

    l_sumario = Label(frameMid, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 17'),bg=co0 , fg='#ad1700')
    l_sumario.place(x=309, y=150)
#2
    l_linha = Label(frameMid, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#ad1700',  )
    l_linha.place(x=309, y=207)
    
    l_sumario = Label(frameMid, text="Total Saldo Em Conta      ".upper(), anchor=NW, font=('Verdana 12'),bg=co0 , fg=co10)
    l_sumario.place(x=309, y=190)

    l_sumario = Label(frameMid, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 17'),bg=co0 , fg='#ad1700')
    l_sumario.place(x=309, y=220)
#3
#aqui criei um novo frame para que o grafico de pizza fique na posição correta
frame_gra_pie = Frame(frameMid, width=580, height=250, bg=co0)
frame_gra_pie.place(x=415, y=5)

def grafico_pie():
    
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    figura.patch.set_facecolor("black") 
    ax = figura.add_subplot(111)

    lista_valores = [3000, 2000, 1000]
    lista_categorias = ['Renda', 'Despesa', 'Saldo']
    colors = ['#4f81bd', '#c0504d', '#9bbb59']  

    explode = [0.05, 0.05, 0.05] 

    wedges, texts, autotexts = ax.pie(
        lista_valores, 
        explode=explode, 
        wedgeprops=dict(width=0.2), 
        autopct='%1.1f%%', 
        colors=colors, 
        shadow=True, 
        startangle=90,
        textprops={'color': "white"} 
    )

    for autotext in autotexts:
        autotext.set_color('white')

    ax.legend(
        lista_categorias, 
        loc="center right", 
        bbox_to_anchor=(1.55, 0.50), 
        facecolor='black', 
        labelcolor='white',
        edgecolor='#ad1700' 
    )

    ax.yaxis.grid(False)

    
    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().place(x=0, y=0)




porcentagem()
grafico_bar()
conta()
grafico_pie()

#create frames within the frame below
frame_income = Frame(frameLow, width=300, height=250, bg=co0,)
frame_income.grid(row=0, column=0)

frame_operations = Frame(frameLow, width=220, height=250, bg=co0,)
frame_operations.grid(row=0, column=1, pady=5)

frame_settings = Frame(frameLow, width=220, height=250, bg=co0,)
frame_settings.grid(row=0, column=2, pady=5)

# create table monthly income

app_table = Label( frameMid,text= " Tabela De Faturamento e gastos", anchor=NW, font=('Verdana 12 bold'),bg=co0, fg=co10)
app_table.place(x=5, y=309)

#create function to show table
def show_income():
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()

    global tree

    # Estilos da Treeview
    style = ttk.Style()
    style.configure("Treeview",
                    background=co0,  # Fundo das células
                    foreground=co10,  # Cor do texto das células
                    rowheight=25,  # Altura das linhas
                    fieldbackground=co0)  # Fundo da área de visualização

    style.map('Treeview', background=[('selected', co2)])  # Cor de seleção
    style.configure('Treeview.Heading', background=co1, foreground=co10, font=('Verdana', 10, 'bold'))  # Cabeçalhos

    # Configurar o estilo do Scrollbar
    style.configure("Vertical.TScrollbar", troughcolor=co0, bordercolor=co0, arrowcolor=co10, background="#ad1700")
    style.configure("Horizontal.TScrollbar", troughcolor=co0, bordercolor=co0, arrowcolor=co10, background="#ad1700")

    # Função do scroll vertical e horizontal 
    tree = ttk.Treeview(frame_income, selectmode="extended", columns=tabela_head, show="headings")
    vsb = ttk.Scrollbar(frame_income, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
    hsb = ttk.Scrollbar(frame_income, orient="horizontal", command=tree.xview, style="Horizontal.TScrollbar")

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n], anchor=hd[n])
        n += 1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

show_income()
class Janela:
    def __init__(self, master):
        self.frame1 = Frame(master, bg='black')
        self.frame1.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        style = ttk.Style()

        # Definindo o tema geral para o estilo
        style.theme_use('clam')

        # Estilizando a Combobox
        style.configure("TCombobox", 
                        fieldbackground="black", 
                        background="orange", 
                        foreground="white", 
                        arrowcolor="white")

        style.configure("Treeview", 
                        background="black", 
                        foreground="white", 
                        rowheight=25, 
                        fieldbackground="black")
        
        style.configure("black.Horizontal.TProgressbar", 
                        background="#ad1700", 
                        thickness=25)

        self.cb = ttk.Combobox(self.frame1, values=["OPÇÃO 1", "OPÇÃO 2", "OPÇÃO 3"], style="TCombobox")
        self.cb.place(relx=0.1, rely=0.1, relwidth=0.25, relheight=0.04)

      
        self.barra = ttk.Progressbar(self.frame1, 
                                     style="black.Horizontal.TProgressbar", 
                                     orient=HORIZONTAL, 
                                     length=500, 
                                     mode='determinate')
        self.barra.place(relx=0.1, rely=0.2, relwidth=0.7, relheight=0.04)
        self.barra['value'] = 70

      
        self.tv = ttk.Treeview(self.frame1, columns=('col1', 'col2', 'col3'), show='headings', style="Treeview")
        self.tv.heading('col1', text="COLUNA 1")
        self.tv.heading('col2', text="COLUNA 2")
        self.tv.heading('col3', text="COLUNA 3")
        self.tv.column('col1', width=100)
        self.tv.column('col2', width=100)
        self.tv.column('col3', width=100)
        self.tv.place(relx=0.1, rely=0.3, relwidth=0.7, relheight=0.3)



#configurando as despesas
l_descricao = Label(frame_operations, text='Insirir Novas Despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_descricao.place(x=10, y=10)

#categoria
l_categoria = Label(frame_operations, text='Categoria:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_categoria.place(x=10, y=40)

#picking up categories
categoria_funcao = view_Categories()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])


combo_categoria_despesas = ttk.Combobox(frame_operations, width=10, font=('Ivy, 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=110, y=41)

l_descricao = Label(frame_operations, text='Data:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_descricao.place(x=10, y=70)

e_cal_despesas = DateEntry(frame_operations, 
                           width=12, 
                           background='black',         # Fundo preto para os quadrados dos dias
                           foreground='white',         # Texto das datas em branco
                           borderwidth=2, 
                           year=2024,
                           selectbackground='#ad1700',  # Cor de fundo para o dia selecionado (vermelho)
                           selectforeground='white',    # Texto do dia selecionado em branco
                           headersbackground=co0,       # Cor de fundo do cabeçalho (dias da semana)
                           headersforeground=co10,      # Cor do texto do cabeçalho
                           normalbackground='black',    # Fundo normal dos dias em preto
                           normalforeground='white',    # Texto normal dos dias em branco
                           bordercolor='#ad1700'        # Cor da borda em vermelho
                          )
e_cal_despesas.place(x=110, y=71)

# valor
l_valor_despesas = Label(frame_operations, text='Valor Gasto:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operations, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)



#button insert
img_add_despesas = Image.open('adicionar.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
button_inserir_despesas = Button( frame_operations, command=inserir_despesas_z, image=img_add_despesas, text= "Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Verdana 7 bold'), bg=co0, fg=co10,overrelief=RIDGE)
button_inserir_despesas.place(x=110, y=131)


#button delet
l_excluir = Label(frame_operations, text='Excluir Ação:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_excluir.place(x=10, y=190)

img_delete = Image.open('bin.png')
img_delete = img_delete.resize((17,17))
img_delete = ImageTk.PhotoImage(img_delete)
button_deletar = Button( frame_operations, image=img_delete, text= "   Deletar".upper(), width=80, compound=LEFT, anchor=NW, font=('Verdana 7 bold'), bg=co0, fg=co10,overrelief=RIDGE)
button_deletar.place(x=110, y=190)


#configurando rendas
l_info = Label(frame_settings, text='Insirir Novos Ganhos ', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_info.place(x=10, y=10)


l_cal_faturamento = Label(frame_settings, text='Data:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_cal_faturamento.place(x=10, y=40)
e_cal_faturamento = DateEntry(frame_settings, 
                           width=12, 
                           background='black',         # Fundo preto para os quadrados dos dias
                           foreground='white',         # Texto das datas em branco
                           borderwidth=2, 
                           year=2024,
                           selectbackground='#ad1700',  # Cor de fundo para o dia selecionado (vermelho)
                           selectforeground='white',    # Texto do dia selecionado em branco
                           headersbackground=co0,       # Cor de fundo do cabeçalho (dias da semana)
                           headersforeground=co10,      # Cor do texto do cabeçalho
                           normalbackground='black',    # Fundo normal dos dias em preto
                           normalforeground='white',    # Texto normal dos dias em branco
                           bordercolor='#ad1700'        # Cor da borda em vermelho
                          )
e_cal_faturamento.place(x=110, y=41)


l_valor_faturamento = Label(frame_settings, text='Quantia:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_valor_faturamento.place(x=10, y=70)
e_valor_faturamento = Entry(frame_settings, width=14, justify='left', relief='solid')
e_valor_faturamento.place(x=110, y=71)

#button insert
img_add_faturamento = Image.open('adicionar.png')
img_add_faturamento = img_add_faturamento.resize((17,17))
img_add_faturamento = ImageTk.PhotoImage(img_add_faturamento)
button_inserir_faturamento = Button( frame_settings, command=inserir_faturamento_y, image=img_add_faturamento, text= "Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Verdana 7 bold'), bg=co0, fg=co10,overrelief=RIDGE)
button_inserir_faturamento.place(x=110, y=111)

#create new category
l_info = Label(frame_settings, text='Categoria:', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co0, fg=co10)
l_info.place(x=10, y=160)

e_categoria = Entry(frame_settings, width=14, justify='left', relief='solid')
e_categoria.place(x=110, y=160)

img_add_categoria = Image.open('adicionar.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
button_inserir_categoria = Button( frame_settings, command=inserir_categoria_x, image=img_add_categoria, text= "Adicionar".upper(), width=80, compound=LEFT, anchor=NW, font=('Verdana 7 bold'), bg=co0, fg=co10,overrelief=RIDGE)
button_inserir_categoria.place(x=110, y=190)


janela.mainloop()
