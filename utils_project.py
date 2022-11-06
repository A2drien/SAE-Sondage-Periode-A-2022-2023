from pandas import DataFrame, isna
from os import path, makedirs
from matplotlib.pyplot import pie, legend, savefig, figure, tight_layout, title

FICHIER_ALIMENTS: str = "Aliments.xlsx"
FICHIER_SONDAGE: str = "Sondage.xlsx"

_NB_ALIMENTS: int = 10

_NOM_COLONNE_ALIMENT: str = 'alim_nom_fr'
_NOM_COLONNE_CATEGORIE_ALIMENT: str = "alim_grp_nom_fr"
_NOM_COLONNE_SPECIFICATION_ALIMENTS: str = 'alim_ssssgrp_nom_fr'
_NOM_COLONNE_NUM_PRODUIT: str = 'alim_code'
NOM_COLONNE_NUTRISCORE = "NutriScore"

_NOM_COLONNE_SUCRE: str = 'Sucres (g/100 g)'
_NOM_COLONNE_SEL: str = 'Sel chlorure de sodium (g/100 g)'
_NOM_COLONNE_FIBRES: str = 'Fibres alimentaires (g/100 g)'
_NOM_COLONNE_PROTEINES: str = 'Protéines, N x facteur de Jones (g/100 g)'

_DONNEES_SONDE: list[str] = ['Administré.e', "Nom", "Prénom"]

_NOM_CATEGORIE_VIANDE: str = 'viandes, œufs, poissons et assimilés'


_PENALITE_QUANTITE_SUCRE: list[float] = [
    3.4, 6.8, 10, 14, 17, 20, 24, 27, 31, 34, 37, 41, 44, 48, 51]
_PENALITE_QUANTITE_SEL: list[float] = [0.2, 0.4, 0.6, 0.8, 1, 1.2,
                                       1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 3.6, 3.8, 4]
_BONUS_QUANTITE_FIBRE: list[float] = [0.7, 1.4, 2.2, 2.9, 3.6, 4.3, 5, 5.8]
_BONUS_QUANTITE_PROTEINES_NON_VIANDE: list[float] = [
    2.4, 4.8, 7.2, 9.6, 12, 14, 17]
_BONUS_QUANTITE_PROTEINES_VIANDE: list[float] = [2.4, 4.8]


_NOM_DOSSIER_Q1a: str = 'Question-1a/'
_NOM_DOSSIER_Q1b: str = 'Question-1b/'
_NOM_FICHIER_Q1b: str = "Camembert-catg-alim.png"
_NOM_DOSSIER_Q2: str = "Question-2"

"""Structure composé de :
    - La Catégorie
        - Le lieu (la colonne) où chercher la vérification de l'appartenance
            à cette catégorie
        - Une whiteliste qui valide l'appartenance à la catégorie
        - Une blackliste qui supprime les termes avant les tests d'appartenances
            à la catégorie 
"""
PREFERENCES_ALIMENTAIRES: dict[str, tuple[str, list[str], list[str]]] = {
    "Bio":      (
        _NOM_COLONNE_ALIMENT,
        ['bio'],
        ['biovive']
    ),

    "Vegan":    (
        _NOM_COLONNE_ALIMENT,
        ['vegan', 'végan'],
        ['ne convient pas aux véganes', 'ne convient pas aux veganes']
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


def getNomColonneCompteur(nomCategorie: str) -> str:
    """Retourne le nom de colonne de la catégorie en paramètre

    Args:
        nomCategorie (str): Nom de la catégorie

    Returns:
        str: Nom de colonne de la catégorie
    """
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


# Méthode mise en public afin de faciliter les tests
def estEtat(dfAliments: DataFrame, idProduit: int, nomColonne: str) -> bool:
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
        numAliment = dfSondage[f'Aliment{idxAliment}'].iloc[idxSonde]
        # Si l'aliment est bien renseigné, le rajouter
        if not isna(numAliment):
            listeAliments.append(
                dfSondage[f'Aliment{idxAliment}'].iloc[idxSonde])

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
        nbOccurrence += estEtat(dfAliments, idProduit, colonneTypeAliment)
    return nbOccurrence


def _supprimerExceptions(string: str, exceptions: list[str]) -> str:
    """Supprime dans le titre les mots blacklistés

    Args:
        string (str): Titre à éventuellement modifier
        exceptions (list[str]): Liste des mots blacklistés

    Returns:
        str: Titre corrigé
    """
    exceptions.sort(key=len, reverse=True)
    for exception in exceptions:
        string = string.replace(exception, '')
    return string


def correspondanceAlimentaire(dfAliments: DataFrame, nomPreference: str) -> list[bool]:
    """Retourne la liste booléenne correspondante à l'appartenance ou non à 
    la préférence donnée en paramètre pour chaque aliment

    Args:
        dfAliments (DataFrame): DataFrame des aliments
        nomPreference (str): Nom de la préférence à tester

    Returns:
        list[bool]: Liste de booléen sur l'appartenance ou non à la préférence
        pour chaque aliment
    """
    nomColonne, correspondances, exceptions = PREFERENCES_ALIMENTAIRES[nomPreference]

    L: list[bool] = []
    for label in dfAliments[nomColonne]:
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


def listePreferenceAlimentaire(dfSondage: DataFrame, nomCategorie: str) -> None:
    """Crée un fichier Excel du nombre d'aliment d'une catégorie consommé par chaque
    personne

    Args:
        dfSondage (DataFrame): DataFrame des sondés
        nomCategorie (str): Nom de la catégorie consommée
    """
    _creerDossier(_NOM_DOSSIER_Q1a)

    # Trie les valeur par ordre décroissant
    dfSondage = dfSondage.sort_values(
        by=[getNomColonneCompteur(nomCategorie)], ascending=False)

    dfSondage.to_excel(f"{_NOM_DOSSIER_Q1a}Pref-{nomCategorie}.xlsx",
                       index=False, columns=_DONNEES_SONDE + [getNomColonneCompteur(nomCategorie)])


def getCategoriesAlimentaires(dfAliments: DataFrame) -> list[str]:
    """
    Args:
        dfAliments (DataFrame): DataFrame des aliments

    Returns:
        list[str]: Liste de toutes les catégories alimentaires
    """
    return list(set(dfAliments[_NOM_COLONNE_CATEGORIE_ALIMENT].tolist()))


def camembertToutesCategories(dfSondage: DataFrame, listeNomCategories: list[str]) -> None:
    """Génère un camembert sur la moyenne du nombre d'aliments choisis par catégorie

    Args:
        dfSondage (DataFrame): DataFrame des sondés
        listeNomCategories (list[str]): Liste des catégories
    """
    _creerDossier(_NOM_DOSSIER_Q1b)

    listeNbAlimentsCategories: list[int] = [
        dfSondage[getNomColonneCompteur(nomCategorie)].sum() for nomCategorie in listeNomCategories]

    listeNbAlimentsCategories, listeNomCategories = _supprimerCategoriesAbsentes(
        listeNbAlimentsCategories, listeNomCategories)

    figure(figsize=(20, 10))

    title("Répartition des catégories d'aliments les plus choisies")

    pie(listeNbAlimentsCategories, labels=listeNomCategories,
        normalize=True, autopct=lambda x: str(round(x, 2)) + '%')

    legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    tight_layout()

    savefig(f"{_NOM_DOSSIER_Q1b}{_NOM_FICHIER_Q1b}")


def _estCategorie(dfAliments: DataFrame, numAliment: int, nomCategorie: str) -> bool:
    """Indique si tel aliment appartient à tel catégorie

    Args:
        dfAliments (DataFrame): DataFrame des aliments
        numAliment (int): Numéro de l'aliment
        nomCategorie (str): Nom de la catégorie

    Returns:
        bool: True s'il appartient à la catégorie en paramètre, False sinon
    """
    return dfAliments[_NOM_COLONNE_CATEGORIE_ALIMENT].iloc[_getNumLigneProduct(dfAliments, numAliment)] == nomCategorie


def _supprimerCategoriesAbsentes(listeQuantite: list[int], listeNom: list[str]) -> tuple[list[int], list[str]]:
    """Supprime les catégories d'aliments non choisies

    Args:
        listeQuantite (list[int]): Liste des quantités choisies par catégories
        listeNom (list[str]): Liste des noms de catégories

    Returns:
        tuple[list[int], list[str]]: Les 2 listes en paramètres modifiées
    """
    i = len(listeQuantite)-1

    while i >= 0:
        if listeQuantite[i] == 0:
            del listeQuantite[i]
            del listeNom[i]
        i -= 1

    return listeQuantite, listeNom


def getNbAlimentsCategorie(dfSondage: DataFrame, dfAliments: DataFrame, nomCategorie: str) -> list[int]:
    """Retourne, pour chaque sondé, le nombre d'aliments appartenant à la
    catégorie donnée en paramètre

    Args:
        dfSondage (DataFrame): DataFrame des sondés
        dfAliments (DataFrame): DataFrame des aliments
        nomCategorie (str): Catégorie

    Returns:
        list[int]: Liste du nombre d'aliments pour la catégorie choisie
    """
    listeNbTypeAlimentCategorie: list[int] = []

    for idxSonde in range(len(dfSondage.values)):
        nbAlimentCategorie = 0

        for numAliment in _getListeAliments(dfSondage, idxSonde):
            nbAlimentCategorie += _estCategorie(dfAliments,
                                                numAliment, nomCategorie)

        listeNbTypeAlimentCategorie.append(nbAlimentCategorie)

    return listeNbTypeAlimentCategorie


def _score(quantite: float, listeScore: list[float]) -> int:
    """Factorisation du code du nutriscore

    Args:
        quantite (float): Quantié de l'élément
        listeScore (list[float]): Liste des paliers de points

    Returns:
        int: Score
    """
    for nbPoints in range(len(listeScore)):
        if quantite < listeScore[nbPoints]:
            return nbPoints
    return len(listeScore)


def _scoreSucre(quantiteSucre: float) -> int:
    """
    Args:
        quantiteSucre (float): Quantité de sucre de l'aliment (pour 100g)

    Returns:
        int: Nombre de points de pénalité
    """
    return -_score(quantiteSucre, _PENALITE_QUANTITE_SUCRE)


def _scoreSel(quantiteSel: float) -> int:
    """
    Args:
        quantiteSel (float): Quantité de sel de l'aliment (pour 100g)

    Returns:
        int: Nombre de points de pénalité
    """
    return -_score(quantiteSel, _PENALITE_QUANTITE_SEL)


def _scoreFibre(quantiteFibre: float) -> int:
    """
    Args:
        quantiteFibre (float): Quantité de fibre de l'aliment (pour 100g)

    Returns:
        int: Nombre de points bonus
    """
    return _score(quantiteFibre, _BONUS_QUANTITE_FIBRE)


def _scoreProteineViande(quantiteProteines: float) -> int:
    """
    Args:
        quantiteProteines (float): Quantité de protéines de la viande (pour 100g)

    Returns:
        int: Nombre de points bonus
    """
    return _score(quantiteProteines, _BONUS_QUANTITE_PROTEINES_VIANDE)


def _scoreProteineNonViande(quantiteProteines: float) -> int:
    """
    Args:
        quantiteProteines (float): Quantité de protéines de l'aliment non-viande (pour 100g)

    Returns:
        int: Nombre de points bonus
    """
    return _score(quantiteProteines, _BONUS_QUANTITE_PROTEINES_NON_VIANDE)


def _convertirQuantite(quantite: str) -> float:
    """Convertit la quantité donnée dans un format utilisable

    Args:
        quantite (str): Quantité donnée

    Returns:
        float: Quantité (format utilisable)
    """
    if type(quantite) == float:
        return float(quantite)

    if quantite in ['traces', '-']:
        return 0

    # Retrait des '<'
    quantite = quantite.replace('<', '')

    # Conversion des ',' en '.'
    quantite = quantite.replace(',', '.')

    return float(quantite)


def _calculNutriScoreAlimentaire(dfAliments: DataFrame, numProduit: int) -> int:
    """Calcul du nutriscore

    Args:
        dfAliments (DataFrame): DataFrame des aliments
        numProduit (int): numéro du produit

    Returns:
        int: Nutriscore du produit
    """
    nutriScore = 0

    infoAliment = dfAliments.loc[_getNumLigneProduct(dfAliments, numProduit)]

    quantiteSucre: float = _convertirQuantite(infoAliment[_NOM_COLONNE_SUCRE])
    quantiteSel: float = _convertirQuantite(infoAliment[_NOM_COLONNE_SEL])
    quantiteFibre: float = _convertirQuantite(infoAliment[_NOM_COLONNE_FIBRES])
    quantiteProteines: float = _convertirQuantite(
        infoAliment[_NOM_COLONNE_PROTEINES])

    nutriScore += _scoreSucre(quantiteSucre)
    nutriScore += _scoreSel(quantiteSel)
    nutriScore += _scoreFibre(quantiteFibre)

    if infoAliment[_NOM_COLONNE_CATEGORIE_ALIMENT] == _NOM_CATEGORIE_VIANDE:
        nutriScore += _scoreProteineViande(quantiteProteines)
    else:
        nutriScore += _scoreProteineNonViande(quantiteProteines)

    return nutriScore


def nutriScorePersonnes(dfSondage: DataFrame, dfAliments: DataFrame) -> list[float]:
    """Retourne le nutriscore de chaque personne

    Args:
        dfSondage (DataFrame): DataFrame des sondés
        dfAliments (DataFrame): DataFrame des aliments

    Returns:
        list[int]: Liste des nutriscores
    """
    listeNutriScore: list[float] = []

    for idxSonde in range(len(dfSondage.values)):
        listeAliments: list[int] = _getListeAliments(dfSondage, idxSonde)
        listeNutriScorePersonne: list[int] = [_calculNutriScoreAlimentaire(
            dfAliments, idProduit) for idProduit in listeAliments]
        scorePersonne = sum(listeNutriScorePersonne) / len(listeNutriScorePersonne)
        listeNutriScore.append(scorePersonne)

    return listeNutriScore


def sauvegardeNutriScore(dfSondage: DataFrame) -> None:
    """Sauvegarde les nutriscores des sondés dans un fichier

    Args:
        dfSondage (DataFrame): DataFrame des sondés
    """
    _creerDossier(_NOM_DOSSIER_Q2)

    # Trie les valeur par ordre décroissant
    dfSondage = dfSondage.sort_values(
        by=[NOM_COLONNE_NUTRISCORE], ascending=False)

    # Sauvegarde le fichier
    dfSondage.to_excel(f"{_NOM_DOSSIER_Q2}/Nutriscore.xlsx",
                       index=False, columns=_DONNEES_SONDE+[NOM_COLONNE_NUTRISCORE])
