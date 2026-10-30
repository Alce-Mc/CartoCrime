#Test des calculs ajustables pour pouvoir confirmer certain calcul fait dans mes autres fichiers.

from chargeur_donnees import ChargeurDonnees
from risk_calculator import CalculateurRisque

chargeur = ChargeurDonnees("data/export.csv")
df = chargeur.charger()
calc = CalculateurRisque(df)
secteurs = chargeur.secteurs()
print(len(df), "lignes,", len(secteurs), "secteurs\n")

print(secteurs)

scenario = {
    "secteur": "Hollywood",
    "heure": 10,
    "age": 78,
    "sexe" : "M",
    #"type_lieu": "STREET",
    #"jour_semaine": 5
}

resultat = calc.calculer_indice(scenario)
print(resultat)
print(calc.top_crimes(scenario))