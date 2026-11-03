from chargeur_donnees import ChargeurDonnees
from graphiques import Graphiques

chargeur = ChargeurDonnees("export.csv")
donnees = chargeur.charger()

print("Nombre de crimes chargés :", len(donnees))

masque = donnees["secteur"] == "Hollywood"
donnees_secteur = donnees[masque]

graphiques = Graphiques(donnees_secteur)
graphiques.par_age()