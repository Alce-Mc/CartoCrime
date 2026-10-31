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

# Nombre minimal d'incidents pour que le top de crimes soit faible
MIN_INCIDENTS_TOP = 30


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


    @staticmethod
    def _tranche_age(age):
        """Retourne la tranche d'âge correspondante à l'âge donné."""
        if age is None:
            return None
        resultat = pd.cut([age], bins=LIMITES_AGE, labels=NOMS_AGE)[0]      
        return None if pd.isna(resultat) else str(resultat)

    def _valeur_du_scenario(self, scenario: dict):  #scenario est un dictionnarie
        """"Facteurs réellement forunis pas l'utilisateur (les champs vides sont ignorées)"""

        valeurs = {
            "secteur": scenario.get("secteur"),
            "type_lieu": scenario.get("type_lieu"),
            "jour_semaine": scenario.get("jour_semaine"),
            "heure": scenario.get("heure"),
            "tranche_age": scenario.get("tranche_age"),
            "sexe": scenario.get("sexe")
        }
        return {cle:valeur for cle, valeur, in valeurs.items() if valeur is not None}
    #retourne un dictionnaire

    def calculer_indice(self, scenario: dict):
        """Indice partiel = incidents de la valeur / moyenne de référence du facteur.
        Indice globale = moyenne géométrique des indices partiels (1.0 = risque moyen)."""
        partiels = {}
        for facteur, valeur in self._valeur_du_scenario(scenario).items():
            comptes, moyenne = self._frequences[facteur]
            partiels[facteur] = float(comptes.get(valeur,0) / moyenne)

        if not partiels:
            raise ValueError("Le scénario ne contient aucun facteur.")

        dominant = ""
        ecart_max = -1
        for facteur, valeur in partiels.items():
            ecart = abs(valeur - 1)
            if ecart > ecart_max:
                ecart_max = ecart
                dominant = facteur

        return ResultatRisque(
            indice=round(indice,2),
            categorie=self._categorie(indice),
            indices_partiels={f: round(v, 2) for f,v in partiels.items()},
            facteur_dominant=dominant
        )
    #retourne un ResultatRisque

    @staticmethod
    def _categorie(indice : float):
        if indice < SEUILS_FAIBLE:
            return "faible"
        if indice <= SEUILS_ELEVES:
            return "moyen"
        return "élevé"
    #retourne un string
    

                            #...Le top des crimes...

    def top_crimes(self, scenario: dict, n: int = 5): #n est un int = 5.
        """Les n (pour l'instant 5) crimes les plus fréquents pour le scénario.
        Si le scénario complet donne pas assez d'incidents, on retombe sur le secteur seul."""

        masque = self.donnees["secteur"] == scenario["secteur"]
        for facteur, valeur in self._valeur_du_scenario(scenario).items():
            if facteur != "secteur":
                masque &= self.donnees[facteur] == valeur
        selection = self.donnees[masque]

        if len(selection) < MIN_INCIDENTS_TOP:
            selection = self.donnees[self.donnees["secteur"] == scenario["secteur"]]

        return selection["type_crime"].value_counts().head(n)
# Retourne une serie pandas.

    