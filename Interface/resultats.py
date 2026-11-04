import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COULEURS = {"faible": "#16a34a", "moyen": "#ca8a04", "élevé": "#dc2626"}


class Resultats(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=15)
        self.grid_columnconfigure(0, weight=1)

        # cree la carte de l'indice
        self.carte = ctk.CTkFrame(self, corner_radius=20, fg_color="gray25")
        self.carte.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 15))
        self.carte.grid_columnconfigure(0, weight=1)

        #texte de l'indice sur la carte
        self.indice = ctk.CTkLabel(self.carte, text="—", font=("Segoe UI", 60, "bold"), text_color="white")
        self.indice.grid(row=0, column=0, pady=(25, 0))

        #Texte initiale
        self.categorie = ctk.CTkLabel(self.carte, text="Remplissez le scénario et cliquez sur Analyser", font=("Segoe UI", 18), text_color="white")
        self.categorie.grid(row=1, column=0, pady=(0, 25))


        #Charte
        self.grid_rowconfigure(1, weight=1)
        self.canvas = None

    def afficher(self, resultat, top, figure):
        couleur = COULEURS.get(resultat.categorie, "gray25")
        self.carte.configure(fg_color=couleur)
        self.indice.configure(text=f"{resultat.indice}×")
        self.categorie.configure(text=f"Risque {resultat.categorie} par rapport à la moyenne")

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))


