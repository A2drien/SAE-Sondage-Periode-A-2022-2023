from pandas import DataFrame
from os import path, makedirs
from matplotlib.pyplot import pie, legend, savefig

FICHIER_ALIMENTS = "Aliments.xlsx"
FICHIER_SONDAGE = "Sondage.xlsx"

_NB_ALIMENTS = 10

_NOM_COLONNE_ALIMENT = 'alim_nom_fr'
_NOM_COLONNE_CATEGORIE_ALIMENT = ""
_NOM_COLONNE_SPECIFICATION_ALIMENTS = 'alim_ssssgrp_nom_fr'
_NOM_COLONNE_NUM_PRODUIT = 'alim_code'

_DONNEES_SONDE: list[str] = ['Administré.e', "Nom", "Prénom"]

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
    listeAliments = []

    for idxAliment in range(1, _NB_ALIMENTS+1):
        listeAliments.append(dfSondage[f'Aliment{idxAliment}'].iloc[idxSonde])

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
    listeNbTypeAlimentsCategorieGlobal = []

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
    print(f"Fichier '{nomFichier}' généré !")


def listePreferenceAlimentaire(dfSondage: DataFrame, nomCategorie: str) -> None:
    _creerDossier(_NOM_DOSSIER_Q1a)

    dfSondage.sort_values(by=[getNomColonneCompteur(nomCategorie)], ascending=False)

    nomFichier = f"Pref-{nomCategorie}.xlsx"
    dfSondage.to_excel(f"{_NOM_DOSSIER_Q1a}{nomFichier}",
                       index=False, columns=_DONNEES_SONDE + [getNomColonneCompteur(nomCategorie)])
    _alerteGeneration(nomFichier)


def getCategoriesAlimentaires(dfAliments: DataFrame) -> list[str]:
    return list(set(dfAliments[_NOM_COLONNE_CATEGORIE_ALIMENT].tolist()))


#!!!
def correspondanceCategorie(dfSondage: DataFrame, dfAliment: DataFrame, listeCategorieAlimentaire: list[str], nomCategorie: str) -> list[int]:
    pass


def camembertToutesCategories(dfSondage: DataFrame) -> None:
    _creerDossier(_NOM_DOSSIER_Q1b)

    listeNomCategories: list[str] = [
        nom for nom in PREFERENCES_ALIMENTAIRES.keys()]
    
    listeNbAlimentsCategories: list[int] = [
        dfSondage[getNomColonneCompteur(nomCategorie)].sum() for nomCategorie in PREFERENCES_ALIMENTAIRES.keys()]

    pie(listeNbAlimentsCategories, labels=listeNomCategories,
        normalize=True, autopct=lambda x: str(round(x, 2)) + '%')
    legend()

    savefig(f"{_NOM_DOSSIER_Q1b}{_NOM_FICHIER_Q1b}")
    _alerteGeneration(_NOM_FICHIER_Q1b)
