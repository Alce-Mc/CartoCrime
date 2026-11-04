import matplotlib.pyplot as plt
import pandas as pd
from risk_calculator import LIMITES_AGE, NOMS_AGE

class Graphiques:
    def __init__(self, donnees):
        self.donnees = donnees

    def par_heure(self):
        nombres = self.donnees["heure"].value_counts()
        nombres = nombres.reindex(range(24), fill_value=0)
        plt.figure()
        plt.bar(nombres.index, nombres.values)
        plt.xlabel("Heure")
        plt.ylabel("Nombre de crimes rapportés")
        plt.title("Nombre de crimes selon l’heure")
        plt.xticks(range(24))
        plt.tight_layout()
        plt.show()
    
    def carte_chaleur(self):
        comptes = self.donnees.groupby(["jour_semaine", "heure"]).size()
        tableau = comptes.unstack(fill_value=0)
        tableau = tableau.reindex(
            index=range(7), columns=range(24), fill_value=0
        )

        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi",
                 "Vendredi", "Samedi", "Dimanche"]

        plt.figure(figsize=(12, 5))
        plt.imshow(tableau, cmap="YlOrRd", aspect="auto")
        plt.colorbar(label="Nombre de crimes rapportés")
        plt.xticks(range(24))
        plt.yticks(range(7), jours)
        plt.xlabel("Heure")
        plt.ylabel("Jour de la semaine")
        plt.title("Crimes rapportés selon le jour et l’heure")
        plt.tight_layout()
        plt.show()

    def par_secteur(self):
        nombres = self.donnees["secteur"].value_counts()
        nombres = nombres.sort_values()

        plt.figure(figsize=(10, 8))
        plt.barh(nombres.index, nombres.values)
        plt.xlabel("Nombre de crimes rapportés")
        plt.ylabel("Secteur")
        plt.title("Nombre de crimes par secteur")
        plt.tight_layout()
        plt.show()

    def par_lieu(self):
        nombres = self.donnees["type_lieu"].value_counts().head(10)
        nombres = nombres.sort_values()

        plt.figure(figsize=(12, 6))
        plt.barh(nombres.index, nombres.values)
        plt.xlabel("Nombre de crimes rapportés")
        plt.ylabel("Type de lieu")
        plt.title("Les 10 types de lieux avec le plus de crimes rapportés")
        plt.tight_layout()
        plt.show()

    def par_age(self):
        tranches = pd.cut(
            self.donnees["age"],
            bins=LIMITES_AGE,
            labels=NOMS_AGE
        )
        nombres = tranches.value_counts()
        nombres = nombres.reindex(NOMS_AGE, fill_value=0)

        plt.figure(figsize=(8, 5))
        plt.bar(nombres.index, nombres.values)
        plt.xlabel("Tranche d’âge")
        plt.ylabel("Nombre de crimes rapportés")
        plt.title("Crimes rapportés selon l’âge de la victime")
        plt.tight_layout()
        plt.show()

