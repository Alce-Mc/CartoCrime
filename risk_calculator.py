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
    def __innit__(self, indice, categorie, indices_partiels, indice_dominant):
        self.indice = indice
        self.categorie = categorie
        self.indices_partiels = indices_partiels
        self.indice_dominant = indice_dominant

    