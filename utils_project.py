from aifc import Error
from pandas import DataFrame

FILE_NAME_ALIMENTS = "Aliments.xlsx"
FILE_NAME_HABITANT = "Sondage.xlsx"

COLUMN_NAME_ALIMENTS = 'alim_nom_fr'
COLUMN_NAME_SPECIFIC_ALIMENTS = 'alim_ssssgrp_nom_fr'
ID_PRODUCT = 'alim_code'

COLONNE_EST_BIO = 'estBio'
COLONNE_EST_VEGAN = 'estVegan'
COLONNE_EST_CASHER = 'estCasher'
COLONNE_EST_HALAL = 'estHalal'

COLONNE_NB_ALIMENTS = 'Administré.e'

LISTE_MOT_BIO = ['bio']
LISTE


def _getNumLigneProduct(dfAliments: DataFrame, idProduct: int) -> int:
    return dfAliments[dfAliments[ID_PRODUCT] == idProduct].index.to_list()[0]


def _estEtat(dfAliments: DataFrame, idProduct: int, nomColonne: str) -> bool:
    return dfAliments[nomColonne][_getNumLigneProduct(dfAliments, idProduct)].to_lower() == 'true'


def _getListeAliment(dfSondage: DataFrame, idxSonde: int) -> list[int]:
    nbAliments = int(dfSondage[COLONNE_NB_ALIMENTS][idxSonde])
    listeAliments = []

    while nbAliments > 0:
        listeAliments.append(dfSondage[f'Aliment{nbAliments}'][idxSonde])

    return listeAliments


def _getNbTypeAliment(listeIdProduct: list[int], dfAliments: DataFrame, colonneTypeAliment: str):
    nbOccurrence = 0
    for idProduct in listeIdProduct:
        nbOccurrence += _estEtat(dfAliments, idProduct, colonneTypeAliment)
    return nbOccurrence

def listeNbAlimentSpécifique(dfSondage: DataFrame, dfAliments: DataFrame, nomColonne: str) -> list[bool]:
    listeNbAlimentSpécifique = []
    nbSonde = len(dfSondage.index.to_list())
    for idxSonde in range(1, nbSonde+1):
        listeAliment = _getListeAliment(dfSondage, idxSonde)


truc = {'v', 'e'}

print(truc in list('te'))