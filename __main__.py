import pandas as pd
import utils_project as up

if __name__ == '__main__':
    dfAliments = pd.read_excel(up.FICHIER_ALIMENTS)
    dfSondage = pd.read_excel(up.FICHIER_SONDAGE)

    up.attribuerNutriScoreAliments(dfAliments)
    
    #Question 1a
    print("Question 1a) :")
    for nomPreference in up.PREFERENCES_ALIMENTAIRES.keys():
        #Ajout pour chaque aliment de leur appartenance ou non à toutes les catégories
        dfAliments[nomPreference] = up.correspondanceAlimentaire(dfAliments, nomPreference)

        #Ajout pour chaque sondé, du nombre d'aliments consommés par catégorie
        dfSondage[up.getNomColonneCompteur(nomPreference)] = up.getNbTypeAlimentsCategorieGlobal(dfSondage, dfAliments, nomPreference)
        
        #Sauvegarde du fichier créé
        up.listePreferenceAlimentaire(dfSondage, nomPreference)
    
    #Question 1b
    print("\nQuestion 1b) :")
    listeCategorieAlimentaire = up.getCategoriesAlimentaires(dfAliments)

    for nomCategorie in listeCategorieAlimentaire:
        dfSondage[up.getNomColonneCompteur(nomCategorie)] = up.truc(dfSondage, dfAliments, nomCategorie)
    
    up.camembertToutesCategories(dfSondage, listeCategorieAlimentaire)


    print("Question 2) :")
    dfAliments["NutriScore"] = up.attribuerNutriScoreAliments(dfAliments)

    dfAliments.to_excel("test.xlsx", index=False, columns=['alim_code', 'alim_nom_fr', 'NutriScore'])