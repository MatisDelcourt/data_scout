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


df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/jaeckel.csv', header=0)

## Filtering for players with more than 10 npxG+xA, 1000 mins and 1 goal
df_filter = (df['Minutes jouées'] >= 2000)
player_filter = df[df_filter]

players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jouées']
players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']
players_final['DefWons'] = player_filter['Duels défensifs gagnés. %']
players_final['DefDuel'] = player_filter['Duels défensifs par 90']
players_final['AerDuel'] = player_filter['Duels aériens par 90']
players_final['TklPAdj'] = player_filter['Tacles glissés PAdj']
players_final['IntPAdj'] = player_filter['Interceptions PAdj']
players_final['Tkl+Int'] = players_final['TklPAdj'] + players_final['IntPAdj']
players_final['AerWons'] = player_filter['Duels aériens gagnés. %']
# players_final['Blk'] = player_filter['Tirs bloqués par 90']
players_final['Pass'] = player_filter['Passes par 90']
players_final['AccPasses'] = player_filter['Passes précises. %']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']
players_final['Lg'] = player_filter['Passes longues par 90']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Forward'] = player_filter['Passes avant par 90']
players_final['Lateral'] = player_filter['Passes latérales par 90']
players_final['KP'] = player_filter['Passes quasi décisives par 90']
players_final['Smart'] = player_filter['Passes judicieuses par 90']
players_final['ShAst'] = player_filter['Passes décisives avec tir par 90']
players_final['Run'] = player_filter['Courses progressives par 90']
players_final['Recept'] = player_filter['Passes réceptionnées par 90']
players_final['PreAst'] = player_filter['Secondes passes décisives par 90'] + player_filter['Troisièmes passes décisives par 90']
players_final['TouchBox'] = player_filter['Touches de balle dans la surface de réparation sur 90']
players_final['Acc'] = player_filter['Accélérations par 90']
players_final['Fouled'] = player_filter['Fautes subies par 90']
players_final['BoxPasses'] = player_filter['Passes vers la surface de réparation par 90']
players_final['xA'] = player_filter['xA par 90']
players_final['xG'] = player_filter['xG par 90']
players_final['Head'] = player_filter['Buts de la tête par 90']
players_final['SuccOff'] = player_filter['Attaques réussies par 90']
players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Cross'] = player_filter['Centres par 90']
players_final['npG'] = player_filter['Buts hors penalty par 90']
players_final['Ast'] = player_filter['Passes décisives par 90']
players_final['DS'] = player_filter['Buts hors penalty par 90'] + player_filter['Passes décisives par 90']
players_final['Shots'] = player_filter['Tirs par 90']
players_final['ShCad%'] = player_filter['Tirs à la cible. %']
players_final['Taux'] = player_filter['Taux de conversion but/tir']
# players_final['Min'] = player_filter['Minutes played']
# players_final['SuccDef'] = player_filter['Successful defensive actions per 90']
# players_final['DefDuels'] = player_filter['Defensive duels won. %']
# players_final['AerWon'] = player_filter['Aerial duels won. %']
# players_final['Tkl'] = player_filter['Sliding tackles per 90']
# players_final['Blk'] = player_filter['Shots blocked per 90']
# players_final['Int'] = player_filter['Interceptions per 90']
# players_final['Prog'] = player_filter['Progressive passes per 90']
# players_final['Through'] = player_filter['Through passes per 90']
# players_final['Lg'] = player_filter['Long passes per 90']
# players_final['Length'] = player_filter['Average long pass length. m']
# players_final['Third'] = player_filter['Passes to final third per 90']
# players_final['Passes'] = player_filter['Accurate passes. %']
# players_final['SuccOff'] = player_filter['Successful attacking actions per 90']
# players_final['xG'] = player_filter['xG per 90']
# players_final['Crosses'] = player_filter['Crosses per 90']
# players_final['Drib'] = player_filter['Dribbles per 90']
# players_final['TouchesBox'] = player_filter['Touches in box per 90']
# players_final['Run'] = player_filter['Progressive runs per 90']
# players_final['xA'] = player_filter['xA per 90']
# players_final['ShAst'] = player_filter['Shot assists per 90']
# players_final['KP'] = player_filter['Key passes per 90']
# players_final['PenPasses'] = player_filter['Passes to penalty area per 90']
# players_final['Shots'] = player_filter['Shots per 90']
# players_final['Gls'] = player_filter['Goals per 90']
# players_final['Ast'] = player_filter['Assists per 90']
# players_final['GoalConv'] = player_filter['Goal conversion. %']
# players_final['HeadGls'] = player_filter['Head goals per 90']
# players_final['OffDuels'] = player_filter['Offensive duels per 90']
# players_final['OffWon'] = player_filter['Offensive duels won. %']
# players_final['Acc'] = player_filter['Accelerations per 90']
# players_final['Diff'] = player_filter['Diff per 90']


# METTRE LE NOM DU JOUEUR ANALYSE
player = players_final[players_final['Player'] == 'P. Jaeckel']
# player_name = player['Player'].split()[1]
name = list(player['Player'])
player_name = name[0].split()[1]

# METTRE LE NOM DES 12 STATS A AFFICHER
stat1 = 'SuccDef'
stat2 = 'DefDuel'
stat3 = 'DefWons'
stat4 = 'AerDuel'
stat5 = 'AerWons'
stat6 = 'IntPAdj'
stat7 = 'TklPAdj'
stat8 = 'PreAst'
stat9 = 'Prog'
stat10 = 'Third'
stat11 = 'Through'
stat12 = 'Lg'

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

f, axes = plt.subplots(3, 4, figsize=(30, 10))

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
ax1.axvline(x1, 0, .95, lw=2.5, color=col)
## Percentile lines
carac_name = carac_abbreviation_to_real_name(stat1)
ax1.set_title("%s : %.1f\n%i percentile" % (carac_name, x1, pct1))
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
    col = "red"
# The plot & player line
ax2 = sns.kdeplot(players_final[stat2], color=col, fill=col, ax=axes[0, 1])
ax2.axvline(x2, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat2)
ax2.set_title("%s : %.1f\n%i percentile" % (carac_name, x2, pct2))
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
    col = "red"
# The plot & player line
ax3 = sns.kdeplot(players_final[stat3], color=col, fill=col, ax=axes[0, 2])
ax3.axvline(x3, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat3)
ax3.set_title("%s : %.1f\n%i percentile" % (carac_name, x3, pct3))
# Clean graph
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
ax4.axvline(x4, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat4)
ax4.set_title("%s : %.1f\n%i percentile" % (carac_name, x4, pct4))
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
ax5.axvline(x5, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat5)
ax5.set_title("%s : %.1f\n%i percentile" % (carac_name, x5, pct5))
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
ax6.axvline(x6, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat6)
ax6.set_title("%s : %.1f\n%i percentile" % (carac_name, x6, pct6))
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
ax7.axvline(x7, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat7)
ax7.set_title("%s : %.1f\n%i percentile" % (carac_name, x7, pct7))
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
ax8.axvline(x8, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat8)
ax8.set_title("%s : %.1f\n%i percentile" % (carac_name, x8, pct8))
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
ax9.axvline(x9, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat9)
ax9.set_title("%s : %.1f\n%i percentile" % (carac_name, x9, pct9))
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
ax10.axvline(x10, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat10)
ax10.set_title("%s : %.1f\n%i percentile" % (carac_name, x10, pct10))
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
ax11.axvline(x11, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat11)
ax11.set_title("%s : %.1f\n%i percentile" % (carac_name, x11, pct11))
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
ax12.axvline(x12, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat12)
ax12.set_title("%s : %.1f\n%i percentile" % (carac_name, x12, pct12))
# Clean graph
ax12.set(xlabel=None)
ax12.set(ylabel=None)
ax12.set(yticks=[])

# Finish the graphs
sns.despine(left=True)
plt.subplots_adjust(hspace=1)
plt.suptitle(
    'Paul Jaeckel (24 ans, Union Berlin, 21-22) - Vs Défenseurs Centraux du top 5 européen \n '
    '2000+ minutes | Data issue de WyScout | Data\'Scout @datascoutsorare | Inspiré par @BeGriffis',
    fontsize=16,
    color="#eb1923", fontweight="bold", fontname="DejaVu Sans")
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
image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\jaeckel.png")
ax_image = add_image(
    image, fig, left=-0.01, bottom=0.825, width=0.15, height=0.15
)

fig.set_size_inches(20, 10)  # length, height

fig.savefig("Graph_%s.png" % (player_name), dpi=220)
fig = plt.gcf()
fig.set_size_inches(20, 10)  # length, height
fig