import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mplsoccer import PyPizza, add_image, FontManager
import numpy as np

df = pd.read_csv('lateraux_filter.csv')

df.head()
df['path'] = df['Joueur'] + '.png'
df['SuccDef'] = df['Actions défensives réussies par 90']
df['DefDuels'] = df['Duels défensifs par 90']
df['DefWon'] = df['Duels défensifs gagnés. %']
df['AerDuels'] = df['Duels aériens par 90']
df['AerWon'] = df['Duels aériens gagnés. %']
df['TklPAdj'] = df['Tacles glissés PAdj']
df['IntPAdj'] = df['Interceptions PAdj']

df['Run'] = df['Courses progressives par 90']
df['Acc'] = df['Accélérations par 90']

df['KeyPasses'] = df['Passes quasi décisives par 90'] + df['Secondes passes décisives par 90'] + df['Troisièmes passes décisives par 90']
df['Third'] = df['Passes dans tiers adverse par 90']
df['Prog'] = df['Passes progressives par 90']

df['xG'] = df['xG par 90']
df['xA'] = df['xA par 90']

df['Tkl+Int'] = df['Tacles glissés PAdj'] + df['Interceptions PAdj']
df['Centre%'] = df['Сentres précises. %']
df['Cross'] = df['Centres dans la surface de but par 90']
df.head()

x_carac = 'Run'
y_carac = 'Prog'

x = list(df[x_carac])
y = list(df[y_carac])
names = list(df['Joueur'])

print(df)
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(df[x_carac], df[y_carac])
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(df[x_carac], df[y_carac], color='white')

def getImage(path):
    return OffsetImage(plt.imread('images/' + path), zoom=.05, alpha = 1)

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row[x_carac], row[y_carac]), frameon=False)
    ax.add_artist(ab)

# Set font and background colour
plt.rcParams.update({'font.family':'Avenir'})
bgcol = '#fafafa'

# Create initial plot
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
fig.set_facecolor(bgcol)
ax.set_facecolor(bgcol)
ax.scatter(df[x_carac], df[y_carac], c=bgcol)

# Change plot spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_color('#ccc8c8')
ax.spines['bottom'].set_color('#ccc8c8')

# Change ticks
plt.tick_params(axis='x', labelsize=8, color='#ccc8c8')
plt.tick_params(axis='y', labelsize=8, color='#ccc8c8')

# x = df['Pts']
# y = x
# plt.plot(x, y, '--', color='grey', linewidth=1)

# Plot badges
def getImage(path):
    return OffsetImage(plt.imread('images/' + path), zoom=.05, alpha = 1)

for index, row in df.iterrows():
    ab = AnnotationBbox(getImage(row['path']), (row[x_carac], row[y_carac]), frameon=False)
    ax.add_artist(ab)

for index in range(0,len(x)):
    if names[index] == 'B. Sosa':
        ax.annotate(names[index], (x[index], y[index]+0.5), color='black', weight='bold', horizontalalignment='center', fontsize=8,
                 zorder=100)
    if names[index] == 'R. Bensebaini':
            ax.annotate(names[index], (x[index]+0.22, y[index]-0.2), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    if names[index] == 'Alex Telles':
            ax.annotate(names[index], (x[index], y[index]+0.5), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    if names[index] == 'José Gayá':
            ax.annotate(names[index], (x[index]+0.05, y[index]-0.7), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    if names[index] == 'Renan Lodi':
            ax.annotate(names[index], (x[index], y[index]+0.5), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    if names[index] == 'Raphaël Guerreiro':
            ax.annotate(names[index].split()[1], (x[index], y[index]-0.7), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    if names[index] == 'Q. Merlin':
            ax.annotate(names[index], (x[index]-0.2, y[index]), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    if names[index] == 'Javi Galán':
            ax.annotate(names[index].split()[1], (x[index], y[index]+0.5), color='black', weight='bold',
                        horizontalalignment='center', fontsize=8,
                        zorder=100)
    # elif names[index] == 'B. Zuculini':
    #     ax.annotate(names[index], (x[index]+0.01, y[index]+0.01), color='red', weight='bold',
    #                     horizontalalignment='center', fontsize=8,
    #                     zorder=100)
    # else:
    #     ax.annotate(names[index], (x[index], y[index]+0.01), color='red', weight='bold',
    #                     horizontalalignment='center', fontsize=8,
    #                     zorder=100)

# Add average lines
# plt.hlines(df['Tkl+Int'].mean(), df['DefWon'].min(), df['DefWon'].max(), color='#c2c1c0')
# plt.vlines(df['DefWon'].mean(), df['Tkl+Int'].min(), df['Tkl+Int'].max(), color='#c2c1c0')

## Title & comment
fig.text(.25,.98,'Capacités de progression des latéraux analysés',size=10, weight='bold')
# fig.text(.4,.93,'Données prises sur la dernière année civile', size=8)

## Avg line explanation
fig.text(.3,0.02,'Courses progressives par 90 min', size=7, color='#575654')
fig.text(.05,.3,'Passes progressives par 90 min', size=7, color='#575654',rotation=90)

CREDIT_1 = "Visualisation réalisée par Data'Scout @datascoutsorare"
CREDIT_2 = "Données issues de WyScout"
CREDIT_3 = "2021 - 2022"
# CREDIT_4 = "Passes créant du danger inclus : Passes-clés, 2èmes passes décisives, 3èmes passes décisives"

font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
fig.text(
    0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=3,
    fontproperties=font_italic.prop, color="#575654",
    ha="right"
)


# ## Axes titles
# fig.text(.7,(df['GADiff'].mean()-df['GADiff'].min())/(df['GADiff'].max()-df['GADiff'].min())+0.01,'Moy. Diff Buts encaissés-xGA', size=6, color='#c2c1c0')
# fig.text((df['GDiff'].mean()-df['GDiff'].min())/(df['GDiff'].max()-df['GDiff'].min())+0.05,.17,'Moy. Diff Buts-xG', size=6, color='#c2c1c0',rotation=90)

## Save plot
plt.savefig('lateraux_prog.png', dpi=1200, bbox_inches = "tight")