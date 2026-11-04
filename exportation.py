class Exportation:
    def exporter(self, chemin, scenario, resultat, top_crimes, donnees):
           with open(chemin, "w", encoding="utf-8") as fichier:
            fichier.write("RAPPORT CARTOCRIME\n\n")

            fichier.write("SCÉNARIO\n")
            for cle, valeur in scenario.items():
                fichier.write(f"{cle} : {valeur}\n")

            fichier.write("\nRÉSULTATS\n")
            fichier.write(f"Indice relatif : {resultat.indice}\n")
            fichier.write(f"Catégorie : {resultat.categorie}\n")
            fichier.write(
                f"Facteur dominant : {resultat.facteur_dominant}\n"
            )
            fichier.write("\nTOP 5 DES CRIMES\n")
            fichier.write(
                "Si le scénario contient moins de 30 incidents, "
                "le classement porte sur le secteur entier.\n"
            )
            for crime, nombre in top_crimes.items():
                fichier.write(f"{crime} : {nombre}\n")

            debut = donnees["date"].min().strftime("%Y-%m-%d")
            fin = donnees["date"].max().strftime("%Y-%m-%d")

            fichier.write("\nDONNÉES UTILISÉES\n")
            fichier.write("Source : données ouvertes du LAPD\n")
            fichier.write(f"Période : du {debut} au {fin}\n")
            fichier.write(f"Nombre total de crimes chargés : {len(donnees)}\n")
            fichier.write(
                "\nCet indice décrit les données historiques et ne "
                "représente pas une probabilité personnelle d’être victime.\n"
            )