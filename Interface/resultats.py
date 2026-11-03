import customtkinter as ctk

class Resultats(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self.grid_columnconfigure(0, weight=1)

        # TEMPORAIRE Felipe remplacera
        self.message = ctk.CTkLabel(self, text="Remplissez le scénario et cliquez sur Analyser",
                                    font=("Segoe UI", 16))
        self.message.grid(row=0, column=0, padx=20, pady=20)

    def afficher(self, resultat):
        self.message.configure(text=f"Scénario reçu : {resultat}")