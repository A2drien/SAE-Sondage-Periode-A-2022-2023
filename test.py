import unittest
import pandas as pd
import utils_project as up


class PythonTest(unittest.TestCase):
    def CategorieTest(self):
        dfAliments = pd.read_excel(up.FICHIER_ALIMENTS)
        dfSondage = pd.read_excel(up.FICHIER_SONDAGE)

        up.attribuerNutriScoreAliments(dfAliments)

        for nomPreference in up.PREFERENCES_ALIMENTAIRES.keys():
            dfAliments[nomPreference] = up.correspondanceAlimentaire(
                dfAliments, nomPreference)

            dfSondage[up.getNomColonneCompteur(nomPreference)] = up.getNbTypeAlimentsCategorieGlobal(
                dfSondage, dfAliments, nomPreference)

        # Tests Bio
        self.assertTrue(up.estEtat(dfAliments, 25957, "Bio"))
        self.assertTrue(up.estEtat(dfAliments, 38402, "Bio"))
        self.assertFalse(up.estEtat(dfAliments, 76081, "Bio"))

        #Tests Végan
        self.assertTrue(up.estEtat(dfAliments, 25229, "Vegan"))
        self.assertTrue(up.estEtat(dfAliments, 25593, "Vegan"))
        self.assertFalse(up.estEtat(dfAliments, 25594, "Vegan"))

        #Tests Casher
        self.assertTrue(up.estEtat(dfAliments, 21508, "Casher"))
        self.assertTrue(up.estEtat(dfAliments, 36203, "Casher"))
        self.assertFalse(up.estEtat(dfAliments, 9082, "Casher"))

        #Tests Halal
        self.assertTrue(up.estEtat(dfAliments, 6101, "Halal"))
        self.assertTrue(up.estEtat(dfAliments, 6310, "Halal"))
        self.assertFalse(up.estEtat(dfAliments, 20906, "Halal"))

    
    def NutriScore(self):
        dfAliments = pd.read_excel(up.FICHIER_ALIMENTS)
        dfSondage = pd.read_excel(up.FICHIER_SONDAGE)

        #Calcul du nutriscore
        dfSondage[up.NOM_COLONNE_NUTRISCORE] = up.nutriScorePersonnes(
            dfSondage, dfAliments)
        
        self.assertEquals(up.)