import unittest
import pandas as pd
import utils_project as up


class PythonTest(unittest.TestCase):
    def CategorieTest(self):
        dfAliments = pd.read_excel(up.FICHIER_ALIMENTS)
        dfSondage = pd.read_excel(up.FICHIER_SONDAGE)

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
        
        """
            -0 car < 3.4g de sucre
            -5 car = 1g de sel
            +1 car > 0.7g de fibre
            +3 car > 8.06g de protéines (produit non viande)
            => -1
        """
        #Incohérant, -5, dont -1 avec le bonus viande (au lieu du +3)
        self.assertEquals(up.calculNutriScoreAlimentaire(dfAliments, 4041), -2)