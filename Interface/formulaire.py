import customtkinter as ctk

class Formulaire(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        ctk.CTkLabel(self, text="Données",  font = ("Segoe UI", 20, "bold")).grid(row = 0, column = 0)
        ctk.CTkLabel(self, text="Age").grid(row = 1, column = 0)
        self.age = ctk.CTkEntry(self, placeholder_text="ex: 19")
        self.age.grid(row = 2, column = 0)
