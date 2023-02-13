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

df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/okafor_fbref.csv', header=0)


## Filtering for players with more than 10 npxG+xA, 1000 mins and 1 goal
df_filter = (df['90s'] >= 3)
player_filter = df[df_filter]
print(player_filter)

# df_filter = (df['xG'] >= 8)
# player_filter = player_filter[df_filter]

## Creating DataFrame for defenders with necessary raw and processed columns from player_filter
players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Player']
# players_final['Equipe'] = player_filter['Squad']
players_final['Succ'] = player_filter['Succ']
players_final['%'] = player_filter['%']

print(players_final)

# players_final['Position'] = player_filter['Pos']
# players_final['npG/90'] = player_filter['G-PK']/player_filter['90s']
# players_final['npxG/90'] = player_filter['npxG']/player_filter['90s']
# players_final['xDS/90'] = player_filter['xG+xA/90']
# players_final['DS/90'] = player_filter['G+A']
# players_final['Champ'] = player_filter['Championnat']

## Mean calculations for important statistics in players_final
x_mean = np.mean(players_final['Succ']) #Mean DS/90
y_mean = np.mean(players_final['%']) #Mean xDS/90

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
x = list(players_final['Succ'])
y = list(players_final['%'])
# team = list(players_final['Equipe'])
names = list(players_final['Player'])

# xfr = list(ligue1_df['xG'])
# yfr = list(ligue1_df['xA'])
# nfr = list(ligue1_df['Player'])
# champfr = list(ligue1_df['Champ'])

# xit = list(serieA_df['xG'])
# yit = list(serieA_df['xA'])
# nit = list(serieA_df['Player'])
# champit = list(serieA_df['Champ'])
#
# xes = list(liga_df['xG'])
# yes = list(liga_df['xA'])
# nes = list(liga_df['Player'])
# champes = list(liga_df['Champ'])
#
# xal = list(bundes_df['xG'])
# yal = list(bundes_df['xA'])
# nal = list(bundes_df['Player'])
# champal = list(bundes_df['Champ'])
#
# xen = list(pl_df['xG'])
# yen = list(pl_df['xA'])
# nen = list(pl_df['Player'])
# champen = list(pl_df['Champ'])

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
xmin = min(x)*1.05
ymin = min(y)*0.99
plt.xlim(xmin, xlimval*1.1)
plt.ylim(ymin, ylimval*1.1)
#ax.set_xticklabels(['',0.5,1.0,1.5,2.0,2.5,3.0])

# Using Matplotlib's rainbow_text function from previous cell to label subtitle legend
# words = "Ligue 1 vs Liga vs Serie A vs Bundesliga Players, 2021/22".split()
# colors = ['xkcd:blue', 'xkcd:blue', 'xkcd:off white', 'xkcd:red', 'xkcd:off white', 'xkcd:green', \
#           'xkcd:green', 'xkcd:off white', 'xkcd:yellow', 'xkcd:off white', 'xkcd:off white']
# rainbow_text((xlimval*1.2)/4,ylimval*1.1+0.01, words, colors, size=18)

# plt.text(0.1,0.4,'Subit des tirs difficiles et est efficace', color='green', size=8) #up right
# plt.text(-0.45,0.4,'Subit des tirs difficiles et pas efficace', color='yellow', size=8) #up right
# plt.text(0.2,0.225,'Tirs faciles et efficace', color='blue', size=8) #up right
# plt.text(-0.45,0.225,'Tirs faciles et pas efficace', color='red', size=8) #up right

# Adding graph and axes titles
ax.set_xlabel('\nChevauchées avec le ballon dans le dernier tiers par 90 min \n', color='xkcd:off white', size=15)
ax.set_ylabel('\nPasses dans le dernier tiers par 90 min', color='xkcd:off white', size=15)
ax.set_title("\nPrésence dans le dernier tiers de Joško Gvardiol vs Défenseurs de Bundesliga \n", color='xkcd:off white', size=20)

# marker_fr = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positionfr]
# marker_es = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positiones]
# marker_it = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positionit]
# marker_al = ['v' if i=="DF" else ('^' if i=="FW" else "o") for i in positional]

# x_diag = np.linspace(0,xlimval,100)
# y_diag = x_diag
# plt.plot(x_diag, y_diag, '--', color='grey', linewidth=1)
# plt.text(0.6, 0.62, 'Performance médiane', style = 'italic',
#             fontweight = 'bold', fontsize = 8, rotation = 37, color='xkcd:grey')

# Adding plot points from each of the three DataFrames in different colours
for i in range(len(x)):
    if names[i] == 'Noah Okafor':
        plt.scatter(x=x[i], y=y[i], s=75, color='#dd0741', zorder=100, marker='.')
    else:
        plt.scatter(x=x[i], y=y[i], s=75, color='xkcd:off white', zorder=100, marker='.')


# Creating and labelling average lines
plt.axhline(y=y_mean, xmin=-100, xmax=100, color='xkcd:dark grey', linestyle='--', linewidth=2)
plt.axvline(x=x_mean, ymin=-100, ymax=100, color='xkcd:dark grey', linestyle='--', linewidth=2, zorder=0.2)
plt.text((x_mean-xmin) / (xlimval-xmin), 0.995, 'Moy', \
         horizontalalignment='right', verticalalignment='top', color='xkcd:grey', transform=ax.transAxes)
plt.text(0.995, (y_mean-ymin) / (ylimval-ymin) -0.1, 'Moy', \
         horizontalalignment='right', verticalalignment='top', color='xkcd:grey', transform=ax.transAxes)
plt.text(0.5, 1.05, 'Gardiens avec au moins 15 matchs joués en 2020-2021', \
         horizontalalignment='center', verticalalignment='top', color='xkcd:grey', transform=ax.transAxes)

# Annotating some text below and some above- change based on need

#For a full annotation
#TOP PLAYERS
for i in range(0,len(x)):
    if names[i] == 'Noah Okafor':
        x_ef = x[i]
        y_ef = y[i]

for i in range(0,len(x)):
    print(names[i])
    if names[i] == 'Noah Okafor':
        plt.annotate(names[i].split()[1], (x[i], y[i]+0.003), color='#dd0741',horizontalalignment='center', fontsize=11, zorder=100, weight='bold')
    else:
        plt.annotate(names[i].split()[1], (x[i], y[i]+0.003), color='xkcd:off white',horizontalalignment='center', fontsize=9, zorder=100)



# for i in range(0,len(xfr)):
#     if xfr[i] > 15 and yfr[i] > 3.5:
#         plt.annotate(nfr[i], (xfr[i], yfr[i]+0.1), color='xkcd:blue',horizontalalignment='center', fontsize=8, zorder=100)
#     if xfr[i] > 16.3 and yfr[i] <= y_mean:
#         plt.annotate(nfr[i], (xfr[i], yfr[i]+0.1), color='xkcd:blue',horizontalalignment='center', fontsize=8, zorder=100)
#     if xfr[i] <= x_mean and yfr[i] > 6:
#         plt.annotate(nfr[i], (xfr[i], yfr[i]+0.1), color='xkcd:blue',horizontalalignment='center', fontsize=8, zorder=100)

# for i in range(0,len(xes)):
#     if xes[i] > 15 and yes[i] > 3.5:
#         plt.annotate(nes[i], (xes[i], yes[i]+0.1), color='xkcd:red',horizontalalignment='center', fontsize=8, zorder=100)
#     if xes[i] > 16.3 and yes[i] <= y_mean:
#         plt.annotate(nes[i], (xes[i], yes[i]+0.1), color='xkcd:red',horizontalalignment='center', fontsize=8, zorder=100)
#     if xes[i] <= x_mean and yes[i] > 6:
#         plt.annotate(nes[i], (xes[i], yes[i]+0.1), color='xkcd:red',horizontalalignment='center', fontsize=8, zorder=100)
#
# for i in range(0,len(xal)):
#     if xal[i] > 15 and yal[i] > 3.5 and nal[i] != 'E. Haaland':
#         plt.annotate(nal[i], (xal[i], yal[i]+0.1), color='xkcd:yellow',horizontalalignment='center', fontsize=8, zorder=100)
#     if xal[i] > 16.3 and yal[i] <= y_mean:
#         plt.annotate(nal[i], (xal[i], yal[i]+0.1), color='xkcd:yellow',horizontalalignment='center', fontsize=8, zorder=100)
#     if xal[i] <= x_mean and yal[i] > 6:
#         plt.annotate(nal[i], (xal[i], yal[i]+0.1), color='xkcd:yellow',horizontalalignment='center', fontsize=8, zorder=100)
#     if nal[i] == 'E. Haaland':
#         plt.annotate(nal[i], (xal[i], yal[i] - 0.2), color='xkcd:yellow', horizontalalignment='center', fontsize=8,
#                      zorder=100)
#
# for i in range(0,len(xen)):
#     if xen[i] > 15 and yen[i] > 3.5 and nen[i] != 'S. Mané':
#         plt.annotate(nen[i], (xen[i], yen[i]+0.1), color='xkcd:orange',horizontalalignment='center', fontsize=8, zorder=100)
#     if xen[i] > 16.3 and yen[i] <= y_mean:
#         plt.annotate(nen[i], (xen[i], yen[i]+0.1), color='xkcd:orange',horizontalalignment='center', fontsize=8, zorder=100)
#     if xen[i] <= x_mean and yen[i] > 6:
#         plt.annotate(nen[i], (xen[i], yen[i]+0.1), color='xkcd:orange',horizontalalignment='center', fontsize=8, zorder=100)
#     if nen[i] == 'S. Mané':
#         plt.annotate(nen[i], (xen[i], yen[i] - 0.2), color='xkcd:orange', horizontalalignment='center', fontsize=8,
#                      zorder=100)
#
# for i in range(0,len(xit)):
#     if xit[i] > 15 and yit[i] > 3.5 and nit[i] != 'João Pedro':
#         plt.annotate(nit[i], (xit[i], yit[i]+0.1), color='xkcd:green',horizontalalignment='center', fontsize=8, zorder=100)
#     if xit[i] > 16.3 and yit[i] <= y_mean and nit[i] != 'João Pedro':
#         plt.annotate(nit[i], (xit[i], yit[i]+0.1), color='xkcd:green',horizontalalignment='center', fontsize=8, zorder=100)
#     if xit[i] > 16.3 and yit[i] > y_mean and nit[i] != 'João Pedro':
#         plt.annotate(nit[i], (xit[i], yit[i]+0.1), color='xkcd:green',horizontalalignment='center', fontsize=8, zorder=100)
#     if xit[i] <= x_mean and yit[i] > 6 and nit[i] != 'João Pedro':
#         plt.annotate(nit[i], (xit[i], yit[i]+0.1), color='xkcd:green',horizontalalignment='center', fontsize=8, zorder=100)
#     if nit[i] == 'João Pedro':
#         plt.annotate(nit[i], (xit[i], yit[i]+0.1), color='xkcd:green', horizontalalignment='center', fontsize=10,
#                          zorder=100, weight='bold')


# Watermarking visualization
plt.text(0.77, -0.06, 'Visualisation réalisée par Data\'Scout @datascoutsorare\n'
                      'Data issue de FBRef', \
         horizontalalignment='left', verticalalignment='top', color='xkcd:off white', transform=ax.transAxes,
         zorder=1000, size=7)

plt.show()