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
# importing NumPy, Pandas, Math, Matplotlib, and Font Libraries
import numpy as np
import pandas as pd
import math
import matplotlib.image as image
from matplotlib import artist
import matplotlib.patches as mpatches
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib import rcParams
from matplotlib.patches import Arc
rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.sans-serif'] = ['Franklin Gothic Medium', 'Franklin Gothic Book']


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


df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Radar2/timbervssaliba.csv', header=0)
print(df)

french = True
if french:
    df["Player"] = df["Joueur"]
    df["Squad"] = df["Equipe"]
    df["Min"] = df["Minutes jouées"]
    df["Duels défensifs gagnés%"] = df["Duels défensifs gagnés. %"]
    df["Duels aériens gagnés%"] = df["Duels aériens gagnés. %"]
    df["Passes précises%"] = df["Passes précises. %"]
    df["Passes arrière précises%"] = df["Passes arrière précises. %"]
    df["Passes latérales précises%"] = df["Passes latérales précises. %"]
    df["Passes en avant précises%"] = df["Passes en avant précises. %"]
    df["Longues passes précises%"] = df["Longues passes précises. %"]
    df["Passes vers la surface de réparation précises%"] = df["Passes vers la surface de réparation précises. %"]
    df["Passes dans tiers adverse précises%"] = df["Passes dans tiers adverse précises. %"]
    df["Passes courtes / moyennes précises%"] = df["Passes courtes / moyennes précises. %"]


## Filtering for players with more than 10 npxG+xA, 1000 mins and 1 goal
df_filter = (df['Min'] >= 2000)
player_filter = df[df_filter]
print(player_filter)
players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Player']
players_final['Min'] = player_filter['Min']

###Template jeu de passes
#players_final['Passes par 90'] = player_filter['Passes par 90']
#players_final['Passes précises%'] = player_filter['Passes précises%']
#players_final['Passes avant par 90'] = player_filter['Passes avant par 90']
#players_final['Passes en avant précises%'] = player_filter['Passes en avant précises%']
#players_final['Passes arrière par 90'] = player_filter['Passes arrière par 90']
#players_final['Passes arrière précises%'] = player_filter['Passes arrière précises%']
#players_final['Passes latérales par 90'] = player_filter['Passes latérales par 90']
#players_final['Passes latérales précises%'] = player_filter['Passes latérales précises%']
#players_final['Passes courtes / moyennes par 90'] = player_filter['Passes courtes / moyennes par 90']
#players_final['Passes courtes / moyennes précises%'] = player_filter['Passes courtes / moyennes précises%']
#players_final['Passes longues par 90'] = player_filter['Passes longues par 90']
#players_final['Longues passes précises%'] = player_filter['Longues passes précises%']
#players_final['Passes dans tiers adverse par 90'] = player_filter['Passes dans tiers adverse par 90']
#players_final['Passes dans tiers adverse précises%'] = player_filter['Passes dans tiers adverse précises%']
#players_final['Passes vers la surface de réparation par 90'] = player_filter['Passes vers la surface de réparation par 90']
#players_final['Passes vers la surface de réparation précises%'] = player_filter['Passes vers la surface de réparation précises%']

###Template jeu de passes offensif
players_final['Passes par 90'] = player_filter['Passes par 90']
players_final['Passes avant par 90'] = player_filter['Passes avant par 90']
players_final['Passes longues par 90'] = player_filter['Passes longues par 90']
players_final['Longueur moyenne des passes longues'] = player_filter['Longueur moyenne des passes longues. m']
# players_final['Passes décisives avec tir par 90'] = player_filter['Passes décisives avec tir par 90']
# players_final['Secondes passes décisives par 90'] = player_filter['Secondes passes décisives par 90']
# players_final['Troisièmes passes décisives par 90'] = player_filter['Troisièmes passes décisives par 90']
# players_final['Passes judicieuses par 90'] = player_filter['Passes judicieuses par 90']
players_final['Passes dans tiers adverse par 90'] = player_filter['Passes dans tiers adverse par 90']
players_final['Passes vers la surface de réparation par 90'] = player_filter['Passes vers la surface de réparation par 90']
players_final['Passes pénétrantes par 90'] = player_filter['Passes pénétrantes par 90']
players_final['Passes progressives par 90'] = player_filter['Passes progressives par 90']

players_final['Passes par 90'] = player_filter['Passes par 90']
players_final['Passes précises%'] = player_filter['Passes précises%']
players_final['Passes avant par 90'] = player_filter['Passes avant par 90']
players_final['Passes en avant précises%'] = player_filter['Passes en avant précises%']
players_final['Passes arrière par 90'] = player_filter['Passes arrière par 90']
players_final['Passes arrière précises%'] = player_filter['Passes arrière précises%']
players_final['Passes latérales par 90'] = player_filter['Passes latérales par 90']
players_final['Passes latérales précises%'] = player_filter['Passes latérales précises%']
players_final['Passes courtes / moyennes par 90'] = player_filter['Passes courtes / moyennes par 90']
players_final['Passes courtes / moyennes précises%'] = player_filter['Passes courtes / moyennes précises%']
players_final['Passes longues par 90'] = player_filter['Passes longues par 90']
players_final['Longues passes précises%'] = player_filter['Longues passes précises%']
players_final['Passes dans tiers adverse par 90'] = player_filter['Passes dans tiers adverse par 90']
players_final['Passes dans tiers adverse précises%'] = player_filter['Passes dans tiers adverse précises%']
players_final['Passes vers la surface de réparation par 90'] = player_filter['Passes vers la surface de réparation par 90']
players_final['Passes vers la surface de réparation précises%'] = player_filter['Passes vers la surface de réparation précises%']


# METTRE LE NOM DU JOUEUR ANALYSE
player1 = players_final[players_final['Player'] == 'W. Saliba']
print(player1)
# player_name = player['Player'].split()[1]
name1 = list(player1['Player'])
player_name1 = name1[0].split()[1]
player2 = players_final[players_final['Player'] == 'J. Timber']
print(player2)
# player_name = player['Player'].split()[1]
name2 = list(player2['Player'])
player_name2 = name2[0].split()[1]

# METTRE LE NOM DES 12 STATS A AFFICHER

stat1 = 'Passes par 90'
stat2 = 'Passes précises%'
stat3 = 'Passes avant par 90'
stat4 = 'Passes en avant précises%'
stat5 = 'Passes latérales par 90'
stat6 = 'Passes latérales précises%'
stat7 = 'Passes dans tiers adverse par 90'
stat8 = 'Passes dans tiers adverse précises%'
stat9 = 'Passes courtes / moyennes par 90'
stat10 = 'Passes courtes / moyennes précises%'
stat11 = 'Passes longues par 90'
stat12 = 'Longues passes précises%'


# Get the specific player's value (and name)
xp1_1 = player1[stat1].values[0]
xp1_2 = player1[stat2].values[0]
xp1_3 = player1[stat3].values[0]
xp1_4 = player1[stat4].values[0]
xp1_5 = player1[stat5].values[0]
xp1_6 = player1[stat6].values[0]
xp1_7 = player1[stat7].values[0]
xp1_8 = player1[stat8].values[0]
xp1_9 = player1[stat9].values[0]
xp1_10 = player1[stat10].values[0]
xp1_11 = player1[stat11].values[0]
xp1_12 = player1[stat12].values[0]

xp2_1 = player2[stat1].values[0]
xp2_2 = player2[stat2].values[0]
xp2_3 = player2[stat3].values[0]
xp2_4 = player2[stat4].values[0]
xp2_5 = player2[stat5].values[0]
xp2_6 = player2[stat6].values[0]
xp2_7 = player2[stat7].values[0]
xp2_8 = player2[stat8].values[0]
xp2_9 = player2[stat9].values[0]
xp2_10 = player2[stat10].values[0]
xp2_11 = player2[stat11].values[0]
xp2_12 = player2[stat12].values[0]

pct1 = stats.percentileofscore(players_final[stat1], xp1_1)
pct2 = stats.percentileofscore(players_final[stat2], xp1_2)
pct3 = stats.percentileofscore(players_final[stat3], xp1_3)
pct4 = stats.percentileofscore(players_final[stat4], xp1_4)
pct5 = stats.percentileofscore(players_final[stat5], xp1_5)
pct6 = stats.percentileofscore(players_final[stat6], xp1_6)
pct7 = stats.percentileofscore(players_final[stat7], xp1_7)
pct8 = stats.percentileofscore(players_final[stat8], xp1_8)
pct9 = stats.percentileofscore(players_final[stat9], xp1_9)
pct10 = stats.percentileofscore(players_final[stat10], xp1_10)
pct11 = stats.percentileofscore(players_final[stat11], xp1_11)
pct12 = stats.percentileofscore(players_final[stat12], xp1_12)

Vpct1 = stats.percentileofscore(players_final[stat1], xp2_1)
Vpct2 = stats.percentileofscore(players_final[stat2], xp2_2)
Vpct3 = stats.percentileofscore(players_final[stat3], xp2_3)
Vpct4 = stats.percentileofscore(players_final[stat4], xp2_4)
Vpct5 = stats.percentileofscore(players_final[stat5], xp2_5)
Vpct6 = stats.percentileofscore(players_final[stat6], xp2_6)
Vpct7 = stats.percentileofscore(players_final[stat7], xp2_7)
Vpct8 = stats.percentileofscore(players_final[stat8], xp2_8)
Vpct9 = stats.percentileofscore(players_final[stat9], xp2_9)
Vpct10 = stats.percentileofscore(players_final[stat10], xp2_10)
Vpct11 = stats.percentileofscore(players_final[stat11], xp2_11)
Vpct12 = stats.percentileofscore(players_final[stat12], xp2_12)
circle_rad = 15  # This is the radius, in points
f, axes = plt.subplots(3, 4, figsize=(30, 15))

if pct1 >= 90:
    col = "darkgreen"
if 70 <= pct1 < 90:
    col = "yellowgreen"
if 50 <= pct1 < 70:
    col = "gold"
if 30 <= pct1 < 50:
    col = "orange"
if 0 <= pct1 < 30:
    col = "red"
# The plot & player line
ax1 = sns.kdeplot(players_final[stat1], color=col, fill=col, ax=axes[0, 0])
ax1.axvline(xp1_1, 0.25, .95, lw=2.5, color="blue")
ax1.axvline(xp2_1, 0.25, .95, lw=2.5, color="red")


ax1.plot(xp1_1, 0.0046, 'o',
        ms=circle_rad * 2, mec='b', mfc='none', mew=2)
ax1.plot(xp2_1, 0.0046, 'o',
        ms=circle_rad * 2, mec='r', mfc='none', mew=2)

ax1.annotate('S', xy=(xp1_1-2.8, 0.0023),
            color='b', size='xx-large', weight='bold')

ax1.annotate('T', xy=(xp2_1-3.5, 0.0023),
            color='r', size='xx-large', weight='bold')



## Percentile lines
carac_name = carac_abbreviation_to_real_name(stat1)
ax1.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_1, player_name1,
                                                               xp2_1, player_name2, pct1, Vpct1))
# Clean graph
ax1.set(xlabel=None)
ax1.set(ylabel=None)
ax1.set(yticks=[])

if pct2 >= 90:
    col = "darkgreen"
if 70 <= pct2 < 90:
    col = "yellowgreen"
if 50 <= pct2 < 70:
    col = "gold"
if 30 <= pct2 < 50:
    col = "orange"
if 0 <= pct2 < 30:
    col = "darkgreen"
# The plot & player line
ax2 = sns.kdeplot(players_final[stat2], color=col, fill=col, ax=axes[0, 1])
ax2.axvline(xp1_2, 0, .95, lw=2.5, color="blue")
ax2.axvline(xp2_2, 0, .95, lw=2.5, color="red")

print(stat2)
carac_name = carac_abbreviation_to_real_name(stat2)
ax2.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_2, player_name1,
                                                               xp2_2, player_name2, pct2, Vpct2))
# Clean graph
ax2.set(xlabel=None)
ax2.set(ylabel=None)
ax2.set(yticks=[])

if pct3 >= 90:
    col = "darkgreen"
if 70 <= pct3 < 90:
    col = "yellowgreen"
if 50 <= pct3 < 70:
    col = "gold"
if 30 <= pct3 < 50:
    col = "orange"
if 0 <= pct3 < 30:
    col = "darkgreen"
# The plot & player line
ax3 = sns.kdeplot(players_final[stat3], color=col, fill=col, ax=axes[0, 2])
ax3.axvline(xp1_3, 0, .95, lw=2.5, color="blue")
ax3.axvline(xp2_3, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat3)
ax3.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_3, player_name1,
                                                               xp2_3, player_name2, pct3, Vpct3))# Clean graph
ax3.set(xlabel=None)
ax3.set(ylabel=None)
ax3.set(yticks=[])

if pct4 >= 90:
    col = "darkgreen"
if 70 <= pct4 < 90:
    col = "yellowgreen"
if 50 <= pct4 < 70:
    col = "gold"
if 30 <= pct4 < 50:
    col = "orange"
if 0 <= pct4 < 30:
    col = "red"
# The plot & player line
ax4 = sns.kdeplot(players_final[stat4], color=col, fill=col, ax=axes[0, 3])
ax4.axvline(xp1_4, 0, .95, lw=2.5, color="blue")
ax4.axvline(xp2_4, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat4)
ax4.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_4, player_name1,
                                                               xp2_4, player_name2, pct4, Vpct4))
# Clean graph
ax4.set(xlabel=None)
ax4.set(ylabel=None)
ax4.set(yticks=[])

if pct5 >= 90:
    col = "darkgreen"
if 70 <= pct5 < 90:
    col = "yellowgreen"
if 50 <= pct5 < 70:
    col = "gold"
if 30 <= pct5 < 50:
    col = "orange"
if 0 <= pct5 < 30:
    col = "red"
# The plot & player line
ax5 = sns.kdeplot(players_final[stat5], color=col, fill=col, ax=axes[1, 0])
ax5.axvline(xp1_5, 0, .95, lw=2.5, color="blue")
ax5.axvline(xp2_5, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat5)
ax5.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_5, player_name1,
                                                               xp2_5, player_name2, pct5, Vpct5))
# Clean graph
ax5.set(xlabel=None)
ax5.set(ylabel=None)
ax5.set(yticks=[])

if pct6 >= 90:
    col = "darkgreen"
if 70 <= pct6 < 90:
    col = "yellowgreen"
if 50 <= pct6 < 70:
    col = "gold"
if 30 <= pct6 < 50:
    col = "orange"
if 0 <= pct6 < 30:
    col = "red"
# The plot & player line
ax6 = sns.kdeplot(players_final[stat6], color=col, fill=col, ax=axes[1, 1])
ax6.axvline(xp1_6, 0, .95, lw=2.5, color="blue")
ax6.axvline(xp2_6, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat6)
ax6.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_6, player_name1,
                                                               xp2_6, player_name2, pct6, Vpct6))
# Clean graph
ax6.set(xlabel=None)
ax6.set(ylabel=None)
ax6.set(yticks=[])

if pct7 >= 90:
    col = "darkgreen"
if 70 <= pct7 < 90:
    col = "yellowgreen"
if 50 <= pct7 < 70:
    col = "gold"
if 30 <= pct7 < 50:
    col = "orange"
if 0 <= pct7 < 30:
    col = "red"
# The plot & player line
ax7 = sns.kdeplot(players_final[stat7], color=col, fill=col, ax=axes[1, 2])
ax7.axvline(xp1_7, 0, .95, lw=2.5, color="blue")
ax7.axvline(xp2_7, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat7)
ax7.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_7, player_name1,
                                                               xp2_7, player_name2, pct7, Vpct7))
# Clean graph
ax7.set(xlabel=None)
ax7.set(ylabel=None)
ax7.set(yticks=[])

if pct8 >= 90:
    col = "darkgreen"
if 70 <= pct8 < 90:
    col = "yellowgreen"
if 50 <= pct8 < 70:
    col = "gold"
if 30 <= pct8 < 50:
    col = "orange"
if 0 <= pct8 < 30:
    col = "red"
# The plot & player line
ax8 = sns.kdeplot(players_final[stat8], color=col, fill=col, ax=axes[1, 3])
ax8.axvline(xp1_8, 0, .95, lw=2.5, color="blue")
ax8.axvline(xp2_8, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat8)
ax8.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_8, player_name1,
                                                               xp2_8, player_name2, pct8, Vpct8))
# Clean graph
ax8.set(xlabel=None)
ax8.set(ylabel=None)
ax8.set(yticks=[])

if pct9 >= 90:
    col = "darkgreen"
if 70 <= pct9 < 90:
    col = "yellowgreen"
if 50 <= pct9 < 70:
    col = "gold"
if 30 <= pct9 < 50:
    col = "orange"
if 0 <= pct9 < 30:
    col = "red"
# The plot & player line
ax9 = sns.kdeplot(players_final[stat9], color=col, fill=col, ax=axes[2, 0])
ax9.axvline(xp1_9, 0, .95, lw=2.5, color="blue")
ax9.axvline(xp2_9, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat9)
ax9.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_9, player_name1,
                                                               xp2_9, player_name2, pct9, Vpct9))
# Clean graph
ax9.set(xlabel=None)
ax9.set(ylabel=None)
ax9.set(yticks=[])

if pct10 >= 90:
    col = "darkgreen"
if 70 <= pct10 < 90:
    col = "yellowgreen"
if 50 <= pct10 < 70:
    col = "gold"
if 30 <= pct10 < 50:
    col = "orange"
if 0 <= pct10 < 30:
    col = "red"
# The plot & player line
ax10 = sns.kdeplot(players_final[stat10], color=col, fill=col, ax=axes[2, 1])
ax10.axvline(xp1_10, 0, .95, lw=2.5, color="blue")
ax10.axvline(xp2_10, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat10)
ax10.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_10, player_name1,
                                                               xp2_10, player_name2, pct10, Vpct10))
# Clean graph
ax10.set(xlabel=None)
ax10.set(ylabel=None)
ax10.set(yticks=[])

if pct11 >= 90:
    col = "darkgreen"
if 70 <= pct11 < 90:
    col = "yellowgreen"
if 50 <= pct11 < 70:
    col = "gold"
if 30 <= pct11 < 50:
    col = "orange"
if 0 <= pct11 < 30:
    col = "red"
# The plot & player line

ax11 = sns.kdeplot(players_final[stat11], color=col, fill=col, ax=axes[2, 2])
ax11.axvline(xp1_11, 0, .95, lw=2.5, color="blue")
ax11.axvline(xp2_11, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat11)
ax11.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_11, player_name1,
                                                               xp2_11, player_name2, pct11, Vpct11))
# Clean graph
ax11.set(xlabel=None)
ax11.set(ylabel=None)
ax11.set(yticks=[])

if pct12 >= 90:
    col = "darkgreen"
if 70 <= pct12 < 90:
    col = "yellowgreen"
if 50 <= pct12 < 70:
    col = "gold"
if 30 <= pct12 < 50:
    col = "orange"
if 0 <= pct12 < 30:
    col = "red"
# The plot & player line
ax12 = sns.kdeplot(players_final[stat12], color=col, fill=col, ax=axes[2, 3])
ax12.axvline(xp1_12, 0, .95, lw=2.5, color="blue")
ax12.axvline(xp2_12, 0, .95, lw=2.5, color="red")
carac_name = carac_abbreviation_to_real_name(stat12)
ax12.set_title("%s \n %.1f %s, %.1f %s\n%i et %i percentiles" % (carac_name, xp1_12, player_name1,
                                                               xp2_12, player_name2, pct12, Vpct12))
# Clean graph
ax12.set(xlabel=None)
ax12.set(ylabel=None)
ax12.set(yticks=[])



# Finish the graphs
sns.despine(left=True)
plt.subplots_adjust(hspace=1)

plt.suptitle("W. Saliba vs J. Timber vs Défenseurs Centraux des 5 grands championnats + Pays-Bas, \n2000+ minutes | Data issue de WyScout | Data\'Scout @datascoutsorare | Inspiré par @BeGriffis",
    fontsize=16,
    color="black", fontweight="bold", fontname="DejaVu Sans")


plt.style.use("default")

fig = plt.gcf()

fig.patch.set_facecolor('#fbf9f4')
ax1.set_facecolor('#fbf9f4')
ax2.set_facecolor('#fbf9f4')
ax3.set_facecolor('#fbf9f4')
ax4.set_facecolor('#fbf9f4')
ax5.set_facecolor('#fbf9f4')
ax6.set_facecolor('#fbf9f4')
ax7.set_facecolor('#fbf9f4')
ax8.set_facecolor('#fbf9f4')
ax9.set_facecolor('#fbf9f4')
ax10.set_facecolor('#fbf9f4')
ax11.set_facecolor('#fbf9f4')
ax12.set_facecolor('#fbf9f4')

# METTRE LE NOM DU FICHIER IMAGE DU JOUEUR
image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\saliba.png")
ax_image = add_image(
    image, fig, left=-0.01, bottom=0.825, width=0.15, height=0.15
)
image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\timber.png")
ax_image = add_image(
    image, fig, left=0.87, bottom=0.825, width=0.15, height=0.15
)

fig.set_size_inches(20, 12)  # length, height

fig.savefig("Graph_duo_%s.png" % (player_name1), dpi=220)
fig = plt.gcf()
fig.set_size_inches(20, 12)  # length, height
fig