import pandas as pd
from risk_calculator import LIMITES_AGE, NOMS_AGE
from matplotlib.figure import Figure

FOND = "#2b2b2b"
TEXTE = "#dce4ee"
ACCENT = "#3b82f6"
SURLIGNE = "#ef4444"
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

class Graphiques:
    def __init__(self, donnees):
        self.donnees = donnees

    def par_heure(self):
        nombres = self.donnees["heure"].value_counts()
        nombres = nombres.reindex(range(24), fill_value=0)
        fig = Figure(figsize = (6,3))
        ax = fig.add_subplot()
        ax.bar(nombres.index, nombres.values)
        ax.set_xlabel("Heure")
        ax.set_ylabel("Nombre de crimes rapportés")
        ax.set_title("Nombre de crimes selon l’heure")
        ax.set_xticks(range(24))
        fig.tight_layout()
        return fig
    
    def carte_chaleur(self):
        comptes = self.donnees.groupby(["jour_semaine", "heure"]).size()
        tableau = comptes.unstack(fill_value=0)
        tableau = tableau.reindex(
            index=range(7), columns=range(24), fill_value=0
        )

        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi",
                 "Vendredi", "Samedi", "Dimanche"]

        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot()
        image = ax.imshow(tableau, cmap="YlOrRd", aspect="auto")
        fig.colorbar(image, ax=ax, label="Nombre de crimes rapportés")
        ax.set_xticks(range(24))
        ax.set_yticks(range(7), jours)
        ax.set_xlabel("Heure")
        ax.set_ylabel("Jour de la semaine")
        ax.set_title("Crimes rapportés selon le jour et l’heure")
        fig.tight_layout()
        return fig
        

    def par_secteur(self):
        nombres = self.donnees["secteur"].value_counts()
        nombres = nombres.sort_values()

        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot()
        ax.barh(nombres.index, nombres.values)
        ax.set_xlabel("Nombre de crimes rapportés")
        ax.set_ylabel("Secteur")
        ax.set_title("Nombre de crimes par secteur")
        fig.tight_layout()
        return fig
        

    def par_lieu(self):
        nombres = self.donnees["type_lieu"].value_counts().head(10)
        nombres = nombres.sort_values()

        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot()
        ax.barh(nombres.index, nombres.values)
        ax.set_xlabel("Nombre de crimes rapportés")
        ax.set_ylabel("Type de lieu")
        ax.set_title("Les 10 types de lieux avec le plus de crimes rapportés")
        fig.tight_layout()
        return fig
    
    def par_age(self):
        tranches = pd.cut(
            self.donnees["age"],
            bins=LIMITES_AGE,
            labels=NOMS_AGE
        )
        nombres = tranches.value_counts()
        nombres = nombres.reindex(NOMS_AGE, fill_value=0)

        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot()
        ax.bar(nombres.index, nombres.values)
        ax.set_xlabel("Tranche d’âge")
        ax.set_ylabel("Nombre de crimes rapportés")
        ax.set_title("Crimes rapportés selon l’âge de la victime")
        fig.tight_layout()
        return fig
