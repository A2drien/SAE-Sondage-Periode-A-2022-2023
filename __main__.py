import pandas as pd
from utils_project import *

if __name__ == '__main__':
    dfAliments = pd.read_excel(FICHIER_ALIMENTS)
    dfSondage = pd.read_excel(FICHIER_SONDAGE)
    
    #Question 1a
    for nomPreference in PREFERENCES_ALIMENTAIRES.keys():
        #Ajout pour chaque aliment de leur appartenance ou non à toutes les catégories
        dfAliments[nomPreference] = correspondanceAlimentaire(dfAliments, nomPreference)

        #Ajout pour chaque sondé, du nombre d'aliments consommés par catégorie
        dfSondage[getNomColonneCompteur(nomPreference)] = getNbTypeAlimentsCategorieGlobal(dfSondage, dfAliments, nomPreference)
        
        #Sauvegarde du fichier créé
        listePreferenceAlimentaire(dfSondage, nomPreference)
    
    #Question 1b
    listeCategorieAlimentaire = getCategoriesAlimentaires(dfAliments)
    for nomCategorie in listeCategorieAlimentaire:
        pass