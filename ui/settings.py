
import customtkinter as ctk
from tkinter import messagebox
import sys
import os

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.database import db

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Title
        self.label_title = ctk.CTkLabel(self, text="Configurações", font=("Roboto Medium", 20))
        self.label_title.grid(row=0, column=0, pady=20, padx=20, sticky="w")
        
        # Appearance Mode
        self.frame_mode = ctk.CTkFrame(self)
        self.frame_mode.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        
        self.label_mode = ctk.CTkLabel(self.frame_mode, text="Aparência:", font=("Roboto", 14, "bold"))
        self.label_mode.pack(side="top", anchor="w", padx=10, pady=10)
        
        self.mode_var = ctk.StringVar(value=ctk.get_appearance_mode())
        
        self.rad_sys = ctk.CTkRadioButton(self.frame_mode, text="Sistema", variable=self.mode_var, value="System", command=self.change_mode)
        self.rad_sys.pack(side="left", padx=10, pady=10)
        
        self.rad_light = ctk.CTkRadioButton(self.frame_mode, text="Claro", variable=self.mode_var, value="Light", command=self.change_mode)
        self.rad_light.pack(side="left", padx=10, pady=10)
        
        self.rad_dark = ctk.CTkRadioButton(self.frame_mode, text="Escuro", variable=self.mode_var, value="Dark", command=self.change_mode)
        self.rad_dark.pack(side="left", padx=10, pady=10)

        # Theme Color
        self.frame_color = ctk.CTkFrame(self)
        self.frame_color.grid(row=2, column=0, pady=10, padx=20, sticky="new") # sticky new to stay top
        
        self.label_color = ctk.CTkLabel(self.frame_color, text="Cor de Destaque (Reinício necessário para alguns itens):", font=("Roboto", 14, "bold"))
        self.label_color.pack(side="top", anchor="w", padx=10, pady=10)
        
        self.btn_blue = ctk.CTkButton(self.frame_color, text="Azul (Padrão)", fg_color="#3B8ED0", command=lambda: self.change_color("blue"))
        self.btn_blue.pack(side="left", padx=10, pady=10)
        
        self.btn_green = ctk.CTkButton(self.frame_color, text="Verde", fg_color="#2CC985", command=lambda: self.change_color("green"))
        self.btn_green.pack(side="left", padx=10, pady=10)
        
        self.btn_dblue = ctk.CTkButton(self.frame_color, text="Azul Escuro", fg_color="#1F538D", command=lambda: self.change_color("dark-blue"))
        self.btn_dblue.pack(side="left", padx=10, pady=10)

    def change_mode(self):
        ctk.set_appearance_mode(self.mode_var.get())

    def change_color(self, color):
        ctk.set_default_color_theme(color)
        messagebox.showinfo("Tema", "Tema alterado! Pode ser necessário reiniciar o app para aplicar em todos os componentes.")
