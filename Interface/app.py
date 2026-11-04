import customtkinter as ctk
from interface.formulaire import Formulaire
from interface.resultats import Resultats
from chargeur_donnees import ChargeurDonnees
from risk_calculator import CalculateurRisque
from graphiques import Graphiques

#Classe App, arrange et presente l'interface pratique.
class App (ctk.CTk):
    def __init__(self):
        super().__init__()

        #importation et nettoyage des données
        donnees = ChargeurDonnees("data/export.csv").charger()
        self.calculateur = CalculateurRisque(donnees)
        self.graphiques = Graphiques(donnees)

        #condition initiales
        self.title("CartoCrime 0.5")
        self.geometry("800x500")
        self.minsize(400, 300)
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
        try:
            resultat = self.calculateur.calculer_indice(scenario)
            top = self.calculateur.top_crimes(scenario)
            figure = self.graphiques.par_heure()
            self.right_panel.afficher(resultat, top, figure)
        except ValueError as e:
            print("Erreur :", e)