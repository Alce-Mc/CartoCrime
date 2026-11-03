import matplotlib.pyplot as plt

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
