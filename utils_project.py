from unittest import case
from numpy import size
from pandas import DataFrame
from os import path, makedirs
from matplotlib.pyplot import pie, legend, savefig, figure, tight_layout, title

FICHIER_ALIMENTS = "Aliments.xlsx"
FICHIER_SONDAGE = "Sondage.xlsx"

_NB_ALIMENTS = 10

_NOM_COLONNE_ALIMENT: str                   = 'alim_nom_fr'
_NOM_COLONNE_CATEGORIE_ALIMENT: str         = "alim_grp_nom_fr"
_NOM_COLONNE_SPECIFICATION_ALIMENTS: str    = 'alim_ssssgrp_nom_fr'
_NOM_COLONNE_NUM_PRODUIT: str               = 'alim_code'

_NOM_COLONNE_SUCRE: str     = 'Sucres (g/100 g)'
_NOM_COLONNE_SEL: str       = 'Sel chlorure de sodium (g/100 g)'
_NOM_COLONNE_FIBRES: str    = 'Fibres alimentaires (g/100 g)'
_NOM_COLONNE_PROTEINES: str = ''

_DONNEES_SONDE: list[str] = ['Administré.e', "Nom", "Prénom"]

_NOM_CATEGORIE_VIANDE: str = 'viandes, œufs, poissons et assimilés'


_PENALITE_QUANTITE_SUCRE: list[float] =             [3.4, 6.8, 10, 14, 17, 20, 24, 27, 31, 34, 37, 41, 44, 48, 51]
_PENALITE_QUANTITE_SEL: list[float] =               [0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4]
_BONUS_QUANTITE_FIBRE : list[float] =               [0.7, 1.4, 2.2, 2.9, 3.6, 4.3, 5, 5.8]
_BONUS_QUANTITE_PROTEINES_NON_VIANDE: list[float] = [2.4, 4.8, 7.2, 9.6, 12, 14, 17]
_BONUS_QUANTITE_PROTEINES_VIANDE: list[float] =     [2.4, 4.8]


_NOM_DOSSIER_Q1a = 'Question-1a/'
_NOM_DOSSIER_Q1b = 'Question-1b/'
_NOM_FICHIER_Q1b = "Camembert-catg-alim.png"



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


def getNomColonneCompteur(nomCategorie: str):
    return "nb"+nomCategorie


def _getNumLigneProduct(dfAliments: DataFrame, idProduit: int) -> int:
    """Renvoie le numéro de la ligne du produit donné en paramètre

    Args:
        dfAliments (DataFrame): DataFrame du fichier "Aliment"
        idProduit (int): Numéro du produit

    Returns:
        int: Numéro de ligne du produit
    """
    return dfAliments[dfAliments[_NOM_COLONNE_NUM_PRODUIT] == idProduit].index.to_list()[0]


def _estEtat(dfAliments: DataFrame, idProduit: int, nomColonne: str) -> bool:
    """Retourne la valeur booléenne de la colonne du produit données en paramètre

    Args:
        dfAliments (DataFrame): DataFrame du fichier "Aliments"
        idProduit (int): Numéro du produit
        nomColonne (str): Nom de la colonne

    Returns:
        bool: Valeur de la colonne (et donc de l'état recherché)
    """
    return bool(dfAliments[nomColonne].iloc[_getNumLigneProduct(dfAliments, idProduit)])


def _getListeAliments(dfSondage: DataFrame, idxSonde: int) -> list[int]:
    """Revoie la liste des numéros de produits indiqués par le sondé

    Args:
        dfSondage (DataFrame): DataFrame du fichier "Sondage"
        idxSonde (int): Index du sondé

    Returns:
        list[int]: Liste des numéros de produits
    """
    listeAliments: list[int] = []

    for idxAliment in range(1, _NB_ALIMENTS+1):
        listeAliments.append(dfSondage[f'Aliment{idxAliment}'].iloc[idxSonde])

    return listeAliments


def _getNbTypeAlimentCategorieIndividuel(listeidProduit: list[int], dfAliments: DataFrame, colonneTypeAliment: str) -> int:
    """Renvoie le nombre d'aliments consommé dans une catégorie précisée

    Args:
        listeidProduit (list[int]): Liste des aliments consommés
        dfAliments (DataFrame): DataFrame des aliments
        colonneTypeAliment (str): Nom de la catégorie recherchée

    Returns:
        int: Nombre d'aliments de la catégorie recherchée
    """
    nbOccurrence = 0
    for idProduit in listeidProduit:
        nbOccurrence += _estEtat(dfAliments, idProduit, colonneTypeAliment)
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
        L.append(any(correspondance in _supprimerExceptions(
            label.lower(), exceptions) for correspondance in correspondances))
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
    listeNbTypeAlimentsCategorieGlobal: list[int] = []

    for idxSonde in range(len(dfSondage.values)):
        listeAliments = _getListeAliments(dfSondage, idxSonde)
        nbTypeAlimentsCategorieGlobal = _getNbTypeAlimentCategorieIndividuel(
            listeAliments, dfAliments, nomCategorie)
        listeNbTypeAlimentsCategorieGlobal.append(
            nbTypeAlimentsCategorieGlobal)

    return listeNbTypeAlimentsCategorieGlobal


def _creerDossier(nomDossier: str) -> None:
    """Crée un dossier s'il n'existe pas encore

    Args:
        nomDossier (str): Nom du dossier à créer
    """
    if not path.exists(nomDossier):
        makedirs(nomDossier)


def _alerteGeneration(nomFichier: str) -> None:
    """Affiche dans la console qu'un fichier a été généré

    Args:
        nomFichier (str): Nom du fichier généré
    """
    print(f"\tFichier '{nomFichier}' généré !")


def listePreferenceAlimentaire(dfSondage: DataFrame, nomCategorie: str) -> None:
    _creerDossier(_NOM_DOSSIER_Q1a)

    dfSondage.sort_values(by=[getNomColonneCompteur(nomCategorie)], ascending=False)

    nomFichier = f"Pref-{nomCategorie}.xlsx"
    dfSondage.to_excel(f"{_NOM_DOSSIER_Q1a}{nomFichier}",
                       index=False, columns=_DONNEES_SONDE + [getNomColonneCompteur(nomCategorie)])
    _alerteGeneration(nomFichier)


def getCategoriesAlimentaires(dfAliments: DataFrame) -> list[str]:
    return list(set(dfAliments[_NOM_COLONNE_CATEGORIE_ALIMENT].tolist()))


def camembertToutesCategories(dfSondage: DataFrame, listeNomCategories: list[str]) -> None:
    _creerDossier(_NOM_DOSSIER_Q1b)
    
    listeNbAlimentsCategories: list[int] = [
        dfSondage[getNomColonneCompteur(nomCategorie)].sum() for nomCategorie in listeNomCategories]

    listeNbAlimentsCategories, listeNomCategories = _supprimerCategoriesAbsentes(listeNbAlimentsCategories, listeNomCategories)

    figure(figsize=(20, 10))

    title("")

    pie(listeNbAlimentsCategories, labels=listeNomCategories,
        normalize=True, autopct=lambda x: str(round(x, 2)) + '%')
    
    legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    tight_layout()

    savefig(f"{_NOM_DOSSIER_Q1b}{_NOM_FICHIER_Q1b}")
    _alerteGeneration(_NOM_FICHIER_Q1b)


def _estCategorie(dfAliment: DataFrame, numAliment: int, nomCategorie: str) -> bool:
    return dfAliment[_NOM_COLONNE_CATEGORIE_ALIMENT].iloc[_getNumLigneProduct(dfAliment, numAliment)] == nomCategorie


def _supprimerCategoriesAbsentes(listeQuantite: list[int], listeNom: list[str]) -> tuple[list[int], list[str]]:
    i = len(listeQuantite)-1

    while i >= 0:
        if listeQuantite[i] == 0:
            del listeQuantite[i]
            del listeNom[i]
        i -= 1
    
    return listeQuantite, listeNom


def truc(dfSondage: DataFrame, dfAliments: DataFrame, nomCategorie: str) -> list[int]:
    listeNbTypeAlimentCategorie: list[int] = []
    
    for idxSonde in range(len(dfSondage.values)):
        nbAlimentCategorie = 0
    
        for numAliment in _getListeAliments(dfSondage, idxSonde):
            nbAlimentCategorie += _estCategorie(dfAliments, numAliment, nomCategorie)
    
        listeNbTypeAlimentCategorie.append(nbAlimentCategorie)
    
    return listeNbTypeAlimentCategorie


def _score(quantite: float, listeScore: list[float]) -> int:
    for nbPoints in range(len(listeScore)):
        if quantite < listeScore[nbPoints]:
            return nbPoints
    return len(listeScore)


def _scoreSucre(quantiteSucre: float) -> int:
    return -_score(quantiteSucre, _PENALITE_QUANTITE_SUCRE)


def _scoreSel(quantiteSel: float) -> int:
    return -_score(quantiteSel, _PENALITE_QUANTITE_SEL)


def _scoreFibre(quantiteFibre: float) -> int:
    return _score(quantiteFibre, _BONUS_QUANTITE_FIBRE)


def _scoreProteineViande(quantiteProteines: float) -> int:
    return _score(quantiteProteines, _BONUS_QUANTITE_PROTEINES_VIANDE)


def _scoreProteineNonViande(quantiteProteines: float) -> int:
    return _score(quantiteProteines, _BONUS_QUANTITE_PROTEINES_NON_VIANDE)


def calculNutriScoreAlimentaire(dfAliments: DataFrame, idProduit: int) -> int:
    nutriScore = 0

    quantiteSucre: float        = dfAliments[_NOM_COLONNE_SUCRE].iloc[_getNumLigneProduct(dfAliments, idProduit)]
    quantiteSel: float          = dfAliments[_NOM_COLONNE_SEL].iloc[_getNumLigneProduct(dfAliments, idProduit)]
    quantiteFibre: float        = dfAliments[_NOM_COLONNE_FIBRES].iloc[_getNumLigneProduct(dfAliments, idProduit)]
    quantiteProteines: float    = dfAliments[_NOM_COLONNE_PROTEINES].iloc[_getNumLigneProduct(dfAliments, idProduit)]

    nutriScore += _scoreSucre(quantiteSucre)
    nutriScore += _scoreSel(quantiteSel)
    nutriScore += _scoreFibre(quantiteFibre)

    return nutriScore