### Règles du CSV
# 1. Il faut absolument toutes les stats possibles (preset GRAPH_BUILDING)
# 2. Il faut "Equipe", "Place", "Matchs joués  ", "Minutes jouées  "
# 3. Sur l'Excel, sur la colonne "Place" : remplacer ', ' par '-'
# 3. Sauvegarde en CSV UTF-8
# 4. Ouvrir via bloc-notes : remplacer les ',' par '.'
# 5. Ouvrir via bloc-notes : remplacer les ';' par ','


### Modifier l'appel à la fonction scout_report
# 1. Modifier le "ws_datapath" : chemin du csv
# 2. Modifier le "savepath" : chemin de sauvegarde
# 3. Modifier le "imgpath" : chemin de l'image
# 4. Changer si nécessaires "league" & "season" (pour le titre)
# 5. Modifier le "template" : 'attacking', 'defensive', ou 'gk'
# 6. Modifier le "pos_buckets" : 'single' pour uniquement une position, 'mult' si plusieurs
# 7. Modifier le "pos" : si 'mult' voir mult positions en dessous
# 8. Modifier le "player_pos" : poste du joueur (pour le titre)
# 9. Modifier le "compares" : poste des joueurs comparés (pour le titre)
# 10. Modifier le "mins" : minutes minimum
# 11. Modifier le "name" : nom du joueur pour le titre
# 12. Modifier le "age" : âge du joueur (pour le titre)
# 13. Modifier le "club_image" : 'y' si tu veux le logo, 'n' si tu veux pas
# 14. Modifier le "save_img" : 'y' si tu veux enregistrer le radar, 'n' si tu veux pas (enregistrer la distribution à la main)
# 15. Run !!!

##### mult position inculsions:
#(Since Wyscout codes very secific positions, like LWF or RWF instead of just WF, the code searches for positions that *contain* these positions below)
#(of course you can go into the code (starting line 45) and modify/add/delete any of these you want to)

### Forward
# CF, RW, LW, AMF

### CF and W
# CF, RW, LW

### Forward no ST
# AMF, LW, RW

### Winger
# WF, LAMF, RAMF, LW, RW, (excludes WBs)

### Midfielder
# CMF, DMF, AMF

### Midfielder no CAM
# CMF, DMF

### Fullback
# LB, RB, WB

### Defenders
#LB, RB, WB, CB, DMF

# import pkg_resources
# pkg_resources.require("seaborn==0.11.1")
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean
from math import pi

sns.set_style("white")
import warnings

warnings.filterwarnings('ignore')
import matplotlib

matplotlib.rcParams.update(matplotlib.rcParamsDefault)


def scout_report(ws_datapath, league, season, xtra, template, pos_buckets, pos, player_pos, mins, compares, name,
                 ws_name, team, age, taille, pied, sig, club_image, save_img, extra_text, savepath=None, imgpath=None):
    import matplotlib
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    df = pd.read_csv(ws_datapath)

    df['pAdj Tkl+Int par 90'] = df['Tacles glissés PAdj'] + df['Interceptions PAdj']
    df['1ere, 2eme, 3eme passes décisives'] = df['Passes décisives par 90'] + df['Secondes passes décisives par 90'] + df['Troisièmes passes décisives par 90']
    df['xA par Passe décisive avec tir'] = df['xA par 90'] / df['Passes décisives avec tir par 90']
    df['Duels aériens gagnés par 90'] = df['Duels aériens par 90'] * (df['Duels aériens gagnés. %'] / 100)
    df['Cartes par 90'] = df['Cartons jaunes par 90'] + df['Cartons rouges par 90']
    df['Clean sheets, %'] = df['Cages inviolées'] / df['Matchs joués  ']
    df['npxG'] = df['xG'] - (.76 * df['Penalties pris'])
    df['npxG par 90'] = df['npxG'] / (df['Minutes jouées  '] / 90)
    df['npxG par tir'] = df['npxG'] / (df['Tir'] - df['Penalties pris'])

    df['Pos'] = ''
    for i in range(len(df)):
        df['Pos'][i] = df['Place'][i].split()[0]

    #####################################################################################
    # Filter data
    dfProspect = df[df['Minutes jouées  '] >= mins]

    if pos_buckets == 'single':
        dfProspect = dfProspect[dfProspect['Pos'].str.contains(pos)]

    if pos_buckets == 'mult':
        if pos == 'Forward':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CF')) |
                                    (dfProspect['Pos'].str.contains('RW')) |
                                    (dfProspect['Pos'].str.contains('LW')) |
                                    (dfProspect['Pos'].str.contains('AMF'))]
        if pos == 'CF and W':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CF')) |
                                    (dfProspect['Pos'].str.contains('RW')) |
                                    (dfProspect['Pos'].str.contains('LW'))]
        if pos == 'Forward no ST':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('AMF')) |
                                    (dfProspect['Pos'].str.contains('RW')) |
                                    (dfProspect['Pos'].str.contains('LW'))]
        if pos == 'Winger':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('WF')) |
                                    (dfProspect['Pos'].str.contains('LAMF')) |
                                    (dfProspect['Pos'].str.contains('RAMF')) |
                                    (dfProspect['Pos'].str.contains('LW')) |
                                    (dfProspect['Pos'].str.contains('RW'))]
            # dfProspect = dfProspect[~dfProspect['Pos'].str.contains('WB')]
        if pos == 'Midfielder':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CMF')) |
                                    (dfProspect['Pos'].str.contains('DMF')) |
                                    (dfProspect['Pos'].str.contains('AMF'))]
        if pos == 'Midfielder Advanced':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CMF')) |
                                    (dfProspect['Pos'].str.contains('AMF'))]
        if pos == 'Midfielder no CAM':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CMF')) |
                                    (dfProspect['Pos'].str.contains('DMF'))]
        if pos == 'Fullback':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('LB')) |
                                    (dfProspect['Pos'].str.contains('RB')) |
                                    (dfProspect['Pos'].str.contains('WB'))]
        if pos == 'Defenders':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('LB')) |
                                    (dfProspect['Pos'].str.contains('RB')) |
                                    (dfProspect['Pos'].str.contains('WB')) |
                                    (dfProspect['Pos'].str.contains('CB')) |
                                    (dfProspect['Pos'].str.contains('DMF'))]
        if pos == 'DC':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CB'))]
        if pos == 'Buteur':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('CF'))]
        if pos == 'Piston':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('WB'))]
        if pos == 'Nkuba':
            dfProspect = dfProspect[(dfProspect['Pos'].str.contains('WB')) |
                                    (dfProspect['Pos'].str.contains('LW')) |
                                    (dfProspect['Pos'].str.contains('RW')) |
                                    (dfProspect['Pos'].str.contains('LAMF')) |
                                    (dfProspect['Pos'].str.contains('RAMF'))]
            dfProspect = dfProspect[~(dfProspect['Pos'].str.contains('WF'))]


    # FORWARD
    fwd1 = "Buts hors penalty par 90"
    fwd2 = "npxG par 90"
    fwd3 = "Passes décisives par 90"
    fwd4 = "xA par 90"
    fwd5 = "Dribbles réussis. %"
    fwd6 = "Taux de conversion but/tir"
    fwd7 = "Passes décisives avec tir par 90"
    fwd8 = "Secondes passes décisives par 90"
    fwd9 = "Courses progressives par 90"
    fwd10 = "Passes progressives par 90"
    fwd11 = "Touches de balle dans la surface de réparation sur 90"
    fwd12 = "Duels aériens gagnés. %"
    # MIDFIELD
    mid1 = "Passes courtes / moyennes précises. %"
    mid2 = "Longues passes précises. %"
    mid3 = "Passes intelligentes précises. %"
    mid4 = "Passes décisives avec tir par 90"
    mid5 = "xA par 90"
    mid6 = "Passes décisives par 90"
    mid7 = "Secondes passes décisives par 90"
    mid8 = "Troisièmes passes décisives par 90"
    mid9 = "Passes progressives par 90"
    mid10 = "Courses progressives par 90"
    mid11 = "Duels gagnés. %"
    mid12 = "pAdj Tkl+Int par 90"
    # DEFENDER
    def1 = "Actions défensives réussies par 90"
    def2 = "Tacles glissés PAdj"
    def3 = "Duels défensifs gagnés. %"
    def4 = "Fautes par 90"
    def5 = "Cartes par 90"
    def6 = "Tirs contrés par 90"
    def7 = "Interceptions PAdj"
    def8 = "Duels aériens gagnés. %"
    def9 = "Longues passes précises. %"
    def10 = "1ere, 2eme, 3eme passes décisives"
    def11 = "Passes progressives par 90"
    def12 = "Courses progressives par 90"
    # GOALKEEPER
    gk1 = "Buts concédés par 90"
    gk2 = "Buts évités par 90"
    gk3 = "Tirs contre par 90"
    gk4 = "Enregistrer. %"
    gk5 = "Clean sheets, %"
    gk6 = "Sorties par 90"
    gk7 = "Duels aériens par 90"
    gk8 = "Passes par 90"
    gk9 = "Longues passes précises. %"
    gk10 = "Longueur moyenne des passes longues. m"
    # OTHERS
    extra = "Passes précises. %"
    extra2 = 'Tirs par 90'
    extra3 = 'Сentres précises. %'
    extra4 = 'Passes judicieuses par 90'
    extra5 = 'xA par Passe décisive avec tir'
    extra6 = 'Accélérations par 90'
    extra7 = 'Duels aériens gagnés par 90'
    extra8 = 'Fautes subies par 90'
    extra9 = 'npxG par tir'
    extra10 = 'Centres par 90'

    df_pros = dfProspect

    dfProspect["midpct1"] = stats.rankdata(dfProspect[mid1], "average") / len(dfProspect[mid1])
    dfProspect["midpct2"] = stats.rankdata(dfProspect[mid2], "average") / len(dfProspect[mid2])
    dfProspect["midpct3"] = stats.rankdata(dfProspect[mid3], "average") / len(dfProspect[mid3])
    dfProspect["midpct4"] = stats.rankdata(dfProspect[mid4], "average") / len(dfProspect[mid4])
    dfProspect["midpct5"] = stats.rankdata(dfProspect[mid5], "average") / len(dfProspect[mid5])
    dfProspect["midpct6"] = stats.rankdata(dfProspect[mid6], "average") / len(dfProspect[mid6])
    dfProspect["midpct7"] = stats.rankdata(dfProspect[mid7], "average") / len(dfProspect[mid7])
    dfProspect["midpct8"] = stats.rankdata(dfProspect[mid8], "average") / len(dfProspect[mid8])
    dfProspect["midpct9"] = stats.rankdata(dfProspect[mid9], "average") / len(dfProspect[mid9])
    dfProspect["midpct10"] = stats.rankdata(dfProspect[mid10], "average") / len(dfProspect[mid10])
    dfProspect["midpct11"] = stats.rankdata(dfProspect[mid11], "average") / len(dfProspect[mid11])
    dfProspect["midpct12"] = stats.rankdata(dfProspect[mid12], "average") / len(dfProspect[mid12])
    dfProspect["fwdpct1"] = stats.rankdata(dfProspect[fwd1], "average") / len(dfProspect[fwd1])
    dfProspect["fwdpct2"] = stats.rankdata(dfProspect[fwd2], "average") / len(dfProspect[fwd2])
    dfProspect["fwdpct3"] = stats.rankdata(dfProspect[fwd3], "average") / len(dfProspect[fwd3])
    dfProspect["fwdpct4"] = stats.rankdata(dfProspect[fwd4], "average") / len(dfProspect[fwd4])
    dfProspect["fwdpct5"] = stats.rankdata(dfProspect[fwd5], "average") / len(dfProspect[fwd5])
    dfProspect["fwdpct6"] = stats.rankdata(dfProspect[fwd6], "average") / len(dfProspect[fwd6])
    dfProspect["fwdpct7"] = stats.rankdata(dfProspect[fwd7], "average") / len(dfProspect[fwd7])
    dfProspect["fwdpct8"] = stats.rankdata(dfProspect[fwd8], "average") / len(dfProspect[fwd8])
    dfProspect["fwdpct9"] = stats.rankdata(dfProspect[fwd9], "average") / len(dfProspect[fwd9])
    dfProspect["fwdpct10"] = stats.rankdata(dfProspect[fwd10], "average") / len(dfProspect[fwd10])
    dfProspect["fwdpct11"] = stats.rankdata(dfProspect[fwd11], "average") / len(dfProspect[fwd11])
    dfProspect["fwdpct12"] = stats.rankdata(dfProspect[fwd12], "average") / len(dfProspect[fwd12])
    dfProspect["defpct1"] = stats.rankdata(dfProspect[def1], "average") / len(dfProspect[def1])
    dfProspect["defpct2"] = stats.rankdata(dfProspect[def2], "average") / len(dfProspect[def2])
    dfProspect["defpct3"] = stats.rankdata(dfProspect[def3], "average") / len(dfProspect[def3])
    dfProspect["defpct4"] = 1 - stats.rankdata(dfProspect[def4], "average") / len(dfProspect[def4])
    dfProspect["defpct5"] = 1 - stats.rankdata(dfProspect[def5], "average") / len(dfProspect[def5])
    dfProspect["defpct6"] = stats.rankdata(dfProspect[def6], "average") / len(dfProspect[def6])
    dfProspect["defpct7"] = stats.rankdata(dfProspect[def7], "average") / len(dfProspect[def7])
    dfProspect["defpct8"] = stats.rankdata(dfProspect[def8], "average") / len(dfProspect[def8])
    dfProspect["defpct9"] = stats.rankdata(dfProspect[def9], "average") / len(dfProspect[def9])
    dfProspect["defpct10"] = stats.rankdata(dfProspect[def10], "average") / len(dfProspect[def10])
    dfProspect["defpct11"] = stats.rankdata(dfProspect[def11], "average") / len(dfProspect[def11])
    dfProspect["defpct12"] = stats.rankdata(dfProspect[def12], "average") / len(dfProspect[def12])
    dfProspect["gkpct1"] = 1 - stats.rankdata(dfProspect[gk1], "average") / len(dfProspect[gk1])
    dfProspect["gkpct2"] = stats.rankdata(dfProspect[gk2], "average") / len(dfProspect[gk2])
    dfProspect["gkpct3"] = stats.rankdata(dfProspect[gk3], "average") / len(dfProspect[gk3])
    dfProspect["gkpct4"] = stats.rankdata(dfProspect[gk4], "average") / len(dfProspect[gk4])
    dfProspect["gkpct5"] = stats.rankdata(dfProspect[gk5], "average") / len(dfProspect[gk5])
    dfProspect["gkpct6"] = stats.rankdata(dfProspect[gk6], "average") / len(dfProspect[gk6])
    dfProspect["gkpct7"] = stats.rankdata(dfProspect[gk7], "average") / len(dfProspect[gk7])
    dfProspect["gkpct8"] = stats.rankdata(dfProspect[gk8], "average") / len(dfProspect[gk8])
    dfProspect["gkpct9"] = stats.rankdata(dfProspect[gk9], "average") / len(dfProspect[gk9])
    dfProspect["gkpct10"] = stats.rankdata(dfProspect[gk10], "average") / len(dfProspect[gk10])
    dfProspect["extrapct"] = stats.rankdata(dfProspect[extra], "average") / len(dfProspect[extra])
    dfProspect["extrapct2"] = stats.rankdata(dfProspect[extra2], "average") / len(dfProspect[extra2])
    dfProspect["extrapct3"] = stats.rankdata(dfProspect[extra3], "average") / len(dfProspect[extra3])
    dfProspect["extrapct4"] = stats.rankdata(dfProspect[extra4], "average") / len(dfProspect[extra4])
    dfProspect["extrapct5"] = stats.rankdata(dfProspect[extra5], "average") / len(dfProspect[extra5])
    dfProspect["extrapct6"] = stats.rankdata(dfProspect[extra6], "average") / len(dfProspect[extra6])
    dfProspect["extrapct7"] = stats.rankdata(dfProspect[extra7], "average") / len(dfProspect[extra7])
    dfProspect["extrapct8"] = stats.rankdata(dfProspect[extra8], "average") / len(dfProspect[extra8])
    dfProspect["extrapct9"] = stats.rankdata(dfProspect[extra9], "average") / len(dfProspect[extra9])
    dfProspect["extrapct10"] = stats.rankdata(dfProspect[extra10], "average") / len(dfProspect[extra10])

    ######################################################################

    dfRadarMF = dfProspect[(dfProspect['Joueur'] == ws_name)].reset_index(drop=True)

    if template == 'attacking':
        dfRadarMF = dfRadarMF[["Joueur",
                               "midpct4", "midpct5", 'extrapct5', "midpct6", "midpct7", 'extrapct4',
                               "fwdpct2", "fwdpct1", "fwdpct6", "extrapct9", "extrapct2", 'fwdpct11',
                               "fwdpct5", 'extrapct6', "midpct10", "midpct9",
                               "defpct1", "midpct12", 'defpct8', ]]
        dfRadarMF.rename(columns={'midpct4': "Passes\namenant\nà un tir",
                                  'midpct5': "Passes\ndécisives\nattendues (xA)",
                                  'extrapct5': 'xA par\nPasses\navant\ntir',
                                  'midpct6': "Passes\ndécisives",
                                  'midpct7': "2ème\npasses\ndécisives",
                                  'extrapct4': 'Passes\nintelligentes',
                                  "fwdpct2": "npxG",
                                  "fwdpct1": "Buts\nsans penalty",
                                  "fwdpct6": "Buts/Tir\ncadré %",
                                  "extrapct9": 'npxG\npar tir',
                                  'extrapct2': "Tirs",
                                  'fwdpct11': 'Touches\ndans\nla surface',
                                  "fwdpct5": "Réussite\ndes\ndribbles %",
                                  'extrapct6': 'Accélérations',
                                  'midpct10': "Courses\nprog.",
                                  'midpct9': "Passes\nprog.",
                                  'defpct1': "Actions\ndéfensives",
                                  'midpct12': "Tacles & Int\n(pAdj)",
                                  'defpct8': 'Duels\naériens\nremportés %'
                                  }, inplace=True)
        print('Number of players comparing to:', len(dfProspect))

    if template == 'defensive':
        dfRadarMF = dfRadarMF[["Joueur",
                               'defpct1', "defpct2", "defpct3", "defpct6", "defpct7", 'extrapct7', "defpct8",
                               "defpct9", "midpct1", "defpct10", "midpct5", "defpct11", "defpct12", "fwdpct5",
                               'extrapct6',
                               "defpct4", "defpct5", 'extrapct8'
                               ]]
        dfRadarMF.rename(columns={'defpct1': 'Actions\ndéfensives',
                                  'defpct2': "Tacles\n(pAdj)",
                                  'defpct3': "Duels\ndéfensifs\ngagnés %",
                                  'defpct6': "Tirs\ncontrés",
                                  'defpct7': "Interceptions\n(pAdj)",
                                  'extrapct7': 'Duels aériens\ngagnés',
                                  'defpct8': "Duels\naériens\n%",
                                  'defpct9': "Passes\nlongues\n%",
                                  'midpct1': 'Passes\ncourtes\n%',
                                  'defpct10': "Passes dé &\n2eme/3eme\nPD",
                                  'midpct5': "Passes\ndécisives\nattendues (xA)",
                                  'defpct11': "Passes\nprog.",
                                  'defpct12': "Courses\nprog.",
                                  "fwdpct5": "Réussite\ndes\ndribbles %",
                                  'extrapct6': 'Accélérations',
                                  'defpct4': "Fautes\ncommises",
                                  'defpct5': "Cartons\nreçus",
                                  'extrapct8': 'Fautes\nsubies'
                                  }, inplace=True)
        print('Number of players comparing to:', len(dfProspect))

    if template == 'gk':
        dfRadarMF = dfRadarMF[["Joueur",
                               'gkpct1', 'gkpct2', 'gkpct3', 'gkpct4', 'gkpct5',
                               'gkpct6', 'gkpct7', 'gkpct8', 'gkpct9', 'gkpct10'
                               ]]
        dfRadarMF.rename(columns={'gkpct1': 'Buts\nconcédés',
                                  'gkpct2': "Buts évités\nvs attendus",
                                  'gkpct3': "Tirs subis",
                                  'gkpct4': "Arrêts %",
                                  'gkpct5': "Clean Sheet %",
                                  'gkpct6': 'Sorties',
                                  'gkpct7': "Duels aériens",
                                  'gkpct8': "Passes",
                                  'gkpct9': 'Passes\nlongues',
                                  'gkpct10': "Passes\nlongues\n%",
                                  }, inplace=True)
        print('Number of players comparing to:', len(dfProspect))

    ###########################################################################

    df1 = dfRadarMF.T.reset_index()

    df1.columns = df1.iloc[0]

    df1 = df1[1:]
    df1 = df1.reset_index()
    print(df1)
    df1 = df1.rename(columns={'Joueur': 'Metric',
                              ws_name: 'Value',
                              'index': 'Group'})
    if template == 'attacking':
        for i in range(len(df1)):
            if df1['Group'][i] <= 6:
                df1['Group'][i] = 'Creativity'
            elif df1['Group'][i] <= 12:
                df1['Group'][i] = 'Shooting'
            elif df1['Group'][i] <= 16:
                df1['Group'][i] = 'Ball Movement'
            elif df1['Group'][i] <= 19:
                df1['Group'][i] = 'Defense'

    if template == 'defensive':
        for i in range(len(df1)):
            if df1['Group'][i] <= 7:
                df1['Group'][i] = 'Defending'
            elif df1['Group'][i] <= 16:
                df1['Group'][i] = 'Attacking'
            elif df1['Group'][i] <= 19:
                df1['Group'][i] = 'Fouling'

    if template == 'gk':
        for i in range(len(df1)):
            if df1['Group'][i] <= 5:
                df1['Group'][i] = 'Traditional'
            elif df1['Group'][i] <= 10:
                df1['Group'][i] = 'Modern'

    #####################################################################

    ### This link below is where I base a lot of my radar code off of
    ### https://www.python-graph-gallery.com/circular-barplot-with-groups

    def get_label_rotation(angle, offset):
        # Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle + offset) + 90
        if angle <= np.pi / 2:
            alignment = "center"
            rotation = rotation + 180
        elif 4.3 < angle < np.pi * 2:  # 4.71239 is 270 degrees
            alignment = "center"
            rotation = rotation - 180
        else:
            alignment = "center"
        return rotation, alignment

    def add_labels(angles, values, labels, offset, ax):

        # This is the space between the end of the bar and the label
        padding = .05

        # Iterate over angles, values, and labels, to add all of them.
        for angle, value, label, in zip(angles, values, labels):
            angle = angle

            # Obtain text rotation and alignment
            rotation, alignment = get_label_rotation(angle, offset)

            # And finally add the text
            ax.text(
                x=angle,
                y=1.05,
                s=label,
                ha=alignment,
                va="center",
                rotation=rotation,
            )

    # Grab the group values
    GROUP = df1["Group"].values
    VALUES = df1["Value"].values
    LABELS = df1["Metric"].values
    OFFSET = np.pi / 2

    PAD = 2
    ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
    ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
    WIDTH = (2 * np.pi) / len(ANGLES)

    offset = 0
    IDXS = []

    if template == 'attacking':
        GROUPS_SIZE = [6, 6, 4, 3]  # Attacker template
    if template == 'defensive':
        GROUPS_SIZE = [7, 8, 3]  # Defender template
    if template == 'gk':
        GROUPS_SIZE = [5, 5]  # GK template

    for size in GROUPS_SIZE:
        IDXS += list(range(offset + PAD, offset + size + PAD))
        offset += size + PAD

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    ax.set_theta_offset(OFFSET)
    ax.set_ylim(-.5, 1)
    ax.set_frame_on(False)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

    ax.bar(
        ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS,
        edgecolor="#4A2E19", linewidth=1
    )

    add_labels(ANGLES[IDXS], VALUES, LABELS, OFFSET, ax)

    offset = 0
    for group, size in zip(GROUPS_SIZE,
                           GROUPS_SIZE):  # replace first GROUPS SIZE with ['Passing', 'Creativity'] etc if needed
        # Add line below bars
        x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
        ax.plot(x1, [-.02] * 50, color="#4A2E19")

        # Add reference lines at 20, 40, 60, and 80
        x2 = np.linspace(ANGLES[offset], ANGLES[offset + PAD - 1], num=50)
        ax.plot(x2, [.2] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.4] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.60] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.80] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [1] * 50, color="#bebebe", lw=0.8)

        offset += size + PAD

    for bar in ax.patches:
        ax.annotate(format(bar.get_height() * 100, '.0f'),
                    (bar.get_x() + bar.get_width() / 2,
                     bar.get_height() - .1), ha='center', va='center',
                    size=12, xytext=(0, 8),
                    textcoords='offset points',
                    bbox=dict(boxstyle="round", fc='white', ec="black", lw=1))

    PAD = 0.02
    ax.text(0.15, 0 + PAD, "0", size=10, color='#4A2E19')
    ax.text(0.15, 0.2 + PAD, "20", size=10, color='#4A2E19')
    ax.text(0.15, 0.4 + PAD, "40", size=10, color='#4A2E19')
    ax.text(0.15, 0.6 + PAD, "60", size=10, color='#4A2E19')
    ax.text(0.15, 0.8 + PAD, "80", size=10, color='#4A2E19')
    ax.text(0.15, 1 + PAD, "100", size=10, color='#4A2E19')

    plt.suptitle('%s (%i, %s), %s | %s\nRangs de Percentile vs %s %s'
                 % (name, age, player_pos, team, season, compares, league),
                 fontsize=17,
                 fontfamily="DejaVu Sans",
                 color="#4A2E19",  # 4A2E19
                 fontweight="bold", fontname="DejaVu Sans",
                 x=0.5,
                 y=.97)

    plt.annotate(
        'Profil : %s cm, %s\n'
        'Toutes les valeurs ramenées à 90 minutes%s\nComparé à %s %s\nJoueurs avec %i+ mins\nData: Wyscout | %s\n'
        'Nombre de joueurs dans l\'échantillon : %s\nCode inspiré par @BeGriffis' % (taille, pied,
        extra_text, compares, league, mins, sig, len(dfProspect)),
        xy=(-0.15, -.05), xycoords='axes fraction',
        ha='left', va='center',
        fontsize=9, fontfamily="DejaVu Sans",
        color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
        )

    if club_image == 'y':
        ######## Club Image ########
        from PIL import Image
        image = Image.open(imgpath)
        newax = fig.add_axes([.44, .42, 0.15, 0.15], anchor='C', zorder=1)
        newax.imshow(image)
        newax.axis('off')

    #         ######## League Logo Image ########
    #         l_image = Image.open('%s/%s/%s Logo.png' %(imgpath, league,league))
    #         newax = fig.add_axes([.76,.845,0.1,0.1], anchor='C', zorder=1)
    #         newax.imshow(l_image)
    #         newax.axis('off')

    ax.set_facecolor('#fbf9f4')
    fig = plt.gcf()
    fig.patch.set_facecolor('#fbf9f4')
    #     ax.set_facecolor('#fbf9f4')
    fig.set_size_inches(12, (12 * .9))  # length, height

    if template == 'attacking':
        fig.text(
            0.8, 0.125, "Créativité", size=14, color="#4A2E19"
        )
        fig.text(
            0.8, 0.095, "Finition", size=14, color="#4A2E19"
        )
        fig.text(
            0.8, 0.065, "Mouvement de balle", size=14, color="#4A2E19"
        )
        fig.text(
            0.8, 0.035, "Défense", size=14, color="#4A2E19"
        )

        fig.patches.extend([
            plt.Rectangle(
                (0.77, 0.12), 0.025, 0.021, fill=True, color='C0',
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.77, 0.09), 0.025, 0.021, fill=True, color='C1',
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.77, 0.06), 0.025, 0.021, fill=True, color='C2',
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.77, 0.03), 0.025, 0.021, fill=True, color='C3',
                transform=fig.transFigure, figure=fig
            ),
        ])
    if template == 'defensive':
        fig.text(
            0.83, 0.155, "Défense", size=14, color="#4A2E19"
        )
        fig.text(
            0.83, 0.125, "Mouvement de balle", size=14, color="#4A2E19"
        )
        fig.text(
            0.83, 0.095, "Discipline", size=14, color="#4A2E19"
        )

        fig.patches.extend([
            plt.Rectangle(
                (0.8, 0.15), 0.025, 0.021, fill=True, color='C0',
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.8, 0.12), 0.025, 0.021, fill=True, color='C1',
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.8, 0.09), 0.025, 0.021, fill=True, color='C2',
                transform=fig.transFigure, figure=fig
            ),
        ])
    if template == 'gk':
        fig.text(
            0.83, 0.155, "Traditionnel", size=14, color="#4A2E19"
        )
        fig.text(
            0.83, 0.125, "Moderne", size=14, color="#4A2E19"
        )

        fig.patches.extend([
            plt.Rectangle(
                (0.8, 0.15), 0.025, 0.021, fill=True, color='C0',
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.8, 0.12), 0.025, 0.021, fill=True, color='C1',
                transform=fig.transFigure, figure=fig
            ),
        ])

    if save_img == 'y':
        fig.savefig("%s/%s Radar %s %s %s %s.png" % (savepath, name, season, pos, template, league), dpi=250)
    fig.show()
    ####################################################################

    #     if analysis == 'distribution':
    import matplotlib
    matplotlib.rcParams['figure.dpi'] = 75

    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    c = {'Metric': [], 'Value': [], 'Player': [], 'TrueVal': [], 'Group': []}
    distdf = pd.DataFrame(c)

    if template == 'attacking':
        var_list = [mid5, extra5, mid6, mid7, extra4,
                    fwd2, fwd1, fwd6, extra9, extra2, fwd11,
                    fwd5, extra6, mid10, mid9,
                    def1, mid12, def8, ]
    if template == 'defensive':
        var_list = [def1, def2, def3, def6, def7, extra7, def8,
                    def9, extra3, def10, def11, def12, fwd5, extra6, mid5,
                    def4, def5, extra8]
    if template == 'gk':
        var_list = [gk1, gk2, gk3, gk4, gk5, gk6, gk7,
                    gk8, gk9, gk10]

    for i in range(len(var_list)):
        n1 = var_list[i]
        n2 = df_pros[var_list[i]].values
        n2 = ((n2 - min(n2)) / (max(n2) - min(n2))) * len(n2)
        n3 = df_pros['Joueur'].values
        n4 = df_pros[var_list[i]].values
        n5 = GROUP[i]
        new = {'Metric': n1, 'Value': n2, 'Player': n3, 'TrueVal': n4, 'Group': n5}
        new_row = pd.DataFrame(new)
        distdf = distdf.append(new_row)

    distdf = distdf.reset_index(drop=True)

    if template == 'attacking':
        distdf['Metric'] = distdf['Metric'].replace({mid4: "Passes\navant tir",
                                                     mid5: "Passes décisives\nattendues (xA)",
                                                     extra5: 'xA par\npasse avant tir',
                                                     mid6: "Passes\ndé",
                                                     mid7: "2ème\npasses décisives",
                                                     extra4: 'Passes\nintelligentes',
                                                     fwd2: "npxG",
                                                     fwd1: "Buts hors\npenalties",
                                                     fwd6: "Buts/Tir\ncadré %",
                                                     extra9: 'npxG\npar tir',
                                                     extra2: "Tirs",
                                                     fwd11: 'Touches dans\nla surface',
                                                     fwd5: "Réussite des\ndribbles %",
                                                     extra6: 'Accélérations',
                                                     mid10: "Courses\nprogressives",
                                                     mid9: "Passes\nprogressives",
                                                     def1: "Actions\ndéfensives",
                                                     mid12: "Tacles & Int\n(pAdj)",
                                                     def8: 'Duels aériens\ngagnés %'
                                                     })
    if template == 'defensive':
        distdf['Metric'] = distdf['Metric'].replace({def1: 'Actions\ndéfensives',
                                                     def2: "Tacles\n(pAdj)",
                                                     def3: "Duels défensifs\ngagnés %",
                                                     def6: "Tirs contrés",
                                                     def7: "Interceptions\n(pAdj)",
                                                     extra7: 'Duels\naériens gagnés',
                                                     def8: "Duels\naériens gagnés %",
                                                     def9: "Passes\nlongues %",
                                                     extra10: "Centres",
                                                     extra3: 'Précision\ndes centres %',
                                                     def10: "Passes dé &\n2eme/3eme PD",
                                                     def11: "Passes\nprogressives",
                                                     def12: "Courses\nprogressives",
                                                     fwd5: "Réussite\ndes dribbles %",
                                                     extra6: 'Accélérations',
                                                     mid5: "Passes décisives\nattendues (xA)",
                                                     def4: "Fautes commises",
                                                     def5: "Cartons reçus",
                                                     extra8: 'Fautes subies'
                                                     })
    if template == 'gk':
        distdf['Metric'] = distdf['Metric'].replace({gk1: "Buts\nconcédés",
                                                     gk2: "Buts évités\nvs attendus",
                                                     gk3: "Tirs subis",
                                                     gk4: "Arrêts %",
                                                     gk5: "Clean Sheet %",
                                                     gk6: "Sorties",
                                                     gk7: "Duels aériens",
                                                     gk8: "Passes",
                                                     gk9: "Passes\nlongues",
                                                     gk10: "Passes\nlongues %",
                                                     })

    x = distdf['Value']
    g = list(distdf.Metric)
    df_1 = pd.DataFrame(dict(x=x, g=g))

    team_unique = list(df_1.g.unique())
    num_teams = len(team_unique)
    means_ = range(0, num_teams)
    meds_ = range(0, num_teams)
    d = {'g': team_unique, 'Mean': means_, 'Median': meds_}
    df_means = pd.DataFrame(data=d)

    for i in range(len(team_unique)):
        a = df_1[df_1['g'] == team_unique[i]]
        mu = float(a.mean())
        med = float(a.median())
        df_means['g'].iloc[i] = team_unique[i]
        df_means['Mean'].iloc[i] = mu
        df_means['Median'].iloc[i] = med
    y_order = list(df_means['g'])

    df_1 = df_1.merge(df_means, on='g', how='left')

    # add in extra columns
    df_1['Joueur'] = distdf['Player']
    df_1['Value'] = distdf['Value']
    df_1['TrueVal'] = distdf['TrueVal']
    df_1['Group'] = distdf['Group']
    player_df = df_1[df_1['Joueur'] == ws_name].reset_index(drop=True)
    line_val = player_df['Value']
    true_val = round(player_df['TrueVal'], 2)
    labels = df_1['g'].unique()

    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]
    # Initialize the FacetGrid object
    pal = sns.cubehelix_palette(num_teams, rot=2.5, light=.5)
    g = sns.FacetGrid(df_1, hue='Group', row="g", aspect=15, height=.5, row_order=y_order,
                      #                   palette=pal,
                      )

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "x",
          bw_adjust=.5, clip_on=False,
          fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5, )

    # draw each distribution's line
    for ax, val, COLORS, tval in zip(g.axes.flat, line_val, COLORS, true_val):
        ax.axvline(x=val, color='white', linestyle='solid', ymin=0, ymax=.7, lw=4)
        ax.axvline(x=val, color=COLORS, linestyle='solid', ymin=0, ymax=.7, lw=2)
        ax.text(max(df_1['Value']) + ((max(df_1['Value']) - min(df_1['Value'])) / 6)-30, 0.005, tval, color=COLORS,
                fontweight='bold')

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]
    #     path_eff = [path_effects.Stroke(linewidth=.5, foreground='white'), path_effects.Normal()]
    for ax, val, COLORS, lab in zip(g.axes.flat, line_val, COLORS, labels):
        print(lab)
        ax.text(min(df_1['Value']) - ((max(df_1['Value']) - min(df_1['Value'])) / 3), 0.005, lab, color='w',
                fontweight='bold', fontsize=9)
        ax.text(min(df_1['Value']) - ((max(df_1['Value']) - min(df_1['Value'])) / 3)+42, 0.002, lab, color=COLORS,
                fontweight='bold', fontsize=10)

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.1)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], xticks=[], ylabel='', xlabel='')
    g.despine(bottom=True, left=True)

    fig = plt.gcf()
    fig.patch.set_facecolor('#fbf9f4')
    fig.set_size_inches(7, 15)

    plt.suptitle('%s - %s ans - %s | %s'
                 % (name, age, team,  season),
                 fontsize=13,
                 fontfamily="DejaVu Sans",
                 color="#4A2E19",  # 4A2E19
                 fontweight="bold", fontname="DejaVu Sans",
                 x=0.5,
                 y=1.)

    plt.annotate(
        'Toutes les valeurs ramenées à 90 minutes%s, %s %s, %i+ mins\nData: Wyscout | %s | Code inspiré par @BeGriffis' % (
        extra_text, compares, league, mins, sig),
        xy=(0, -.6), xycoords='axes fraction',
        ha='left', va='center',
        fontsize=7, fontfamily="DejaVu Sans",
        color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
        )

    if template == 'attacking':
        plt.annotate("Valeur /90 min",
                     xy=(.85, 20.6), xycoords='axes fraction',
                     ha='left', va='center',
                     fontsize=10, fontfamily="DejaVu Sans",
                     color="#4A2E19", fontweight="bold", fontname="DejaVu Sans",
                     )
        plt.annotate("Métrique",
                     xy=(0, 20.6), xycoords='axes fraction',
                     ha='left', va='center',
                     fontsize=10, fontfamily="DejaVu Sans",
                     color="#4A2E19", fontweight="bold", fontname="DejaVu Sans",
                     )
    if template == 'defensive':
        plt.annotate("Valeur /90 min",
                     xy=(.85, 16), xycoords='axes fraction',
                     ha='left', va='center',
                     fontsize=8, fontfamily="DejaVu Sans",
                     color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                     )
        plt.annotate("Métrique",
                     xy=(0, 16), xycoords='axes fraction',
                     ha='left', va='center',
                     fontsize=8, fontfamily="DejaVu Sans",
                     color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                     )
    if template == 'gk':
        plt.annotate("Valeur /90 min",
                     xy=(.85, 9), xycoords='axes fraction',
                     ha='left', va='center',
                     fontsize=15, fontfamily="DejaVu Sans",
                     color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                     )
        plt.annotate("Métrique",
                     xy=(0, 9), xycoords='axes fraction',
                     ha='left', va='center',
                     fontsize=15, fontfamily="DejaVu Sans",
                     color="#4A2E19", fontweight="regular", fontname="DejaVu Sans",
                     )

    # if club_image == 'y':
    #     from PIL import Image
    #     image = Image.open(imgpath)
    #     newax = fig.add_axes([.8, -.03, 0.08, 0.08], anchor='C', zorder=1)
    #     newax.imshow(image)
    #     newax.axis('off')
    # plt.show()

scout_report(ws_datapath = 'C:/Users/Matis/Documents/Sorare_Data/Graph_Building/davidcosta.csv',  # Make sure your csv is UTF-8 Encoded
             savepath = 'C:/Users/Matis/Documents/Sorare_Data/Graph_Building/Radars',  # OPTIONAL: This will be the location the radar saves to (if you have the save_img variable as y below)
             imgpath = 'C:/Users/Matis/Documents/Sorare_Data/Graph_Building/costa.png',  # OPTIONAL: if you don't add an image, comment this line out
             league = 'Top 5 européen',  # name of your league (make sure your dataset league name and image folder league name match)
             season = '2022-2023',  # for example: 2022 for summer leagues' seasons, 21-22 for winter leagues
             xtra = ' current',  # this is for the ws_datapath. I have '' for finished seasons, and ' current' for in-progress ones.
             template = 'attacking',  #  OPTIONS: attacking, defensive, gk   # This determines which radar template you want. I only have 3 right now, am looking into making more position-specific ones
             pos_buckets = 'mult',   # OPTIONS: single, mult (if you want a sinlg wyscout position like CF/LCB/LAMF or if the position contains something like CB/AMF/etc, then choose single)
             pos = 'Midfielder Advanced',  # See the 'mult position options' description below for the options (after the ###)
             player_pos = 'Milieu offensif',  # this will be included in the title, showing the player's name, age, and position you put here
             compares = 'Milieux offensifs du',   # this adds the comparison group in the notes at the bottom. essentially, "compared to League [compares]..."
             mins = 1000,  # minimum minutes played filter
             name = 'David Costa',  # Actual player name (because Wyscout doesn't use full names, but we should)
             ws_name = 'David Costa',  # Wyscout's name they use for the player
             team = 'RC Lens',  # The player's club. Variable in Wyscout I use is 'Club within selected timeframe'
             age = 22,  # Player age
             taille = '168',
             pied = 'Droitier',
             sig = 'Twitter: @datascout_',  # Signature you want to add to the notes at the bottom
             club_image = 'y',  # if you want a club & league logo on the radar, make sure you have the imgpath variable filled out
             save_img = 'y',  # this will save the radar automatically, not the distribution chart. That will need to be saved by right-clicking it
             extra_text = '',  # Any extra text you want to add to the notes at the bottom. I usually put ' | Data final for 21-22' or ' | Data as of 9/2/22' for example. Make sure people finding this chart in the future know if it's got an expiration date, essentially.
            )