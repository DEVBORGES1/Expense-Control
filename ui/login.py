
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add parent directory to path to import data module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import db

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, login_success_callback):
        super().__init__(master)
        self.login_success_callback = login_success_callback
        
        # Center Content
        # Custom Colors
        self.brand_color = "#2cc985"
        self.bg_color = "#1a1a1a"
        self.card_color = "#2b2b2b"
        
        # Main Background
        self.configure(fg_color=self.bg_color)
        
        # Center Content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Login Card
        self.container = ctk.CTkFrame(self, width=500, corner_radius=20, fg_color=self.card_color, border_width=1, border_color="#333333")
        self.container.grid(row=0, column=0, padx=20)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Logo / Title Area
        self.label_logo = ctk.CTkLabel(self.container, text="💰", font=("Emoji", 72))
        self.label_logo.grid(row=0, column=0, pady=(50, 10))
        
        self.label_title = ctk.CTkLabel(self.container, text="Expense Control", font=("Roboto Medium", 32))
        self.label_title.grid(row=1, column=0, padx=20)
        
        self.label_subtitle = ctk.CTkLabel(self.container, text="Gerencie suas finanças com inteligência.", font=("Roboto", 14), text_color="gray")
        self.label_subtitle.grid(row=2, column=0, pady=(5, 40))
        
        # Inputs
        self.entry_user = ctk.CTkEntry(self.container, placeholder_text="Usuário", width=360, height=50, corner_radius=12, font=("Roboto", 14))
        self.entry_user.grid(row=3, column=0, pady=12)
        
        self.entry_pass = ctk.CTkEntry(self.container, placeholder_text="Senha", show="*", width=360, height=50, corner_radius=12, font=("Roboto", 14))
        self.entry_pass.grid(row=4, column=0, pady=(0, 25))
        
        # Buttons
        self.btn_login = ctk.CTkButton(self.container, text="ENTRAR", width=360, height=50, corner_radius=12, 
                                       fg_color=self.brand_color, hover_color="#26ad73", 
                                       font=("Roboto Medium", 16), command=self.login_event)
        self.btn_login.grid(row=5, column=0, pady=(10, 15))
        
        self.btn_register = ctk.CTkButton(self.container, text="Criar nova conta", width=360, height=35, 
                                          fg_color="transparent", text_color="gray", hover_color="#333333", 
                                          font=("Roboto", 13), command=self.register_event)
        self.btn_register.grid(row=6, column=0, pady=(0, 50))
        
    def login_event(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        if not username or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
            
        success, result = db.login_user(username, password)
        if success:
            self.login_success_callback(result)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    def register_event(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        if not username or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        
        success, msg = db.register_user(username, password)
        if success:
            messagebox.showinfo("Sucesso", "Conta criada com sucesso! Você já pode entrar.")
        else:
            messagebox.showerror("Erro", msg)
