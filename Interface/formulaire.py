import customtkinter as ctk
from constantes import SECTEURS, JOURS, SEXES

#Classe gérant l'entrée de données, (Tout le panneau de gauche)
class Formulaire(ctk.CTkFrame):

    #Initialisation des éléments de base
    def __init__(self, master, on_analyser):
        super().__init__(master, corner_radius=15)
        self.rangee = 2
        self.on_analyser = on_analyser

        #Création des champs d'entrées
        ctk.CTkLabel(self, text="Données",  font = ("Segoe UI", 20, "bold")).grid(row = 1, column = 0, sticky = 'w', pady =(10, 0) )
        self.age = self._ajouter_champ("Âge", ctk.CTkEntry(self, placeholder_text="ex: 19"))
        self.sexe = self._ajouter_champ("Sexe", ctk.CTkSegmentedButton(self, values=list(SEXES.keys())))
        self.sexe.set("Femme")
        self.jour = self._ajouter_champ("Jour", ctk.CTkOptionMenu(self, values=JOURS))
        self.secteur = self._ajouter_champ("Secteur", ctk.CTkOptionMenu(self, values=SECTEURS))
        
        #Label de l'entrée de l'heure
        self.label_heure = ctk.CTkLabel(self, text="Heure: 17h")
        self.label_heure.grid(row=self.rangee, column = 0, sticky = "w", padx = 20)
        self.rangee += 2

        #Slider de l'entrée de l'heure
        self.heure = ctk.CTkSlider(self, from_=0, to=23, number_of_steps=23, command=self._maj_heure)
        self.heure.set(17)
        self.heure.grid(row=self.rangee, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.rangee += 2

        #Bouton d'erreur
        self.erreur = ctk.CTkLabel(self, text="", text_color="#e74c3c")
        self.erreur.grid(row=98, column=0, padx=20)

        ctk.CTkButton(self, text="Analyser", height=40, font=("Segoe UI", 15, "bold"), command=self._clic).grid(row=self.rangee, column=0, sticky="ew", padx=20, pady=(5, 20))

    #mise a jour de l'heure afficher lorsque glisse le slider.
    def _maj_heure(self, valeur):
        self.label_heure.configure(text=f"Heure : {int(valeur)}h")

    #Bouton d'entrée des paramètres
    def _clic(self):
        #Validation des paramètres
        try:
            age = int(self.age.get())
            if not 1 <= age <= 119:
                raise ValueError
        except ValueError:
            self.erreur.configure(text="Âge invalide (entre 1 et 119)")
            return
        self.erreur.configure(text="")


        #Construire le scénario puis le rendre accessible à app.py
        scenario = {
            "secteur": self.secteur.get(),        # "Hollywood"
            "jour": self.jour.get(),              # "Lundi"
            "heure": int(self.heure.get()),       # 17
            "age": age,                           # 19
            "sexe": SEXES[self.sexe.get()],       # "F"
        }

        self.on_analyser(scenario)

    #fonctions pour afficher les champs
    def _ajouter_champ(self, titre, widget):
        #Place un label + son widget sur les 2 prochaines rangées, et retourne le widget.
        ctk.CTkLabel(self, text=titre).grid(row=self.rangee, column=0, sticky="w", padx=20)
        widget.grid(row=self.rangee + 1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.rangee += 2
        return widget
