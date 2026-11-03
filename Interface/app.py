import customtkinter as ctk
from interface.formulaire import Formulaire
from interface.resultats import Resultats

#Classe App, arrange et presente l'interface pratique.
class App (ctk.CTk):
    def __init__(self):
        super().__init__()
        #condition initiales
        self.title("CartoCrime 0.1")
        self.geometry("1100x600")
        self.minsize(800, 500)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Panneau formulaire et résultats
        self.left_panel = Formulaire(self, on_analyser=self.analyser)
        self.right_panel  = Resultats(self)     
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

    #fonction d'analyse du scénario
    def analyser(self, scenario):
        self.right_panel.afficher(scenario)