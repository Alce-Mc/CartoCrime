"""Calcul de l'indice de risque relatif et du top des crimes"""

import numpy as np
import pandas as pd

LIMITES_AGE = [0,17,29,44,59,100]
NOMS_AGE = ['0-17','18-29','30-44','45-59','60+']

# Une seule valeur de seuil est utilisée pour déterminer si un crime est représentatif ou non.
# Si on utilise tous les valeurs qui aont presque jamais été observées, on risque d'avoir des résultats biaisés,
# puis la moyenne sera faussée. On choisit donc un seuil de représentativité pour ne garder que les crimes qui ont été observés au moins 1% du temps.
SEUIL_REPRESENTATIVITE = 0.01

# Seuils des catégories de risque (à ajuster)
SEUILS_FAIBLE = 0.90
SEUILS_ELEVES = 1.02

# Nombre minimal d'incidents pour que le top de crimes soit fiable
MIN_INCIDENTS_TOP = 30

# C'est les facteurs qu'on compare à l'intérieur du secteur et non en globalité.
FACTEURS_DANS_SECTEUR = ["jour_semaine", "heure", "tranche_age", "sexe"]


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
        self.donnees["tranche_age"] = pd.cut(self.donnees['age'], bins=LIMITES_AGE, labels=NOMS_AGE)
        self._ref_secteur = self._calculer_reference(self.donnees, "secteur")       # C'est la référence du secteur qui est calculé sur tout le fichier (un secteur vs un autre)
        self._refs_par_secteur = {}   # C'est la référence des facteurs qui sont calculés une fois par secteur et stocker ici.

    def _calculer_reference(self, donnees, facteur):      # Ça return un dictionnaire.
        """Pour un facteur dans un ensemble de données: nb d'incidents par valeur + moyenne de référence."""
        total = len(self.donnees)
        comptes = donnees[facteur].value_counts()
        if facteur == "heure" and 12 in comptes.index:
            comptes = comptes.astype(float)
            comptes[12] = (comptes.get(11, 0) + comptes.get(13, 0)) / 2
        # J'ai remarqué qu'il avait un grand pic de crimes à exactement midi, que je trouvais très anormal. Alors, on remplace le compte de 12h pour la moyenne de 11 et 13h.

        representatifs = comptes[comptes >= SEUIL_REPRESENTATIVITE *total]
        moyenne = representatifs.mean() if len(representatifs) else comptes.mean()

        return comptes, moyenne

    def _reference_du_secteur(self, secteur):
        """Références de chaque facteur calculés seulement avec les inicdents de ce secteur ci."""
        if secteur not in self._refs_par_secteur:
            sous_ensemble = self.donnees[self.donnees["secteur"] == secteur]
            references = {}
            for facteur in FACTEURS_DANS_SECTEUR:
                references[facteur] = self._calculer_reference(sous_ensemble, facteur)
            self._refs_par_secteur[secteur] = references
        return self._refs_par_secteur[secteur]


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
            "tranche_age": self._tranche_age(scenario.get("age")),  #scenario.get("age"), va trouver l'age exacte, puis tranche_age va la trasnformer en tranche.
            "sexe": scenario.get("sexe")
        }
        return {cle:valeur for cle, valeur in valeurs.items() if valeur is not None}
    #retourne un dictionnaire

    def calculer_indice(self, scenario: dict):
        """Indice partiel = incidents de la valeur / moyenne de référence du facteur.
        Indice globale = moyenne géométrique des indices partiels (1.0 = risque moyen)."""

        valeurs = self._valeur_du_scenario(scenario)
        if "secteur" not in valeurs:
            raise ValueError(f"Le secteur est obligatoire")

        secteur = valeurs["secteur"]
        comptes_secteurs, moyenne_secteurs = self._ref_secteur
        if secteur not in comptes_secteurs.index:
            raise ValueError(f"Secteur inconnu : {secteur}")

        partiels = {"secteur": float(comptes_secteurs[secteur] / moyenne_secteurs)}

        references = self._reference_du_secteur(secteur)
        for facteur, valeur in valeurs.items():
            if facteur in references:               # Ici on ignore type_lieu et le secteur
                comptes, moyenne = references[facteur]
                partiels[facteur] = float(comptes.get(valeur, 0) / moyenne)

        produit = 1
        for valeur in partiels.values():
            produit *= max(valeur, 0.01)  #évite qu'un 0 mette tout l'indice à 0.
        indice = produit ** (1/ len(partiels))

        dominant = ""
        ecart_max = -1
        for facteur, valeur in partiels.items():
            ecart = abs(valeur - 1)
            if ecart > ecart_max:
                ecart_max = ecart
                dominant = facteur

        return ResultatRisque(
            indice = round(indice,2),
            categorie = self._categorie(indice),
            indices_partiels = {f: round(v, 2) for f,v in partiels.items()},
            facteur_dominant = dominant
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
