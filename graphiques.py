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
