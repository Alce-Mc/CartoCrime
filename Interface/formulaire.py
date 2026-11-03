import customtkinter as ctk

#Classe gérant l'entrée de données, (Tout le panneau de gauche)

class Formulaire(ctk.CTkFrame):
    def __init__(self, master, on_analyser):
        super().__init__(master, corner_radius=15)
        self.on_analyser = on_analyser

        #Étiquetages des champs d'entrées
        ctk.CTkLabel(self, text="Données",  font = ("Segoe UI", 20, "bold")).grid(row = 0, column = 0)
        ctk.CTkLabel(self, text="Age").grid(row = 1, column = 0)
        self.age = ctk.CTkEntry(self, placeholder_text="ex: 19")
        self.secteur = ctk.CTkEntry(self, placeholder_text="Hollywood")
        self.type_lieu = ctk.CTkEntry(self, placeholder_text="Trottoir")
        self.jour = ctk.CTkEntry(self, placeholder_text="Mardi")
        self.heure = ctk.CTkEntry(self, placeholder_text="")

        #positionnement des champs d'entrée
        self.age.grid(row = 2, column = 0)

        self.erreur = ctk.CTkLabel(self, text="", text_color="#e74c3c")
        self.erreur.grid(row=98, column=0, padx=20)

        ctk.CTkButton(self, text="Analyser", height=40, font=("Segoe UI", 15, "bold"), command=self._clic).grid(row=99, column=0, sticky="ew", padx=20, pady=(5, 20))


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
            "age": age,
            # "secteur": self.secteur.get(),
            # "sexe": self.sexe.get(),
        }

        self.on_analyser(scenario)


