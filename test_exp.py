from chargeur_donnees import ChargeurDonnees
from risk_calculator import CalculateurRisque
from exportation import Exportation

chargeur = ChargeurDonnees("export.csv")
donnees = chargeur.charger()

scenario = {
    "secteur": "Hollywood",
    "jour_semaine": 0,
    "heure": 18,
    "age": 19,
    "sexe": "M"
}

calculateur = CalculateurRisque(donnees)
resultat = calculateur.calculer_indice(scenario)
top_crimes = calculateur.top_crimes(scenario)

exportation = Exportation()
exportation.exporter(
    "rapport_test.txt", scenario, resultat, top_crimes, donnees
)
print("Rapport enregistré dans rapport_test.txt")