import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mplsoccer import PyPizza, add_image, FontManager

#1. ENREGISTRER TOUS LES LOGOS PNG DES EQUIPES DANS UN DOSSIER /images ET LES REDIMENSIONNER A LA MEME TAILLE (300x300)
#2. CREER CSV AVEC LES STATS VOULUES

df = pd.read_csv('JPL.csv')
df.head()
df['path'] = df['Equipe'] + '.png'
# df['xG'] = df['xB']
# df['xGA'] = df['xGA']
df['Pts'] = df['Points']
df['xPts'] = df['Expected points']

df['Buts'] = df['Buts']
df['xB'] = df['xB']
df['Buts contre'] = df['Buts concédés']
df['xGA'] = df['xGA']
# df['GDiff'] = df['Buts']-df['xB'] # +10 (attaque en surperf)
# df['GADiff'] = df['Buts encaissés']-df['xGA'] # +10 (défense en sous perf)
df['Buts'] = df['Buts']
df['CPA%'] = round(((df['ButCorner'] + df['ButCF'] + df['ButPeno']) / df['Buts']) * 100, 2)
df['RatioXG'] = round(df['xB par tir'] * 100, 2)
df['TirsCadrés'] = df['Tirs90'] * df['Target%'] / 100
df['Drib'] = df['Dribbles90']
df['Drib%'] = df['Dribbles%']
df['Centre'] = df['Centres90']
df['Centre%'] = df['Centres%']
df['CentreR'] = round((df['CentreDroite'] / df['Centres'] * 100), 2)
df['CentreL'] = round((df['CentreGauche'] / df['Centres'] * 100), 2)
df['Box'] = df['TouchesSurface90']
df['HJ'] = df['HJ90']
df['ButsContre90'] = df['ButsContre90']
df['IntPAdj'] = round(df['Interceptions90'] / (100 - df['Possession']) * 50, 2)
df['Lost'] = df['BallesPerdues90']
df['Fouls'] = df['Fautes90']
df['Cards'] = df['Cartons']
df['Def'] = df['DuelsDef90']
df['Def%'] = df['DuelsDef%']
df['Aer'] = df['DuelsAer90']
df['Aer%'] = df['DuelsAer%']
df['Intens'] = df['Intensité des challenges']

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


def graph_building(graph_type, champ):
    if graph_type == 'classement':
        moy = False
        diag = True
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Pts'
        y_carac = 'xPts'

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
        fig.text(.4, .98, 'Classement', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Points marqués', size=7, color='#575654')
        fig.text(.05, .35, 'Points attendus marqués', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.38,.65,'Equipes en potentielle sous-performance', size=6, color='blue', weight='bold', ha='center')
        fig.text(.6,.25,'Equipes en potentielle sur-performance', size=6, color='orange', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'attaque':
        moy = False
        diag = True
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Buts'
        y_carac = 'xB'

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
        fig.text(.35, .98, 'Performances offensives', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Buts marqués', size=7, color='#575654')
        fig.text(.05, .38, 'Buts attendus', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.38,.65,'Attaque en potentielle sous-performance', size=6, color='blue', weight='bold', ha='center')
        fig.text(.6,.25,'Attaque en potentielle sur-performance', size=6, color='orange', weight='bold', ha='center')

        ## Save plot
        plt.savefig("%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'defense':
        moy = False
        diag = True
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Buts contre'
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
        fig.text(.3, .98, 'Performances défensives', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Buts encaissés', size=7, color='#575654')
        fig.text(.05, .32, 'Buts encaissés attendus', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.38, .65, 'Défense en potentielle sur-performance', size=6, color='orange', weight='bold', ha='center')
        fig.text(.6, .28, 'Défense en potentielle sous-performance', size=6, color='blue', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'tirs':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'RatioXG'
        y_carac = 'TirsCadrés'

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
        fig.text(.3, .98, 'Qualité vs Quantité des tirs', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Ratio d\'xG par tir', size=7, color='#575654')
        fig.text(.05, .32, 'Tirs cadrés par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Peu de tirs,\nTirs de qualité', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Beaucoup de tirs,\nTirs de qualité', size=5, color='green', weight='bold', ha='center')
        fig.text(.2,.85,'Beaucoup de tirs,\nTirs de faible qualité', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.15,'Peu de tirs,\nTirs de faible qualité', size=5, color='red', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'centres':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Centre%'
        y_carac = 'Centre'

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
        fig.text(.26, .98, 'Précision vs Quantité de centres', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Pourcentage de centres réussis', size=7, color='#575654')
        fig.text(.05, .32, 'Centres par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.2,'Moins de centres,\nCentres précis', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Beaucoup de centres,\nCentres précis', size=5, color='green', weight='bold', ha='center')
        fig.text(.2,.75,'Beaucoup de centres,\nCentres imprécis', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.17,'Moins de centres,\nCentres imprécis', size=5, color='red', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'centres2':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'CentreR'
        y_carac = 'CentreL'

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
        fig.text(.34, .98, 'Origine des centres', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Centres venus de la droite (%)', size=7, color='#575654')
        fig.text(.05, .32, 'Centres venus de la gauche (%)', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8, .22, 'Centres majoritairement\nvenus de la droite', size=6, color='orange', weight='bold',
                 ha='center')
        fig.text(.27, .8, 'Centres majoritairement\nvenus de la gauche', size=6, color='blue', weight='bold',
                 ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'dribbles':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Drib%'
        y_carac = 'Drib'

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
        fig.text(.26, .98, 'Quantité vs Réussite des dribbles', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Pourcentage de dribbles réussis', size=7, color='#575654')
        fig.text(.05, .32, 'Dribbles par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Moins de dribbles,\nBonne réussite', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Beaucoup de dribbles,\nBonne réussite', size=5, color='green', weight='bold', ha='center')
        fig.text(.2,.85,'Beaucoup de dribbles,\nFaible réussite', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.15,'Moins de dribbles,\nFaible réussite', size=5, color='red', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'permeabilite':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'TirsContre90'
        y_carac = 'ButsContre90'

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
        fig.text(.3, .98, 'Perméabilité des défenses', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Tirs concédés par match', size=7, color='#575654')
        fig.text(.05, .32, 'Buts encaissés par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Défense impénétrable,\nDéfense sous pression', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Défense perméable,\nDéfense sous pression', size=5, color='red', weight='bold', ha='center')
        fig.text(.2,.85,'Défense perméable,\nDéfense sans pression', size=5, color='orange', weight='bold', ha='center')
        fig.text(.23,.33,'Défense impénétrable,\nDéfense sans pression', size=5, color='green', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'recup':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'IntPAdj'
        y_carac = 'Lost'

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
        fig.text(.25, .98, 'Possession & Récupération du ballon', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.35, 0.02, 'Interceptions par match (ajustés à la possession)', size=7, color='#575654')
        fig.text(.05, .32, 'Balles perdues par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Perd peu de ballons,\nBeaucoup d\'interceptions', size=5, color='green', weight='bold', ha='center')
        fig.text(.78,.85,'Perd beaucoup de ballons,\nBeaucoup d\'interceptions', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.85,'Perd beaucoup de ballons,\nPeu d\'interceptions', size=5, color='red', weight='bold', ha='center')
        fig.text(.2,.15,'Perd peu de ballons,\nPeu d\'interceptions', size=5, color='orange', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'faute':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Fouls'
        y_carac = 'Cards'

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
        fig.text(.4, .98, 'Discipline', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Fautes commises par match', size=7, color='#575654')
        fig.text(.05, .32, 'Cartons reçus', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Bcp de fautes commises,\nPeu de cartons reçus', size=5, color='orange', weight='bold', ha='center')
        fig.text(.78,.85,'Bcp de fautes commises,\nBcp de cartons reçus', size=5, color='red', weight='bold', ha='center')
        fig.text(.2,.85,'Peu de fautes commises,\nBcp de cartons reçus', size=5, color='orange', weight='bold', ha='center')
        fig.text(.25,.15,'Peu de fautes commises,\nPeu de cartons reçus', size=5, color='green', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'pressing':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Intens'
        y_carac = 'PPDA'

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
        fig.text(.35, .98, 'Intensité du pressing', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.3, 0.02, 'Duels, tacles & interceptions par minute de possession adverse', size=7, color='#575654')
        fig.text(.05, .42, 'PPDA', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.75,.25,'Pressing collectif intense', size=6, color='blue', weight='bold', ha='center')
        fig.text(.27,.75,'Pressing collectif peu intense', size=6, color='orange', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'cpa':
        moy = False
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Intens'
        y_carac = 'PPDA'

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
        fig.text(.34, .98, 'Importance des CPA', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.35, 0.02, 'Buts marqués', size=7, color='#575654')
        fig.text(.05, .35, 'Part de buts marqués sur CPA (%)', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.75,.25,'Forte attaque,\nfaible part de buts sur CPA', size=6, color='orange', weight='bold', ha='center')
        fig.text(.22,.8,'Faible attaque,\ngrosse part de buts sur CPA', size=6, color='blue', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'dueldef':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Def%'
        y_carac = 'Def'

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
        fig.text(.37, .98, 'Duels défensifs', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Pourcentage de duels réussis', size=7, color='#575654')
        fig.text(.05, .32, 'Duels défensifs par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Peu de duels,\nBonne réussite', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Beaucoup de duels,\nBonne réussite', size=5, color='green', weight='bold', ha='center')
        fig.text(.2,.85,'Beaucoup de duels,\nFaible réussite', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.15,'Peu de duels,\nFaible réussite', size=5, color='red', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'duelaer':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Aer%'
        y_carac = 'Aer'

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
        fig.text(.43, .98, 'Duels aériens', size=15, weight='bold')
        fig.text(.38, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Pourcentage de duels aériens réussis', size=7, color='#575654')
        fig.text(.05, .32, 'Duels aériens par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.15,'Peu de duels aériens,\nBonne réussite', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Beaucoup de duels aériens,\nBonne réussite', size=5, color='green', weight='bold', ha='center')
        fig.text(.2,.85,'Beaucoup de duels aériens,\nFaible réussite', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.15,'Peu de duels aériens,\nFaible réussite', size=5, color='red', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    elif graph_type == 'prog':
        moy = True
        diag = False
        # METTRE ICI LES DEUX CARACS QUE L'ON VEUT CONFRONTER
        x_carac = 'Run90'
        y_carac = 'Prog90'

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
        fig.text(.32, .98, 'Progression du ballon', size=15, weight='bold')
        fig.text(.33, .93, "Equipes de %s - Saison 2022/2023" % (champ), size=10)

        ## Avg line explanation
        fig.text(.4, 0.02, 'Courses progressives par match', size=7, color='#575654')
        fig.text(.05, .32, 'Passes progressives par match', size=7, color='#575654', rotation=90)

        CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
        CREDIT_2 = "Données issues de WyScout"

        font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                                   "Roboto-Italic.ttf?raw=true"))
        fig.text(
            0.9, 0.001, f"{CREDIT_1}\n{CREDIT_2}", size=4,
            fontproperties=font_italic.prop, color="#575654",
            ha="right"
        )

        fig.text(.8,.18,'Peu de passes progressives,\nBcp de courses', size=5, color='orange', weight='bold', ha='center')
        fig.text(.8,.85,'Bcp de passes progressives,\nBcp de courses', size=5, color='green', weight='bold', ha='center')
        fig.text(.2,.85,'Bcp de passes progressives,\nPeu de courses', size=5, color='orange', weight='bold', ha='center')
        fig.text(.2,.25,'Peu de passes progressives,\nPeu de courses', size=5, color='red', weight='bold', ha='center')

        ## Save plot
        plt.savefig("output/%s_%s_%s.png" % (x_carac, y_carac, champ), dpi=1200, bbox_inches="tight")
    else:
        print("Carac indisponible")

champ = "JPL"
carac_list = ["classement", "attaque", "defense", "tirs", "centres", "centres2", "dribbles", "permeabilite", "recup", "faute",
              "pressing", "cpa", "dueldef", "duelaer", "prog"]
for i in carac_list:
    graph_building(i, champ)
