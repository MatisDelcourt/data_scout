import matplotlib.pyplot as plt
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean
from math import pi
import os
from pathlib import Path

######################################################"
# 1. Récupérer les données grâce à WyScout en csv
# 2. Remplacer les "," par des "." puis remplacer les ";" par des "," (bloc-notes)
# 3. Récupérer une image du joueur en question et la crop sur paint en l'alignant sur le modèle png (cercle)
# 4. Choisir les stats à afficher sur le graph (12) (à automatiser en fonction du poste du joueur plus tard)
#    Si la stat est manquante dans le fichier carac_names_legend.csv, la rajouter ainsi que sa traduction
# 5. Lancer le script et le graph sera sauvegardé dans le dossier source

def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    with open('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/carac_names_legend.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val[:-1]
            #print(carac_dict[key])
    return carac_dict[carac]

##############################################################################

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))


df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/skhiri.csv', header=0)

## Filtering for players with more than 10 npxG+xA, 1000 mins and 1 goal
df_filter = (df['Minutes jouées'] >= 1900)
player_filter = df[df_filter]

players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jouées']
players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']
# players_final['DefDuels'] = player_filter['Defensive duels won. %']
# players_final['AerWon'] = player_filter['Aerial duels won. %']
players_final['Tkl'] = player_filter['Tacles glissés par 90']
players_final['Blk'] = player_filter['Tirs bloqués par 90']
players_final['Int'] = player_filter['Interceptions par 90']

players_final['Passes par 90'] = player_filter['Passes par 90']
players_final['Passes précises%'] = player_filter['Passes précises. %']
players_final['Passes avant par 90'] = player_filter['Passes avant par 90']
players_final['Passes en avant précises%'] = player_filter['Passes en avant précises. %']
players_final['Passes arrière par 90'] = player_filter['Passes arrière par 90']
players_final['Passes arrière précises%'] = player_filter['Passes arrière précises. %']
players_final['Passes latérales par 90'] = player_filter['Passes latérales par 90']
players_final['Passes latérales précises%'] = player_filter['Passes latérales précises. %']
players_final['Passes courtes / moyennes par 90'] = player_filter['Passes courtes / moyennes par 90']
players_final['Passes courtes / moyennes précises%'] = player_filter['Passes courtes / moyennes précises. %']
players_final['Passes longues par 90'] = player_filter['Passes longues par 90']
players_final['Longues passes précises%'] = player_filter['Longues passes précises. %']
players_final['Passes dans tiers adverse par 90'] = player_filter['Passes dans tiers adverse par 90']
players_final['Passes dans tiers adverse précises%'] = player_filter['Passes dans tiers adverse précises. %']
players_final['Passes vers la surface de réparation par 90'] = player_filter['Passes vers la surface de réparation par 90']
players_final['Passes vers la surface de réparation précises%'] = player_filter['Passes vers la surface de réparation précises. %']


# METTRE LE NOM DU JOUEUR ANALYSE
player = players_final[players_final['Player'] == 'E. Skhiri']
# player_name = player['Player'].split()[1]
name = list(player['Player'])
player_name = name[0].split()[1]

# METTRE LE NOM DES 12 STATS A AFFICHER
stat1 = 'SuccDef'
stat2 = 'Tkl'
stat3 = 'Blk'
stat4 = 'Int'

# Get the specific player's value (and name)
x1 = player[stat1].values[0]
x2 = player[stat2].values[0]
x3 = player[stat3].values[0]
x4 = player[stat4].values[0]

pct1 = stats.percentileofscore(players_final[stat1], x1)
pct2 = stats.percentileofscore(players_final[stat2], x2)
pct3 = stats.percentileofscore(players_final[stat3], x3)
pct4 = stats.percentileofscore(players_final[stat4], x4)

f, axes = plt.subplots(3, 1, figsize=(10, 100))

data_def = [pct1, pct2, pct3, pct4]
bars_def = ('SuccDef','Tkl','Blk','Int')
colors_def = []

for i in data_def:
    if i >= 90:
        col = "darkgreen"
    if 70 <= i < 90:
        col = "yellowgreen"
    if 50 <= i < 70:
        col = "gold"
    if 30 <= i < 50:
        col = "orange"
    if 0 <= i < 30:
        col = "red"
    colors_def.append(col)
y_pos = np.arange(len(bars_def))
# Create horizontal bars
plt.subplot(311)
defense = plt.barh(y_pos, data_def, color=colors_def)
# Create names on the x-axis
plt.yticks(y_pos, bars_def)

stat1 = 'Passes par 90'
stat2 = 'Passes précises%'
stat3 = 'Passes avant par 90'
stat4 = 'Passes en avant précises%'
stat5 = 'Passes arrière par 90'
stat6 = 'Passes arrière précises%'
stat7 = 'Passes latérales par 90'
stat8 = 'Passes latérales précises%'
stat9 = 'Passes courtes / moyennes par 90'
stat10 = 'Passes courtes / moyennes précises%'
stat11 = 'Passes longues par 90'
stat12 = 'Longues passes précises%'

# Get the specific player's value (and name)
x1 = player[stat1].values[0]
x2 = player[stat2].values[0]
x3 = player[stat3].values[0]
x4 = player[stat4].values[0]
x5 = player[stat5].values[0]
x6 = player[stat6].values[0]
x7 = player[stat7].values[0]
x8 = player[stat8].values[0]
x9 = player[stat9].values[0]
x10 = player[stat10].values[0]
x11 = player[stat11].values[0]
x12 = player[stat12].values[0]

pct1 = stats.percentileofscore(players_final[stat1], x1)
pct2 = stats.percentileofscore(players_final[stat2], x2)
pct3 = stats.percentileofscore(players_final[stat3], x3)
pct4 = stats.percentileofscore(players_final[stat4], x4)
pct5 = stats.percentileofscore(players_final[stat5], x5)
pct6 = stats.percentileofscore(players_final[stat6], x6)
pct7 = stats.percentileofscore(players_final[stat7], x7)
pct8 = stats.percentileofscore(players_final[stat8], x8)
pct9 = stats.percentileofscore(players_final[stat9], x9)
pct10 = stats.percentileofscore(players_final[stat10], x10)
pct11 = stats.percentileofscore(players_final[stat11], x11)
pct12 = stats.percentileofscore(players_final[stat12], x12)

#POSSESSION
data_pos = [pct1, pct2, pct3, pct4, pct5, pct6, pct7, pct8, pct9, pct10, pct11, pct12]
bars_pos = ('Passes par 90','Passes précises%','Passes avant par 90','Passes en avant précises%','Passes arrière par 90',
            'Passes arrière précises%','Passes latérales par 90','Passes latérales précises%','Passes courtes / moyennes par 90',
            'Passes courtes / moyennes précises%','Passes longues par 90','Longues passes précises%')
colors_pos = []

for i in data_pos:
    if i >= 90:
        col = "darkgreen"
    if 70 <= i < 90:
        col = "yellowgreen"
    if 50 <= i < 70:
        col = "gold"
    if 30 <= i < 50:
        col = "orange"
    if 0 <= i < 30:
        col = "red"
    colors_pos.append(col)
y_pos = np.arange(len(bars_pos))
plt.subplot(312)
# Create horizontal bars
poss = plt.barh(y_pos, data_pos, color=colors_pos)
# Create names on the x-axis
plt.yticks(y_pos, bars_pos)

plt.show()