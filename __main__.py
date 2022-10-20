import pandas as pd
from utils_project import *

if __name__ == '__main__':
    dfAliments = pd.read_excel(FICHIER_ALIMENTS)
    dfSondage = pd.read_excel(FICHIER_SONDAGE)
    
    for nomPreference in PREFERENCES_ALIMENTAIRES.keys():
        #Ajout pour chaque aliment de leur appartenance ou non à toutes les catégories
        dfAliments[nomPreference] = correspondanceAlimentaire(dfAliments, nomPreference)

        #Ajout pour chaque sondé, du nombre d'aliments consommés par catégorie
        dfSondage["nb" + nomPreference] = getNbTypeAlimentsCategorieGlobal(dfSondage, dfAliments, nomPreference)
        
        #Sauvegarde du fichier créé
        listePreferenceAlimentaire(dfSondage, nomPreference)