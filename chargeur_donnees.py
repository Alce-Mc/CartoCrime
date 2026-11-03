import pandas as pd
import numpy as np

class ChargeurDonnees:
    """Classe pour charger les données du csv"""

    def __init__(self, chemin):
        self.chemin = chemin
        self.donnees = None

    def charger(self):
        #Lire seulement les colonnes utiles, car il a beaucoup de colonnes.
        df = pd.read_csv(self.chemin, usecols=["DATE OCC", "TIME OCC", "AREA NAME", "Premis Desc", "Crm Cd Desc", "Vict Age", "Vict Sex"])  

        #Le renommer pour que ça soit comme risk_calculator s'attend.
        df = df.rename(columns={"AREA NAME": "secteur", "Premis Desc": "type_lieu", "Crm Cd Desc": "type_crime", "Vict Age": "age", "Vict Sex": "sexe"})

        #Date, jour de la semaine (0 = lundi) et heure (2200 devient 22).
        df["date"] = pd.to_datetime(df["DATE OCC"], format="%Y %b %d %I:%M:%S %p", errors="coerce")
        df["jour_semaine"] = df["date"].dt.dayofweek
        df["heure"] = pd.to_numeric(df["TIME OCC"], errors="coerce") // 100

        #Enlever les lignes sans dates ou avec des heures impossibles.
        df = df.dropna(subset=["date", "heure"])
        df = df[(df["heure"] >= 0) & (df["heure"] <= 23)].copy()
        df["heure"] = df["heure"].astype(int)

        #Mettre les ages invalides au vide, mais on garde la ligne
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df.loc[(df["age"] <= 0) | (df["age"] > 100), "age"] = np.nan

        #On garde les sexe F et M puis le reste devient X
        df.loc[~df["sexe"].isin(["F", "M"]), "sexe"] = "X"

        #On remplace les valeurs manquantes seulement dans les colonnes de texte
        colonnes_texte = ["secteur", "type_lieu", "type_crime"]
        df[colonnes_texte] = df[colonnes_texte].fillna("INCONNU")

        #Pour garder seulement les colonnes qu'on a besoin dans le calculateur de risque.
        df = df[["date", "jour_semaine", "heure", "secteur", "type_lieu", "type_crime", "age", "sexe"]]

        self.donnees = df.reset_index(drop=True)
        return self.donnees

    def secteurs(self):
        return sorted(self.donnees["secteur"].unique())

    def types_lieux(self):
        return sorted(self.donnees["type_lieu"].unique())