from pandas import DataFrame
from os import path, makedirs
from matplotlib.pyplot import pie, legend, savefig

FICHIER_ALIMENTS = "Aliments.xlsx"
FICHIER_SONDAGE = "Sondage.xlsx"

_NOM_COLONNE_ALIMENT = 'alim_nom_fr'
_NOM_COLONNE_SPECIFICATION_ALIMENTS = 'alim_ssssgrp_nom_fr'
_NOM_COLONNE_NUM_PRODUIT = 'alim_code'
_NOM_COLONNE_NB_ALIMENTS = 'Administré.e'

_DONNEES_SONDE: list[str] = ['Administré.e', "Nom", "Prénom"]

_NOM_DOSSIER_Q1a = 'Question-1a/'
_NOM_DOSSIER_Q1b = 'Question-1b/'

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
    return bool(dfAliments[nomColonne].iloc[_getNumLigneProduct(dfAliments, idProduct)])


def _getListeAliments(dfSondage: DataFrame, idxSonde: int) -> list[int]:
    """Revoie la liste des numéro de produits indiqués par le sondé

    Args:
        dfSondage (DataFrame): DataFrame du fichier "Sondage"
        idxSonde (int): Index du sondé

    Returns:
        list[int]: Liste des numéros de produits
    """
    nbAliments = int(dfSondage[_NOM_COLONNE_NB_ALIMENTS].iloc[idxSonde])
    listeAliments = []

    while nbAliments > 0:
        listeAliments.append(dfSondage[f'Aliment{nbAliments}'].iloc[idxSonde])
        nbAliments -= 1

    return listeAliments


def _getNbTypeAlimentCategorieIndividuel(listeIdProduct: list[int], dfAliments: DataFrame, colonneTypeAliment: str) -> int:
    """Renvoie le nombre d'aliments consommé dans une catégorie précisée

    Args:
        listeIdProduct (list[int]): Liste des aliments consommés
        dfAliments (DataFrame): DataFrame des aliments
        colonneTypeAliment (str): Nom de la catégorie recherchée

    Returns:
        int: Nombre d'aliments de la catégorie recherchée
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

    L = []
    for label in dfAliment[nomColonne]:
        if any(correspondance in _supprimerExceptions(label.lower(), exceptions) for correspondance in correspondances):
            L.append(True)
        else:
            L.append(False)
    return L


def getNbTypeAlimentsCategorieGlobal(dfSondage: DataFrame, dfAliments: DataFrame, nomCategorie: str) -> list[int]:
    """Retourne, pour tous les sondés, le nombre d'aliments correspondant à la catégorie demandée

    Args:
        dfSondage (DataFrame): DataFrame des sondés
        dfAliments (DataFrame): DataFrame des aliments
        nomCategorie (str): Nom de la catégorie des aliments à rechercher

    Returns:
        list[int]: Nombre d'aliments correspondant à la catégorie demandée
    """
    listeNbTypeAlimentsCategorieGlobal = []

    for idxSonde in range(len(dfSondage.values)):
        listeAliments = _getListeAliments(dfSondage, idxSonde)
        nbTypeAlimentsCategorieGlobal = _getNbTypeAlimentCategorieIndividuel(
            listeAliments, dfAliments, nomCategorie)
        listeNbTypeAlimentsCategorieGlobal.append(
            nbTypeAlimentsCategorieGlobal)

    return listeNbTypeAlimentsCategorieGlobal


def _creerDossier(nomDossier: str) -> None:
    if not path.exists(nomDossier):
        makedirs(nomDossier)


def _alerteGeneration(nomFichier: str) -> None:
    print(f"Fichier '{nomFichier}' généré !")

def listePreferenceAlimentaire(dfSondage: DataFrame, nomCategorie: str) -> None:
    _creerDossier(_NOM_DOSSIER_Q1a)
    
    dfSondage.sort_values(by=["nb"+nomCategorie], ascending=False)
   
    nomFichier = f"Pref-{nomCategorie}.xlsx"
    dfSondage.to_excel(f"{_NOM_DOSSIER_Q1a}{nomFichier}", index=False, columns= _DONNEES_SONDE + ["nb"+nomCategorie])
    _alerteGeneration(nomFichier)

def camembertToutesCategories(dfSondage: DataFrame) -> None:
    _creerDossier(_NOM_DOSSIER_Q1b)

    listeNomCategories: list[str] = [nom for nom in PREFERENCES_ALIMENTAIRES.keys()]
    listeNbAlimentsCategories: list[int] = [dfSondage["nb" + nomCategorie].sum() for nomCategorie in PREFERENCES_ALIMENTAIRES.keys()]    
    
    pie(listeNbAlimentsCategories, labels = listeNomCategories, normalize = True, autopct = lambda x: str(round(x, 2)) + '%')
    legend()
    
    nomFichier = "Camembert-catg-alim.png"
    savefig(f"{_NOM_DOSSIER_Q1b}{nomFichier}")
    _alerteGeneration(nomFichier)