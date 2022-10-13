import pandas as pd

FILE_NAME = "Aliments.xlsx"
COLUMN_NAME_ALIMENTS = 'alim_nom_fr'


dfAliments = pd.read_excel(FILE_NAME)

dfAliments['estBio'] = ['bio' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index]
dfAliments['estVegan'] = ['vegan' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index]
dfAliments['estCasher'] = ['casher' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index]
dfAliments['estHalal'] = ['halal' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index]

#Facultatif, sert au debug
print(sum(['bio' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index])) #51 trouvés
print(sum(['vegan' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index])) #13 trouvés
print(sum(['casher' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index])) #0
print(sum(['halal' in dfAliments[COLUMN_NAME_ALIMENTS][i] for i in dfAliments.index]))  #0

#Facultatif, sert au debug
dfAliments.to_excel('Aliment-modif.xlsx', index=False)


