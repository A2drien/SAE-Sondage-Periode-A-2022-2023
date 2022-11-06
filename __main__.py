import pandas as pd
import utils_project as up

if __name__ == '__main__':
    dfAliments = pd.read_excel(up.FICHIER_ALIMENTS)
    dfSondage = pd.read_excel(up.FICHIER_SONDAGE)

    # Question 1a
    for nomPreference in up.PREFERENCES_ALIMENTAIRES.keys():
        # Ajout pour chaque aliment de leur appartenance ou non à toutes les catégories
        dfAliments[nomPreference] = up.correspondanceAlimentaire(
            dfAliments, nomPreference)

        # Ajout pour chaque sondé, du nombre d'aliments consommés par catégorie
        dfSondage[up.getNomColonneCompteur(nomPreference)] = up.getNbTypeAlimentsCategorieGlobal(
            dfSondage, dfAliments, nomPreference)

        # Sauvegarde du fichier créé
        up.listePreferenceAlimentaire(dfSondage, nomPreference)

    # Question 1b
    listeCategorieAlimentaire = up.getCategoriesAlimentaires(dfAliments)

    for nomCategorie in listeCategorieAlimentaire:
        dfSondage[up.getNomColonneCompteur(nomCategorie)] = up.getNbAlimentsCategorie(
            dfSondage, dfAliments, nomCategorie)

    # Sauvegarde du camembert
    up.camembertToutesCategories(dfSondage, listeCategorieAlimentaire)

    # Question 2
    #Calcul du nutriscore
    dfSondage[up.NOM_COLONNE_NUTRISCORE] = up.nutriScorePersonnes(
        dfSondage, dfAliments)

    # Sauvegarde du nutriscore
    up.sauvegardeNutriScore(dfSondage)

    dfAliments.to_excel("test.xlsx", index=False, columns=[
                        "alim_code", "alim_nom_fr", "alim_grp_nom_fr", "Bio", "Vegan", "Casher", "Halal"])
