import customtkinter as ctk
from interface.formulaire import Formulaire

class App (ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CartoCrime 0.1")
        self.geometry("1100x600")
        self.minsize(800, 500)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_panel = Formulaire(self)
        self.right_panel  = ctk.CTkFrame(self, fg_color="dark blue")     

        self.left_panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
