import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

COULEURS = {"faible": "#16a34a", "moyen": "#ca8a04", "élevé": "#dc2626"}


class Resultats(ctk.CTkFrame):
    def __init__(self, master, figures):
        super().__init__(master, corner_radius=15)
        self.grid_columnconfigure(0, weight=1)

        # crée et place la carte de l'indice
        self.carte = ctk.CTkFrame(self, corner_radius=20, fg_color="gray25")
        self.carte.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 15))
        self.carte.grid_columnconfigure(0, weight=1)

        #texte de l'indice sur la carte
        self.indice = ctk.CTkLabel(self.carte, text="—", font=("Segoe UI", 20,), text_color="white")
        self.indice.grid(row=1, column=0, pady=(0, 25))

        #Texte initiale
        self.categorie = ctk.CTkLabel(self.carte, text="Remplissez le scénario à analyser", font=("Segoe UI", 30, "bold"), text_color="white")
        self.categorie.grid(row=0, column=0, pady=(25, 0))


        #Onglets des graphiques
        self.onglets = ctk.CTkTabview(self)
        self.onglets.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))

        self.canvas = {}
        for nom, figure in figures.items():
            self.onglets.add(nom)
            self._placer_figure(nom, figure)

    #Place les graphiques
    def _placer_figure(self, onglet, figure):
        if onglet in self.canvas:
            self.canvas[onglet].get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(figure, master=self.onglets.tab(onglet))
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas[onglet] = canvas


    #affichage de la carte de résultats
    def afficher(self, resultat, top, figure):
        couleur = COULEURS.get(resultat.categorie, "gray25")
        self.carte.configure(fg_color=couleur)
        self.categorie.configure(text=f"Risque {resultat.categorie}")
        ecart = round(abs(resultat.indice - 1) * 100)
        if resultat.indice >= 1:
            phrase = f"{ecart} % plus élevé que la moyenne  ({resultat.indice}×)"
        else:
            phrase = f"{ecart} % plus bas que la moyenne  ({resultat.indice}×)"

        self.indice.configure(text=phrase)
        

