import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mplsoccer import PyPizza, add_image, FontManager

#1. ENREGISTRER TOUS LES LOGOS PNG DES EQUIPES DANS UN DOSSIER /images ET LES REDIMENSIONNER A LA MEME TAILLE (300x300)
#2. CREER CSV AVEC LES STATS VOULUES

df = pd.read_csv('WC_Moyenne.csv')
df.head()
df['path'] = df['Equipe'] + '.png'

df.head()

def plotting(x, y):
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    ax.scatter(df[x], df[y])
    fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
    ax.scatter(df[x], df[y], color='white')

    def getImage(path):
        return OffsetImage(plt.imread('images/cdm/' + path), zoom=.05, alpha=1)

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
        return OffsetImage(plt.imread('images/cdm/' + path), zoom=.05, alpha=1)

    for index, row in df.iterrows():
        ab = AnnotationBbox(getImage(row['path']), (row[x], row[y]), frameon=False)
        ax.add_artist(ab)

def diagonale(x, y, fig):
    x = df[x]
    y = x
    plt.plot(x, y, '-', color='grey', linewidth=1)
    fig.text(0.69, 0.69, 'Performance médiane', style='italic',
             fontweight='bold', fontsize=5, rotation=26, color='xkcd:grey')


def graph_building(graph_type, champ, x, y):
    if graph_type == 'attaque':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = x
        y_carac = y

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
        fig.text(.35, .98, 'Coupe du Monde 2022', size=15, weight='bold')

        ## Avg line explanation
        fig.text(.35, 0.02, 'OM Final Third Padj', size=7, color='#575654')
        fig.text(.05, .15, 'Opp OM Final Third Padj', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Source des données : FIFA"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    else:
        print("Carac indisponible")

champ = "CDM"
carac_list = ["attaque"]

# ['BU Unopposed', 'BU Opposed', 'Progression', 'Final Third', 'Long Ball', 'Attacking Transition',
#  'Counter Attack', 'Set Piece', 'High Press', 'Mid Press', 'Low Press', 'HighPress%', 'MidPress%',
#  'LowPress%', 'Press', 'High Block', 'Mid Block', 'Low Block', 'Block', 'HighBlock%', 'MidBlock%', 'LowBlock%',
#  'Recovery', 'Defensive Transition', 'Counter-press', 'Possession', 'Possession adverse',
#  'Contest', 'Goals', 'Attempts', 'On target', 'Total Passes', 'Complete Passes', 'Completed Line Breaks Padj',
#  'Defensive Line Breaks Padj', 'Receptions Final Third', 'Crosses', 'Ball Progressions',
#  'Defensive pressures applied Padj', 'Direct pressures Padj', 'Forced TO', 'Second balls', 'Distance',
#  'High Speed Distance', 'OM Final Third Padj',
#  'OM Mid Third Padj', 'OM Def Third Padj', 'OM Total Padj', 'Offers received Padj', 'OM Inside Shape Padj',
#  'OM Outside Shape Padj', 'Opp OM Final Third Padj', 'Opp OM Mid Third Padj', 'Opp OM Def Third Padj',
#  'Opp OM Total Padj', 'Opp Offers received Padj', 'Opp OM Inside Shape Padj', 'Opp OM Outside Shape Padj',
#  'Possession regained Padj', 'Interceptions Padj', 'Tackles Padj', 'Ratio Poss Def Actions', 'Pressure Duration',
#  'Ball recovery Time', 'Pressing direction inside', 'Pressing direction outside', 'xG']

x = 'Ratio Poss Def Actions'
y = 'xG'
for i in carac_list:
    graph_building(i, champ, x, y)
