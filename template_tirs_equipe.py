import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mplsoccer import PyPizza, add_image, FontManager

#1. ENREGISTRER TOUS LES LOGOS PNG DES EQUIPES DANS UN DOSSIER /images ET LES REDIMENSIONNER A LA MEME TAILLE (300x300)
#2. CREER CSV AVEC LES STATS VOULUES

df = pd.read_csv('liga_stats.csv')
df.head()
df['path'] = df['Equipe'] + '.png'

# df['Tirs'] = df['TirsTotal']
# df['TirsCadrés'] = df['Tirs90'] * df['Cadré%'] / 100
#
# df['Buts'] = df['ButsTotal']
#
# df['PartTirsHorsSurface'] = df['TirsHorsSurface'] / df['Tirs'] * 100
# df['PartButsHorsSurface'] = df['ButsHorsSurface'] / df['Buts'] * 100

df.head()

def plotting(x, y):
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    ax.scatter(df[x], df[y])
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    ax.scatter(df[x], df[y], color='white')

    def getImage(path):
        return OffsetImage(plt.imread('images/' + path), zoom=.05, alpha=1)

    for index, row in df.iterrows():
        print(index)
        print(row)
        ab = AnnotationBbox(getImage(row['path']), (row[x], row[y]), frameon=False)
        ax.add_artist(ab)

    # Set font and background colour
    plt.rcParams.update({'font.family': 'Avenir'})
    bgcol = '#fafafa'

    # Create initial plot
    fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
    fig.set_facecolor(bgcol)
    ax.set_facecolor(bgcol)
    ax.scatter(df[x], df[y], c=bgcol)

    # Change plot spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color('#ccc8c8')
    ax.spines['bottom'].set_color('#ccc8c8')

    # Change ticks
    plt.tick_params(axis='x', labelsize=8, color='#ccc8c8')
    plt.tick_params(axis='y', labelsize=8, color='#ccc8c8')
    return fig,ax

def plotting_badges(x, y, ax):
    def getImage(path):
        return OffsetImage(plt.imread('images/' + path), zoom=.05, alpha=1)

    for index, row in df.iterrows():
        ab = AnnotationBbox(getImage(row['path']), (row[x], row[y]), frameon=False)
        ax.add_artist(ab)

def diagonale(x, y, fig):
    x = df[x]
    y = x
    plt.plot(x, y, '-', color='grey', linewidth=1)
    fig.text(0.69, 0.69, 'Performance médiane', style='italic',
             fontweight='bold', fontsize=5, rotation=26, color='xkcd:grey')


def graph_building(champ):
    moy = True
    diag = False
    # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
    x_carac = 'xG'
    y_carac = 'xGA'

    fig, ax = plotting(x_carac, y_carac)

    # Pour une diagonale, performance médiane
    if diag == True:
        diagonale(x_carac, y_carac, fig)

    plotting_badges(x_carac, y_carac, ax)

    # # Add average lines
    if moy == True:
        plt.hlines(df[y_carac].mean(), df[x_carac].min(), df[x_carac].max(), color='#c2c1c0')
        plt.vlines(df[x_carac].mean(), df[y_carac].min(), df[y_carac].max(), color='#c2c1c0')
        # fig.text(.15, (df[y_carac].mean()-df[y_carac].min()) / (df[y_carac].max() - df[y_carac].min()),
        #          'Moy. Points marqués', size=6, color='#c2c1c0')
        # fig.text((df[x_carac].mean()-df[x_carac].min()) / (df[x_carac].max() - df[x_carac].min()), .15,
        #          "Moy. Points attendus", size=6, color='#c2c1c0', rotation=90)

    ## Title & comment
    fig.text(.2, .98, 'Buts attendus vs Buts concédés attendus', size=15, weight='bold')
    fig.text(.25, .93, "%s - Saison 2022/2023" % (champ), size=10)

    ## Avg line explanation
    fig.text(.4, 0.02, 'Buts attendus (xG)', size=7, color='#575654')
    fig.text(.05, .35, 'Buts concédés attendus (xGA)', size=7, color='#575654', rotation=90)

    CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
    CREDIT_2 = "Données issues de WyScout"

    font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                               "Roboto-Italic.ttf?raw=true"))
    fig.text(
        0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
        fontproperties=font_italic.prop, color="#575654",
        ha="right"
    )

    # fig.text(.38, .65, 'Equipes en potentielle sous-performance', size=6, color='blue', weight='bold', ha='center')
    # fig.text(.6, .25, 'Equipes en potentielle sur-performance', size=6, color='orange', weight='bold', ha='center')

    ## Save plot
    plt.savefig("output/%s_%s.png" % (x_carac, y_carac), dpi=1200, bbox_inches="tight")

champ = "Liga Santander"
graph_building(champ)
