"""Calcul de l'indice de risque relatif et du top des crimes"""

from symtable import Class

import numpy as np
import pandas as pd

LIMITES_AGE = [0,17,29,44,59,100]
NOMS_AGE = ['0-17','18-29','30-44','45-59','60+']

# Une seule valeur de seuil est utilisée pour déterminer si un crime est représentatif ou non.
# Si on utilise tous les valeurs qui aont presque jamais été observées, on risque d'avoir des résultats biaisés,
# puis la moyenne sera faussée. On choisit donc un seuil de représentativité pour ne garder que les crimes qui ont été observés au moins 1% du temps.
SEUIL_REPRESENTATIVITE = 0.01

# Seuils des catégories de risque (à ajuster)
SEUILS_FAIBLE = 0.8
SEUILS_ELEVES = 1.2


class ResultatRisque:
    def __init__(self, indice, categorie, indices_partiels, facteur_dominant):
        self.indice = indice                            # Indice du risque relatif
        self.categorie = categorie                      # Catégorie de risque (faible, moyen, élevé)
        self.indices_partiels = indices_partiels        # ex "heure": 1.8, "secteur": 0.5, "age": 1.2, "sexe": 1.0
        self.facteur_dominant = facteur_dominant        # facteur qui a le plus contribué à l'indice de risque relatif


    def __str__(self):
        return f"Indice: {self.indice}, Catégorie: {self.categorie}, Indices partiels: {self.indices_partiels}, Facteur dominant: {self.facteur_dominant}"




class CalculateurRisque:
    """Classe pour calculer l'indice de risque relatif et le top des crimes à  partir du Dataframe nettoyé."""

    def __init__(self, donnees):
        self.donnees = donnees.copy()  # Copie du DataFrame pour éviter de modifier l'original
        self.donnees["tranche d'âge"] = pd.cut(self.donnees['age'], bins=LIMITES_AGE, labels=NOMS_AGE)
        self._frequences = self._calculer_frequences()

    def _calculer_frequences(self):      # Ça return un dictionnaire.
        """premiere methode: pour chaque facteur, on fait nb dincidents par valeur + la moyenne de reference."""
        total = len(self.donnees)
        frequences = {}
        for facteur in ["secteur", "type_lieu", "jour_semaine", "heure", "tranche d'âge", "sexe"]:
            comptes = self.donnees[facteur].value_counts()
            representatifs = comptes[comptes >= SEUIL_REPRESENTATIVITE * total]
            moyenne = representatifs.mean() if len(representatifs) else comptes.mean()
            frequences[facteur] = (comptes, moyenne)

        return frequences
