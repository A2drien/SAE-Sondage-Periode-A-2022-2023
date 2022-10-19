import string
from pandas import DataFrame

FICHIER_ALIMENTS = "Aliments.xlsx"
FICHIER_SONDAGE = "Sondage.xlsx"

_NOM_COLONNE_ALIMENT = 'alim_nom_fr'
_NOM_COLONNE_SPECIFICATION_ALIMENTS = 'alim_ssssgrp_nom_fr'
_NOM_COLONNE_NUM_PRODUIT = 'alim_code'
_NOM_COLONNE_NB_ALIMENTS = 'Administré.e'


PREFERENCES_ALIMENTAIRES: dict[str, tuple[str, list[str], list[str]]] = {
    "Bio":      (
        _NOM_COLONNE_ALIMENT,
        ['bio'],
        ['biovive']
    ),

    "Vegan":    (
        _NOM_COLONNE_ALIMENT,
        ['vegan', 'végan'],
        []
    ),

    "Casher":   (
        _NOM_COLONNE_SPECIFICATION_ALIMENTS,
        ['casher'],
        []
    ),

    "Halal":    (
        _NOM_COLONNE_SPECIFICATION_ALIMENTS,
        ['halal'],
        []
    )
}


def _getNumLigneProduct(dfAliments: DataFrame, idProduct: int) -> int:
    """Renvoie le numéro de la ligne du produit donné en paramètre

    Args:
        dfAliments (DataFrame): DataFrame du fichier "Aliment"
        idProduct (int): Numéro du produit

    Returns:
        int: Numéro de ligne du produit
    """
    return dfAliments[dfAliments[_NOM_COLONNE_NUM_PRODUIT] == idProduct].index.to_list()[0]


def _estEtat(dfAliments: DataFrame, idProduct: int, nomColonne: str) -> bool:
    """Retourne la valeur booléenne de la colonne du produit données en paramètre

    Args:
        dfAliments (DataFrame): DataFrame du fichier "Aliments"
        idProduct (int): Numéro du produit
        nomColonne (str): Nom de la colonne

    Returns:
        bool: Valeur de la colonne (et donc de l'état recherché)
    """
    return dfAliments[nomColonne][_getNumLigneProduct(dfAliments, idProduct)].to_lower() == 'true'


def _getListeAliment(dfSondage: DataFrame, idxSonde: int) -> list[int]:
    """Revoie la liste des numéro de produits indiqués par le sondé

    Args:
        dfSondage (DataFrame): DataFrame du fichier "Sondage"
        idxSonde (int): Index du sondé

    Returns:
        list[int]: Liste des numéros de produits
    """
    nbAliments = int(dfSondage[_NOM_COLONNE_NB_ALIMENTS][idxSonde])
    listeAliments = []

    while nbAliments > 0:
        listeAliments.append(dfSondage[f'Aliment{nbAliments}'][idxSonde])

    return listeAliments


def getNbTypeAliment(listeIdProduct: list[int], dfAliments: DataFrame, colonneTypeAliment: str):
    """Retourne le

    Args:
        listeIdProduct (list[int]): _description_
        dfAliments (DataFrame): _description_
        colonneTypeAliment (str): _description_

    Returns:
        _type_: _description_
    """
    nbOccurrence = 0
    for idProduct in listeIdProduct:
        nbOccurrence += _estEtat(dfAliments, idProduct, colonneTypeAliment)
    return nbOccurrence


def _supprimerExceptions(string: str, exceptions: list[str]) -> str:
    exceptions.sort(key=len, reverse=True)
    for exception in exceptions:
        string = string.replace(exception, '')
    return string


def correspondanceAlimentaire(dfAliment: DataFrame, nomPreference: str) -> list[bool]:
    nomColonne, correspondances, exceptions = PREFERENCES_ALIMENTAIRES[nomPreference]

    L: list[bool] = []
    for label in dfAliment[nomColonne]:
        if any(correspondance in _supprimerExceptions(label.lower(), exceptions) for correspondance in correspondances):
            L.append(True)
            print(f"{nomPreference} : {label}")
        else:
            L.append(False)
    return L
