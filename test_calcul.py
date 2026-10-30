#Test des calculs ajustables pour pouvoir confirmer certain calcul fait dans mes autres fichiers.
import pandas as pd

from chargeur_donnees import ChargeurDonnees
from risk_calculator import CalculateurRisque

chargeur = ChargeurDonnees("data/export.csv")
df = chargeur.charger()
calc = CalculateurRisque(df)
secteurs = chargeur.secteurs()
print(len(df), "lignes,", len(secteurs), "secteurs\n")

print(secteurs)

scenario = {
    "secteur": "Harbor",
    "heure": 12,
    "age": 45,
    "sexe" : "F",
    #"type_lieu": "STREET",
    #"jour_semaine": 4
}

resultat = calc.calculer_indice(scenario)
print(resultat)
print(calc.top_crimes(scenario))

# Mes test pour comprendre pourquoi est-ce que 12 heures est toujours plus elevés que les autres heures
"""
print(df["heure"].value_counts().sort_index())
for h in range(24):
    s = {"secteur": "Harbor", "heure": h, "age": 45, "sexe": "F"}
    print(h, calc.calculer_indice(s).indice)

brut = pd.read_csv("data/export.csv", usecols=["TIME OCC"])
print(brut["TIME OCC"].value_counts().head(10))
"""

# Tests pour trouver les meilleurs seuils pour mon indice. Cest comme ca que jai trouvé 0.77 et 0.95
def centiles(ages):
    indices = []
    for secteur in secteurs:
        for heure in range(24):
            for age in ages:
                for sexe in ["F", "M"]:
                    s = {"secteur": secteur, "heure": heure, "age": age, "sexe": sexe}
                    indices.append(calc.calculer_indice(s).indice)

    serie = pd.Series(indices)
    print("Ages", ages)
    print(serie.describe())
    print("33e centile :", serie.quantile(0.33), "| 67e centile :", serie.quantile(0.67))

centiles([10, 25, 40, 55, 70])   
centiles([25, 40, 55])              #Pour tester si les groupes dages exxtreme changent beaucoup les données