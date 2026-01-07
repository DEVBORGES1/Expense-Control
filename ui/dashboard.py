
import customtkinter as ctk
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfilename
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date
import pandas as pd
from .settings import SettingsFrame

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import db
from utils.gamification import LevelSystem

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, user_id, logout_callback):
        super().__init__(master)
        self.user_id = user_id
        self.logout_callback = logout_callback
        
        # State
        self.editing_id = None
        self.editing_type = None

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Main Content Area
        self.main_view = ctk.CTkTabview(self)
        self.main_view.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_view.add("Visão Geral")
        self.main_view.add("Orçamento")
        self.main_view.add("Lista de Espera")
        self.main_view.add("Gráficos")
        self.main_view.add("Configurações")
        
        # Tabs Setup
        self.setup_overview_tab()
        self.setup_budget_tab()
        self.setup_wishlist_tab()
        self.setup_charts_tab()
        self.setup_settings_tab()
        
        # Initial Content Load
        self.refresh_data()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Expense\nControl", font=("Roboto Medium", 20))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Player Profile
        self.level_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.level_frame.grid(row=1, column=0, padx=10, pady=10)
        
        self.lbl_level_title = ctk.CTkLabel(self.level_frame, text="Nível 1", font=("Roboto", 12, "bold"))
        self.lbl_level_title.pack()
        
        self.lbl_level_name = ctk.CTkLabel(self.level_frame, text="Aprendiz", font=("Roboto", 11))
        self.lbl_level_name.pack()
        
        self.prog_level = ctk.CTkProgressBar(self.level_frame, width=120, height=8, progress_color="#E0A800")
        self.prog_level.set(0)
        self.prog_level.pack(pady=5)
        
        self.lbl_xp = ctk.CTkLabel(self.level_frame, text="R$ 0 / R$ 500", font=("Roboto", 10))
        self.lbl_xp.pack()

        self.btn_refresh = ctk.CTkButton(self.sidebar, text="Atualizar", command=self.refresh_data)
        self.btn_refresh.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_export = ctk.CTkButton(self.sidebar, text="Exportar CSV", fg_color="green", command=self.export_csv)
        self.btn_export = ctk.CTkButton(self.sidebar, text="Exportar CSV", fg_color="green", command=self.export_csv)
        self.btn_export.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_logout = ctk.CTkButton(self.sidebar, text="Sair", fg_color="transparent", border_width=2, command=self.logout_callback)
        self.btn_logout.grid(row=6, column=0, padx=20, pady=20)

    def setup_overview_tab(self):
        tab = self.main_view.tab("Visão Geral")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(3, weight=1)
        
        # 0. Filters Frame
        self.filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        months = ["Todos"] + [f"{i:02d}" for i in range(1, 13)]
        years = ["Todos", "2024", "2025", "2026"]
        
        ctk.CTkLabel(self.filter_frame, text="Mês:").pack(side="left", padx=5)
        self.cb_month = ctk.CTkComboBox(self.filter_frame, values=months, width=100)
        self.cb_month.set("Todos")
        self.cb_month.pack(side="left", padx=5)
        
        ctk.CTkLabel(self.filter_frame, text="Ano:").pack(side="left", padx=5)
        self.cb_year = ctk.CTkComboBox(self.filter_frame, values=years, width=100)
        self.cb_year.set("Todos")
        self.cb_year.pack(side="left", padx=5)
        
        ctk.CTkButton(self.filter_frame, text="Filtrar", width=80, command=self.refresh_data).pack(side="left", padx=10)

        # 1. Summary Cards Frame
        self.cards_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="ew", pady=10)
        self.cards_frame.grid_columnconfigure((0,1,2), weight=1)
        
        self.card_income = self.create_info_card(self.cards_frame, "Receitas", "+ R$ 0,00", "green")
        self.card_income.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.card_expense = self.create_info_card(self.cards_frame, "Despesas", "- R$ 0,00", "red")
        self.card_expense.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.card_balance = self.create_info_card(self.cards_frame, "Saldo", "R$ 0,00", "gray")
        self.card_balance.grid(row=0, column=2, padx=5, sticky="ew")
        
        # 2. Add/Edit Transaction Form
        self.form_frame = ctk.CTkFrame(tab)
        self.form_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        categories = db.get_categories()
        
        self.cb_type = ctk.CTkComboBox(self.form_frame, values=["Receita", "Despesa"])
        self.cb_type.set("Despesa")
        self.cb_type.pack(side="left", padx=10, pady=10)
        
        self.entry_val = ctk.CTkEntry(self.form_frame, placeholder_text="Valor")
        self.entry_val.pack(side="left", padx=10, pady=10)
        
        self.cb_cat = ctk.CTkComboBox(self.form_frame, values=categories)
        self.cb_cat.pack(side="left", padx=10, pady=10)
        
        # Mood Selector (Visible only for 'Despesa')
        self.cb_mood = ctk.CTkComboBox(self.form_frame, values=["Normal", "Ansioso 😰", "Triste 😢", "Feliz 🤩", "Entediado 😐", "Estressado 🤯"])
        self.cb_mood.set("Normal")
        self.cb_mood.pack(side="left", padx=10, pady=10)
        
        self.entry_date = ctk.CTkEntry(self.form_frame, placeholder_text="Data (YYYY-MM-DD)")
        self.entry_date.pack(side="left", padx=10, pady=10)
        self.entry_date.insert(0, str(date.today()))
        
        self.btn_add = ctk.CTkButton(self.form_frame, text="Adicionar", command=self.add_transaction)
        self.btn_add.pack(side="left", padx=10, pady=10)
        
        self.btn_cancel_edit = ctk.CTkButton(self.form_frame, text="X", width=30, fg_color="gray", command=self.cancel_edit)
        # Hidden by default
        
        # 3. Recent Transactions Table
        self.tree_frame = ctk.CTkFrame(tab)
        self.tree_frame.grid(row=3, column=0, sticky="nsew")
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Tipo", "Categoria", "Data", "Valor"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Valor", text="Valor")
        self.tree.column("ID", width=30)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Actions
        self.action_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.action_frame.grid(row=4, column=0, pady=5, sticky="ew")
        
        self.btn_delete = ctk.CTkButton(self.action_frame, text="Excluir Selecionado", fg_color="red", command=self.delete_selected)
        self.btn_delete.pack(side="right", padx=5)
        
        self.btn_edit = ctk.CTkButton(self.action_frame, text="Editar Selecionado", fg_color="#E0A800", command=self.start_edit)
        self.btn_edit.pack(side="right", padx=5)

    def setup_budget_tab(self):
        self.tab_budget = self.main_view.tab("Orçamento")
        self.tab_budget.grid_columnconfigure(0, weight=1)
        
        # Add Budget Form
        form = ctk.CTkFrame(self.tab_budget)
        form.pack(pady=10, fill="x")
        
        ctk.CTkLabel(form, text="Definir Meta Mensal:").pack(side="left", padx=10)
        self.cb_budget_cat = ctk.CTkComboBox(form, values=db.get_categories())
        self.cb_budget_cat.pack(side="left", padx=5)
        
        self.entry_budget_val = ctk.CTkEntry(form, placeholder_text="Limite (R$)")
        self.entry_budget_val.pack(side="left", padx=5)
        
        ctk.CTkButton(form, text="Salvar Meta", command=self.save_budget).pack(side="left", padx=10)
        
        # Budget List Container (Scrollable)
        self.budget_container = ctk.CTkScrollableFrame(self.tab_budget)
        self.budget_container.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_wishlist_tab(self):
        self.tab_wishlist = self.main_view.tab("Lista de Espera")
        self.tab_wishlist.grid_columnconfigure(0, weight=1)
        self.tab_wishlist.grid_rowconfigure(1, weight=1)
        
        # Form
        form = ctk.CTkFrame(self.tab_wishlist)
        form.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        
        self.entry_wish_name = ctk.CTkEntry(form, placeholder_text="Eu quero comprar...", width=200)
        self.entry_wish_name.pack(side="left", padx=5, pady=10)
        
        self.entry_wish_val = ctk.CTkEntry(form, placeholder_text="Preço (R$)")
        self.entry_wish_val.pack(side="left", padx=5, pady=10)
        
        ctk.CTkLabel(form, text="Esperar por:").pack(side="left", padx=5)
        self.cb_wish_time = ctk.CTkComboBox(form, values=["24 Horas", "3 Dias", "7 Dias"])
        self.cb_wish_time.pack(side="left", padx=5)
        
        ctk.CTkButton(form, text="Adicionar à Lista", command=self.add_wishlist).pack(side="left", padx=10)
        
        # List
        self.wishlist_frame = ctk.CTkScrollableFrame(self.tab_wishlist)
        self.wishlist_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def setup_settings_tab(self):
        self.settings_frame = SettingsFrame(self.main_view.tab("Configurações"))
        self.settings_frame.pack(fill="both", expand=True)

    def setup_charts_tab(self):
        tab = self.main_view.tab("Gráficos")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        self.chart_frame = ctk.CTkFrame(tab)
        self.chart_frame.grid(row=0, column=0, sticky="nsew")

    def create_info_card(self, parent, title, value, color_code):
        card = ctk.CTkFrame(parent, fg_color="#333333")
        ctk.CTkLabel(card, text=title, font=("Roboto", 14)).pack(pady=(10, 0))
        label_val = ctk.CTkLabel(card, text=value, font=("Roboto", 24, "bold"))
        label_val.pack(pady=(5, 10))
        if color_code == "green": label_val.configure(text_color="#2cc985")
        elif color_code == "red": label_val.configure(text_color="#e34c4c")
        return card

    # --- Logic ---

    def start_edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um item")
            return
            
        item = self.tree.item(selected[0])
        val = item['values'] 
        # [ID, Tipo, Cat, Data, Valor]
        
        self.editing_id = val[0]
        self.editing_type = val[1]
        
        # Populate form
        self.cb_type.set(val[1])
        self.cb_cat.set(val[2])
        self.entry_date.delete(0, "end")
        self.entry_date.insert(0, val[3])
        self.entry_val.delete(0, "end")
        self.entry_val.insert(0, str(val[4]))
        
        # Change Button State
        self.btn_add.configure(text="Salvar Alteração", fg_color="#E0A800")
        self.btn_cancel_edit.pack(side="left", padx=5)

    def cancel_edit(self):
        self.editing_id = None
        self.editing_type = None
        self.btn_add.configure(text="Adicionar", fg_color=['#3a7ebf', '#1f538d'])
        self.btn_cancel_edit.pack_forget()
        self.entry_val.delete(0, "end")

    def add_transaction(self):
        t_type = self.cb_type.get()
        t_cat = self.cb_cat.get()
        t_date = self.entry_date.get()
        t_val = self.entry_val.get()
        
        try:
            val_float = float(t_val.replace(",", "."))
            
            if self.editing_id:
                # Update Mode
                db.update_transaction(self.editing_id, t_type, t_cat, t_date, val_float)
                messagebox.showinfo("Sucesso", "Atualizado com sucesso!")
                self.cancel_edit()
            else:
                # Add Mode
                if t_type == "Receita":
                    db.add_income(self.user_id, t_cat, t_date, val_float)
                else:
                    mood = self.cb_mood.get()
                    db.add_expense(self.user_id, t_cat, t_date, val_float, mood)
                messagebox.showinfo("Sucesso", "Registrado com sucesso!")
                self.entry_val.delete(0, "end")
                
            self.refresh_data()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected: return
        val = self.tree.item(selected[0])['values']
        if messagebox.askyesno("Confirmar", f"Excluir {val[1]}?"):
            db.delete_transaction(val[0], val[1])
            self.refresh_data()

    def update_card(self, card_widget, text):
        card_widget.winfo_children()[1].configure(text=text)

    def get_filters(self):
        m = self.cb_month.get()
        y = self.cb_year.get()
        return (None if m == "Todos" else m, None if y == "Todos" else y)

    def refresh_data(self):
        m, y = self.get_filters()
        
        # Balances
        income, expenses, balance = db.get_user_balance_filtered(self.user_id, m, y)
        self.update_card(self.card_income, f"+ R$ {income:,.2f}")
        self.update_card(self.card_expense, f"- R$ {expenses:,.2f}")
        self.update_card(self.card_balance, f"R$ {balance:,.2f}")
        
        # Table
        for row in self.tree.get_children(): self.tree.delete(row)
        transactions = db.get_transactions_filtered(self.user_id, m, y)
        for t in transactions: self.tree.insert("", "end", values=t)
        
        # Charts
        self.update_charts(income, expenses)
        
        # Budgets refresh
        self.refresh_budgets()

    def save_budget(self):
        try:
            val = float(self.entry_budget_val.get().replace(",", "."))
            cat = self.cb_budget_cat.get()
            db.set_budget(self.user_id, cat, val)
            messagebox.showinfo("Sucesso", "Meta salva!")
            self.refresh_budgets()
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")

    def refresh_budgets(self):
        # Clear container
        for w in self.budget_container.winfo_children(): w.destroy()
        
        budgets = db.get_budgets(self.user_id)
        # Calculate spending for current month (implicit assumption: user wants to see current month progress)
        today = date.today()
        m, y = f"{today.month:02d}", str(today.year)
        spending = db.get_category_spending(self.user_id, m, y)
        
        if not budgets:
            ctk.CTkLabel(self.budget_container, text="Nenhuma meta definida.").pack(pady=20)
            return

        for cat, limit in budgets.items():
            spent = spending.get(cat, 0.0)
            percent = spent / limit if limit > 0 else 0
            
            frame = ctk.CTkFrame(self.budget_container)
            frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(frame, text=f"{cat} (R$ {spent:,.2f} / R$ {limit:,.2f})", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10, pady=2)
            
            # Progress Bar Color
            color = "#2cc985"
            if percent > 0.8: color = "#E0A800" # Warning
            if percent >= 1.0: color = "#e34c4c" # Error
            
            prog = ctk.CTkProgressBar(frame, progress_color=color)
            prog.set(min(percent, 1.0))
            prog.pack(fill="x", padx=10, pady=(0, 10))

    def add_wishlist(self):
        name = self.entry_wish_name.get()
        val_str = self.entry_wish_val.get()
        duration_str = self.cb_wish_time.get()
        
        if not name or not val_str:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
            
        try:
            val = float(val_str.replace(",", "."))
            hours = 24
            if "3 Dias" in duration_str: hours = 72
            if "7 Dias" in duration_str: hours = 168
            
            db.add_wishlist_item(self.user_id, name, val, hours)
            messagebox.showinfo("Sucesso", "Item adicionado! O botão de compra será liberado após o tempo.")
            self.entry_wish_name.delete(0, "end")
            self.entry_wish_val.delete(0, "end")
            self.refresh_wishlist()
            
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")

    def refresh_wishlist(self):
        for w in self.wishlist_frame.winfo_children(): w.destroy()
        
        items = db.get_wishlist(self.user_id)
        if not items:
            ctk.CTkLabel(self.wishlist_frame, text="Sua lista de espera está vazia.").pack(pady=20)
            return

        for item in items:
            # item: (id, name, value, cooldown_end, status)
            i_id, name, val, end, status = item
            
            card = ctk.CTkFrame(self.wishlist_frame)
            card.pack(fill="x", pady=5)
            
            ctk.CTkLabel(card, text=f"{name} (R$ {val:,.2f})", font=("Roboto", 14, "bold")).pack(side="left", padx=10)
            ctk.CTkLabel(card, text=f"Libera em: {end}").pack(side="left", padx=10)
            
            if status == "AVAILABLE":
                ctk.CTkButton(card, text="Comprar Agora", fg_color="green", command=lambda x=item: self.buy_wishlist(x)).pack(side="right", padx=5)
                ctk.CTkButton(card, text="Desistir (Economizei!)", fg_color="#E0A800", command=lambda x=i_id: self.cancel_wishlist(x)).pack(side="right", padx=5)
            else:
                ctk.CTkButton(card, text="Bloqueado 🔒", state="disabled", fg_color="gray").pack(side="right", padx=10)

    def buy_wishlist(self, item):
        # item: id, name, val, end, status
        # Add to expenses logic
        i_id, name, val, _, _ = item
        # Open Add Dialog pre-filled? Or just add directly? 
        # Adding directly for simplicity
        try:
            db.add_expense(self.user_id, "Lazer", date.today(), val, "Normal")
            db.update_wishlist_status(i_id, "PURCHASED")
            messagebox.showinfo("Sucesso", "Compra realizada! Despesa registrada.")
            self.refresh_wishlist()
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def cancel_wishlist(self, item_id):
        if messagebox.askyesno("Parabéns", "Tem certeza que quer desistir? Você economizará esse dinheiro!"):
            db.update_wishlist_status(item_id, "CANCELLED")
            self.refresh_wishlist()

    def refresh_data(self):
        # ... logic as before ...
        m, y = self.get_filters()
        
        # Balances
        income, expenses, balance = db.get_user_balance_filtered(self.user_id, m, y)
        self.update_card(self.card_income, f"+ R$ {income:,.2f}")
        self.update_card(self.card_expense, f"- R$ {expenses:,.2f}")
        self.update_card(self.card_expense, f"- R$ {expenses:,.2f}")
        self.update_card(self.card_balance, f"R$ {balance:,.2f}")
        
        # Update Level
        stats = LevelSystem.calculate_stats(balance)
        self.lbl_level_title.configure(text=f"Nível {stats['level']}")
        self.lbl_level_name.configure(text=stats['title'])
        self.prog_level.set(stats['percent'])
        self.lbl_xp.configure(text=f"R$ {stats['current']:,.0f} / R$ {stats['goal']:,.0f}")
        
        # Table
        for row in self.tree.get_children(): self.tree.delete(row)
        transactions = db.get_transactions_filtered(self.user_id, m, y)
        for t in transactions: self.tree.insert("", "end", values=t)
        
        # Charts
        self.update_charts(income, expenses)
        
        # Budgets refresh
        self.refresh_budgets()
        
        # Wishlist refresh
        self.refresh_wishlist()

    def update_charts(self, inc, exp):
        for widget in self.chart_frame.winfo_children(): widget.destroy()
        if inc == 0 and exp == 0:
            ctk.CTkLabel(self.chart_frame, text="Sem dados para gráfico").pack(pady=50)
            return
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie([inc, exp], labels=['Receitas', 'Despesas'], autopct='%1.1f%%', startangle=90, colors=['#2cc985', '#e34c4c'])
        FigureCanvasTkAgg(fig, master=self.chart_frame).get_tk_widget().pack(fill="both", expand=True)
        
    def export_csv(self):
        m, y = self.get_filters()
        transactions = db.get_transactions_filtered(self.user_id, m, y)
        
        path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path: return
        
        try:
            # Convert list of tuples to DataFrame (id, type, cat, date, val)
            df = pd.DataFrame(transactions, columns=["ID", "Tipo", "Categoria", "Data", "Valor"])
            df.to_csv(path, index=False, encoding="utf-8-sig") # utf-8-sig for Excel compatibility
            messagebox.showinfo("Exportar", "Arquivo salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
