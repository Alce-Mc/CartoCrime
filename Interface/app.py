import customtkinter as ctk
from tkinter import filedialog
from exportation import Exportation
from Interface.formulaire import Formulaire
from Interface.resultats import Resultats
from chargeur_donnees import ChargeurDonnees
from risk_calculator import CalculateurRisque
from graphiques import Graphiques

#Classe App, arrange et presente l'interface pratique.
class App (ctk.CTk):
    def __init__(self):
        super().__init__()

        #importation et nettoyage des données
        donnees = ChargeurDonnees("data/export.csv").charger()
        self.donnees = donnees
        self.calculateur = CalculateurRisque(donnees)
        self.graphiques = Graphiques(donnees)

        #condition initiales
        self.title("CartoCrime 1.0")
        self.geometry("1200x700")
        self.minsize(400, 300)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        #Création des figures
        graphiques = Graphiques(donnees)
        figures = {
            "Jour × heure": graphiques.carte_chaleur(),
            "Par heure": graphiques.par_heure(),
            "Par secteur": graphiques.par_secteur(),
            "Par lieu": graphiques.par_lieu(),
            "Par âge": graphiques.par_age(),
        }

        #Création des panneau formulaire et résultats
        self.left_panel = Formulaire(self, on_analyser=self.analyser)
        self.right_panel  = Resultats(self, figures)     
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=15, pady=15)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.bouton_export = ctk.CTkButton(
            self.left_panel, text="Exporter le rapport", state="disabled"
        )
        self.bouton_export.grid(column=0, padx=20, pady=10)

    #fonction d'analyse du scénario
    def analyser(self, scenario):
        try:
            resultat = self.calculateur.calculer_indice(scenario)
            top = self.calculateur.top_crimes(scenario)
            figure = self.graphiques.carte_chaleur(scenario)
            self.right_panel.afficher(resultat, top, figure)
            self.bouton_export.configure(
                state="normal",
                command=lambda: self.exporter_rapport(scenario, resultat, top)
            )
        except ValueError as e:
            print("Erreur :", e)

    def exporter_rapport(self, scenario, resultat, top):
        chemin = filedialog.asksaveasfilename(
            title="Enregistrer le rapport",
            initialfile="rapport_cartocrime.txt",
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt")]
        )
        if chemin:
            Exportation().exporter(chemin, scenario, resultat, top, self.donnees)