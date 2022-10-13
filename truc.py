import pandas
from utils_project import *

dfAliments = pandas.read_excel(FILE_NAME_ALIMENTS)

dfAliments[COLONNE_EST_BIO] = ['bio' in nom_aliment for nom_aliment in dfAliments[COLUMN_NAME_ALIMENTS]]
dfAliments[COLONNE_EST_VEGAN] = ['vegan' in nom_aliment for nom_aliment in dfAliments[COLUMN_NAME_ALIMENTS]]
dfAliments[COLONNE_EST_CASHER] = ['casher' in groupe_aliment for groupe_aliment in dfAliments[COLUMN_NAME_SPECIFIC_ALIMENTS]]
dfAliments[COLONNE_EST_HALAL] = ['halal' in groupe_aliment for groupe_aliment in dfAliments[COLUMN_NAME_SPECIFIC_ALIMENTS]]

#Facultatif, sert au debug
dfAliments.to_excel('Aliment-modif.xlsx', index=False)


dfSondage = pandas.read_excel(FILE_NAME_HABITANT)


