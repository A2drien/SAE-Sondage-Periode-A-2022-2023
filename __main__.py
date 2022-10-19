from email import utils
import pandas
from utils_project import *

if __name__ == '__main__':
    dfAliments = pandas.read_excel(FICHIER_ALIMENTS)
    dfSondage = pandas.read_excel(FICHIER_SONDAGE)

    for nomPreference in PREFERENCES_ALIMENTAIRES.keys():
        dfAliments[nomPreference] = correspondanceAlimentaire(dfAliments, nomPreference)

    # Facultatif, sert au debug
    dfAliments.to_excel('Aliment-modif.xlsx', index=False)

    for nomPreference in PREFERENCES_ALIMENTAIRES.keys():
        dfSondage["nb" + nomPreference] = [getNbTypeAliment(personne, dfAliments, nomPreference) for personne in dfSondage.values]
