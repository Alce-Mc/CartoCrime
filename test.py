import pandas as pd
from graphiques import Graphiques

donnees = pd.DataFrame({
    "heure": [8, 8, 9, 12, 12, 12, 18, 18, 22]
})

graphiques = Graphiques(donnees)
graphiques.par_heure()