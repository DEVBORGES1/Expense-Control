from tkinter import *
from tkinter import Tk, ttk


#colors
from PIL import Image, ImageTk  # type: ignore

# import progress bar do tkinter

from tkinter.ttk import Progressbar

#import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt  
from matplotlib.figure import Figure  

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

# porcentagem -------------
def porcentagem():
    l_nome = Label(frameMid, text="Porcentagem da receita gasta no mês", height=1, anchor=NW, font=('Verdana 12'), bg=co0, fg=co10,)
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
    valor = [600,400,100]
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
    figura.patch.set_facecolor("black")  # Define o fundo do gráfico como preto
    ax = figura.add_subplot(111)

    lista_valores = [600, 400, 100]
    lista_categorias = ['Renda', 'Despesa', 'Saldo']

    explode = [0.05, 0.05, 0.05]  # Explode para todas as categorias igualmente

    # Gráfico de pizza com ajustes de cor e porcentagem branca
    wedges, texts, autotexts = ax.pie(
        lista_valores, 
        explode=explode, 
        wedgeprops=dict(width=0.2), 
        autopct='%1.1f%%', 
        colors=colors, 
        shadow=True, 
        startangle=90,
        textprops={'color': "white"}  # Porcentagens em branco
    )

    # Ajusta as cores das porcentagens manualmente
    for autotext in autotexts:
        autotext.set_color('white')

    # Ajusta a legenda
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    # Corrige a posição do gráfico e atribui ao frame correto
    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().place(x=0, y=0)


porcentagem()
grafico_bar()
conta()
grafico_pie()

janela.mainloop()
