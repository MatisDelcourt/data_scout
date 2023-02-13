# importing NumPy, Pandas, Math, Matplotlib, and Font Libraries
from utils import rainbow_text
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

df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/Taylor2022.csv', header=0)


## Filtering for players with more than 10 npxG+xA, 1000 mins and 1 goal
df_filter = (df['Minutes jouées'] >= 350)
player_filter = df[df_filter]

# df_filter = (df['xG'] >= 8)
# player_filter = player_filter[df_filter]

## Creating DataFrame for defenders with necessary raw and processed columns from player_filter
players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Equipe'] = player_filter['Equipe']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Run'] = player_filter['Courses progressives par 90']

players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Acc'] = player_filter['Accélérations par 90']

players_final['BoxTouch'] = player_filter['Touches de balle dans la surface de réparation sur 90']
players_final['BoxPasses'] = player_filter['Passes vers la surface de réparation par 90']
players_final['Deep'] = player_filter['Réalisations en profondeur par 90']
players_final['BoxCross'] = player_filter['Centres dans la surface de but par 90']

players_final['Cross'] = player_filter['Centres par 90']
players_final['Cross%'] = player_filter['Сentres précises. %']

players_final['KP'] = player_filter['Passes quasi décisives par 90']

players_final['DefWons'] = player_filter['Duels défensifs gagnés. %']
players_final['AerWons'] = player_filter['Duels aériens gagnés. %']
players_final['Tkl'] = player_filter['Tacles glissés PAdj']
players_final['Int'] = player_filter['Interceptions PAdj']
players_final['Tkl+Int'] = player_filter['Tacles glissés PAdj'] + player_filter['Interceptions PAdj']

players_final['Def'] = player_filter['Duels défensifs par 90']
players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']

players_final['DS'] = player_filter['Buts par 90'] + player_filter['Passes décisives par 90']
players_final['xDS'] = player_filter['xG par 90'] + player_filter['xA par 90']
players_final['xG'] = player_filter['xG']
players_final['xA'] = player_filter['xA']
players_final['xG90'] = player_filter['xG par 90']
players_final['xA90'] = player_filter['xA par 90']

players_final['Shots'] = player_filter['Tirs par 90'] # + player_filter['Passes décisives par 90']
players_final['ShGls'] = player_filter['Taux de conversion but/tir']
players_final['ShAst'] = player_filter['Passes décisives avec tir par 90']

players_final['Smart'] = player_filter['Passes judicieuses par 90']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Forward'] = player_filter['Passes avant par 90']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']

players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Drib%'] = player_filter['Dribbles réussis. %']

players_final['AccPasses'] = player_filter['Passes précises. %']
players_final['Ball'] = player_filter['Passes réceptionnées par 90']

players_final['Lg'] = player_filter['Passes longues par 90']
players_final['Longueur'] = player_filter['Longueur moyenne des passes. m']

print(player_filter)

x_carac = 'AccPasses'
y_carac = 'Ball'

# players_final['Position'] = player_filter['Pos']
# players_final['npG/90'] = player_filter['G-PK']/player_filter['90s']
# players_final['npxG/90'] = player_filter['npxG']/player_filter['90s']
# players_final['xDS/90'] = player_filter['xG+xA/90']
# players_final['DS/90'] = player_filter['G+A']
# players_final['Champ'] = player_filter['Championnat']

## Mean calculations for important statistics in players_final
x_mean = np.mean(players_final[x_carac]) #Mean DS/90
y_mean = np.mean(players_final[y_carac]) #Mean xDS/90

## Splitting DataFrame into 4; one per champ France Italie Allemagne Espagne
# players_filter = ((players_final['Champ'] == 'France'))
# ligue1_df = players_final[players_filter]
#
# players_filter = ((players_final['Champ'] == 'Italie'))
# serieA_df = players_final[players_filter]
#
# players_filter = ((players_final['Champ'] == 'Espagne'))
# liga_df = players_final[players_filter]
#
# players_filter = ((players_final['Champ'] == 'Allemagne'))
# bundes_df = players_final[players_filter]
#
# players_filter = ((players_final['Champ'] == 'Angleterre'))
# pl_df = players_final[players_filter]


## Creating the scatter plot
# Establishing lists used for plotting in Matplotlib
x = list(players_final[x_carac])
y = list(players_final[y_carac])
team = list(players_final['Equipe'])
names = list(players_final['Player'])

# Creating empty plot in desired 'fivethirtyeight' style with gridlines and desired backround colours and sizes, as well
# as aesthetic settings
fig, ax = plt.subplots(figsize=(10, 10))
matplotlib.style.use('fivethirtyeight')
ax.grid(True, color='xkcd:dark grey')
fig.patch.set_facecolor('#0b0d0f')
ax.set_facecolor('#171b1e')
ax.spines['bottom'].set_color('xkcd:off white')
ax.spines['top'].set_color('xkcd:off white')
ax.spines['left'].set_color('xkcd:off white')
ax.spines['right'].set_color('xkcd:off white')
ax.spines['bottom'].set_linewidth(1)
ax.spines['top'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)
ax.spines['right'].set_linewidth(1)
ax.tick_params(axis='x', colors='xkcd:off white')
ax.tick_params(axis='y', colors='xkcd:off white')
plt.text(1.075, 0.5, "\n", \
         horizontalalignment='right', verticalalignment='top', color='xkcd:off white', size='18',
         transform=ax.transAxes)
plt.text(1.1, -0.075, '\n', \
         horizontalalignment='right', verticalalignment='top', color='xkcd:off white', \
         style='italic', transform=ax.transAxes, size='14')

# Establishing x and y limits
xlimval = max(x)*1.01
ylimval = max(y)*1.01
xmin = min(x)*0.99
ymin = min(y)*0.99
plt.xlim(xmin, xlimval*1.1)
plt.ylim(ymin, ylimval*1.1)
#ax.set_xticklabels(['',0.5,1.0,1.5,2.0,2.5,3.0])

# Using Matplotlib's rainbow_text function from previous cell to label subtitle legend
# words = "Ligue 1 vs Liga vs Serie A vs Bundesliga Players, 2021/22".split()
# colors = ['xkcd:blue', 'xkcd:blue', 'xkcd:off white', 'xkcd:red', 'xkcd:off white', 'xkcd:green', \
#           'xkcd:green', 'xkcd:off white', 'xkcd:yellow', 'xkcd:off white', 'xkcd:off white']
# rainbow_text((xlimval*1.2)/4,ylimval*1.1+0.01, words, colors, size=18)

# plt.text(xlimval*0.7,ylimval*1.05,'Gros volume d\'action décisive et les concrétise', color='white') #up right
# plt.text(xlimval*0.7,0.3,'Petit volume d\'action mais arrive à être décisif', color='white') #down right
# plt.text(0.1,ylimval*0.8,'Gros volume d\'action mais n\'y arrive pas', color='white') #up left

# Adding graph and axes titles
ax.set_xlabel('\nPasses vers la surface adverse par 90 min\n', color='xkcd:off white', size=15)
ax.set_ylabel('\nTouches de balle dans la surface adverse par 90 min', color='xkcd:off white', size=15)
ax.set_title("\nPrésence dans la surface de Kenneth Taylor vs Top 5 européen & Eredivisie - 2022/2023\n", color='xkcd:off white', size=20)

# marker_fr = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positionfr]
# marker_es = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positiones]
# marker_it = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positionit]
# marker_al = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positional]

# x_diag = np.linspace(0,xlimval,100)
# y_diag = x_diag
# plt.plot(x_diag, y_diag, '--', color='grey', linewidth=1)
# plt.text(0.7, 0.72, 'Performance médiane', style = 'italic',
#             fontweight = 'bold', fontsize = 8, rotation = 37, color='xkcd:grey')

# Adding plot points from each of the three DataFrames in different colours
for i in range(len(x)):
    if names[i] != 'K. Taylor' and team[i] != 'Ajax':
        plt.scatter(x=x[i], y=y[i], s=75, color='xkcd:off white', zorder=100, marker='.')
    else:
        plt.scatter(x=x[i], y=y[i], s=75, color='#D2122E', zorder=100, marker='.')


# Creating and labelling average lines
plt.axhline(y=y_mean, xmin=-100, xmax=100, color='xkcd:dark grey', linestyle='--', linewidth=2)
plt.axvline(x=x_mean, ymin=-100, ymax=100, color='xkcd:dark grey', linestyle='--', linewidth=2, zorder=0.2)
plt.text((x_mean-xmin) / (xlimval-xmin), 0.995, 'Moy', \
         horizontalalignment='right', verticalalignment='top', color='xkcd:grey', transform=ax.transAxes)
plt.text(0.995, (y_mean-ymin) / (ylimval-ymin), 'Moy', \
         horizontalalignment='right', verticalalignment='top', color='xkcd:grey', transform=ax.transAxes)
plt.text(0.5, 1.05, 'Milieux centraux avec 350+ min en 2022-2023', \
         horizontalalignment='center', verticalalignment='top', color='xkcd:grey', transform=ax.transAxes)

# Annotating some text below and some above- change based on need

#For a full annotation
#TOP PLAYERS
# for i in range(0,len(x)):
#     if names[i] == 'E. Skhiri':
#         x_ef = x[i]
#         y_ef = y[i]

for i in range(0,len(x)):
    if names[i] == 'K. Taylor':
        plt.annotate(names[i], (x[i], y[i]+0.08), color='#D2122E',horizontalalignment='center', fontsize=12, zorder=100, weight='bold')
    elif names[i] != 'K. Taylor' and team[i] != 'Ajax' and x[i] > 4:
        plt.annotate(names[i], (x[i], y[i]+0.08), color='xkcd:off white', horizontalalignment='center', fontsize=8,
                     zorder=100)
    elif names[i] != 'K. Taylor' and team[i] != 'Ajax' and y[i] >= 3:
        plt.annotate(names[i], (x[i], y[i]+0.08), color='xkcd:off white', horizontalalignment='center', fontsize=8,
                     zorder=100)
    elif names[i] != 'K. Taylor' and team[i] == 'Ajax':
        plt.annotate(names[i], (x[i], y[i]+0.08), color='#D2122E', horizontalalignment='center', fontsize=8,
                     zorder=100, weight='bold')

# Watermarking visualization
plt.text(0.77, -0.06, 'Visualisation réalisée par Data\'Scout @datascout_\n'
                      'Data issue de WyScout', \
         horizontalalignment='left', verticalalignment='top', color='xkcd:off white', transform=ax.transAxes,
         zorder=1000, size=7)

plt.show()