
import customtkinter as ctk
from .login import LoginFrame
from .dashboard import DashboardFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Control Moderno")
        self.geometry("1100x700")
        
        # Current User State
        self.current_user_id = None
        
        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize Frames
        self.login_frame = None
        self.dashboard_frame = None
        
        self.show_login()

    def show_login(self):
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        
        self.login_frame = LoginFrame(self, login_success_callback=self.on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, user_id):
        self.current_user_id = user_id
        if self.login_frame:
            self.login_frame.destroy()
            
        self.show_dashboard()

    def show_dashboard(self):
        self.dashboard_frame = DashboardFrame(self, self.current_user_id, logout_callback=self.logout)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        self.current_user_id = None
        self.show_login()
