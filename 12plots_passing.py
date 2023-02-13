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
    with open('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/carac_names_txt.txt', newline='', encoding="utf-8") as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val[:-1]
            #print(carac_dict[key])
    return carac_dict[carac]

##############################################################################

# font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
#                            "Roboto-Regular.ttf?raw=true"))
# font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
#                            "Roboto-Italic.ttf?raw=true"))
# font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
#                          "Roboto-Medium.ttf?raw=true"))


# df = pd.read_csv('/home/abennetot/Dataviz_Sorare/data/mid_top6.csv', header=0)
df = pd.read_csv('mid_top5.csv')
print(df)

french = True
if french:
    df["Player"] = df["Joueur"]
    # df["Squad"] = df["Équipe"]
    df["Min"] = df["Minutes jouées  "]
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
df_filter = (df['Min'] >= 700)
player_filter = df[df_filter]
print(player_filter)
players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Player']
players_final['Min'] = player_filter['Min']

###Template jeu de passes
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
player = players_final[players_final['Player'] == 'P. Højbjerg']
print(player)
# player_name = player['Player'].split()[1]
name = list(player['Player'])

try:
    player_name = name[0].split()[1]
except:
    player_name = name[0].split()[0]

# METTRE LE NOM DES 16 STATS A AFFICHER
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
stat13 = 'Passes dans tiers adverse par 90'
stat14 = 'Passes dans tiers adverse précises%'
stat15 = 'Passes vers la surface de réparation par 90'
stat16 = 'Passes vers la surface de réparation précises%'

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
x13 = player[stat13].values[0]
x14 = player[stat14].values[0]
x15 = player[stat15].values[0]
x16 = player[stat16].values[0]

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
pct13 = stats.percentileofscore(players_final[stat13], x13)
pct14 = stats.percentileofscore(players_final[stat14], x14)
pct15 = stats.percentileofscore(players_final[stat15], x15)
pct16 = stats.percentileofscore(players_final[stat16], x16)

f, axes = plt.subplots(4, 4, figsize=(40, 10))

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
ax1.set_title("%s : %.2f\n%i centile" % (carac_name, x1, pct1))
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
ax2.set_title("%s : %.2f\n%i centile" % (carac_name, x2, pct2))
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
ax3.set_title("%s : %.2f\n%i centile" % (carac_name, x3, pct3))
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
ax4.set_title("%s : %.2f\n%i centile" % (carac_name, x4, pct4))
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
ax5.set_title("%s : %.2f\n%i centile" % (carac_name, x5, pct5))
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
ax6.set_title("%s : %.2f\n%i centile" % (carac_name, x6, pct6))
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
ax7.set_title("%s : %.2f\n%i centile" % (carac_name, x7, pct7))
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
ax8.set_title("%s : %.2f\n%i centile" % (carac_name, x8, pct8))
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
ax9.set_title("%s : %.2f\n%i centile" % (carac_name, x9, pct9))
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
ax10.set_title("%s : %.2f\n%i centile" % (carac_name, x10, pct10))
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
ax11.set_title("%s : %.2f\n%i centile" % (carac_name, x11, pct11))
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
ax12.set_title("%s : %.2f\n%i centile" % (carac_name, x12, pct12))
# Clean graph
ax12.set(xlabel=None)
ax12.set(ylabel=None)
ax12.set(yticks=[])

###########
if pct13 >= 90:
    col = "darkgreen"
if 70 <= pct13 < 90:
    col = "yellowgreen"
if 50 <= pct13 < 70:
    col = "gold"
if 30 <= pct13 < 50:
    col = "orange"
if 0 <= pct13 < 30:
    col = "red"
# The plot & player line
ax13 = sns.kdeplot(players_final[stat13], color=col, fill=col, ax=axes[3, 0])
ax13.axvline(x13, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat13)
ax13.set_title("%s : %.2f\n%i centile" % (carac_name, x13, pct13))
# Clean graph
ax13.set(xlabel=None)
ax13.set(ylabel=None)
ax13.set(yticks=[])

if pct14 >= 90:
    col = "darkgreen"
if 70 <= pct14 < 90:
    col = "yellowgreen"
if 50 <= pct14 < 70:
    col = "gold"
if 30 <= pct14 < 50:
    col = "orange"
if 0 <= pct14 < 30:
    col = "red"
# The plot & player line
ax14 = sns.kdeplot(players_final[stat14], color=col, fill=col, ax=axes[3, 1])
ax14.axvline(x14, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat14)
ax14.set_title("%s : %.2f\n%i centile" % (carac_name, x14, pct14))
# Clean graph
ax14.set(xlabel=None)
ax14.set(ylabel=None)
ax14.set(yticks=[])

if pct15 >= 90:
    col = "darkgreen"
if 70 <= pct15 < 90:
    col = "yellowgreen"
if 50 <= pct15 < 70:
    col = "gold"
if 30 <= pct15 < 50:
    col = "orange"
if 0 <= pct15 < 30:
    col = "red"
# The plot & player line
ax15 = sns.kdeplot(players_final[stat15], color=col, fill=col, ax=axes[3, 2])
ax15.axvline(x15, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat15)
ax15.set_title("%s : %.2f\n%i centile" % (carac_name, x15, pct15))
# Clean graph
ax15.set(xlabel=None)
ax15.set(ylabel=None)
ax15.set(yticks=[])

if pct16 >= 90:
    col = "darkgreen"
if 70 <= pct16 < 90:
    col = "yellowgreen"
if 50 <= pct16 < 70:
    col = "gold"
if 30 <= pct16 < 50:
    col = "orange"
if 0 <= pct16 < 30:
    col = "red"
# The plot & player line
ax16 = sns.kdeplot(players_final[stat16], color=col, fill=col, ax=axes[3, 3])
ax16.axvline(x16, 0, .95, lw=2.5, color=col)
carac_name = carac_abbreviation_to_real_name(stat16)
ax16.set_title("%s : %.2f\n%i centile" % (carac_name, x16, pct16))
# Clean graph
ax16.set(xlabel=None)
ax16.set(ylabel=None)
ax16.set(yticks=[])

# Finish the graphs
sns.despine(left=True)
plt.subplots_adjust(hspace=1)
plt.suptitle(
    'Pierre-Emile Højbjerg (27 ans, Tottenham Hotspur) - Vs Milieux du Top 5 européen - 2022/2023 \n'
    '700+ minutes | Data issue de WyScout | Data\'Scout @datascout_ | Inspiré par @BeGriffis',
    fontsize=16,
    color="#132257", fontweight="bold", fontname="DejaVu Sans")
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
ax13.set_facecolor('#fbf9f4')
ax14.set_facecolor('#fbf9f4')
ax15.set_facecolor('#fbf9f4')
ax16.set_facecolor('#fbf9f4')

# METTRE LE NOM DU FICHIER IMAGE DU JOUEUR
image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\hojbjerg.png")
ax_image = add_image(
    image, fig, left=-0.01, bottom=0.825, width=0.15, height=0.15
)

# CREDIT_5 = "Ligues européennes de l'échantillon : Top 5 européen, Portugal, Pays-Bas & Autriche"
# fig.text(
#     0.01, 0.005, f"{CREDIT_5}", size=10,
#     fontproperties=font_italic.prop, color="#000000",
#     ha="left"
# )

fig.set_size_inches(20, 10)  # length, height

fig.savefig("Graph_%s.png" % (player_name), dpi=220)
fig = plt.gcf()
fig.set_size_inches(20, 10)  # length, height
fig