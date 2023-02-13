"""BONJOUR TIPICS
Ce que tu dois faire pour faire fonctionner ce TAP-IN :
1/ Ligne 22 tu indique l'endroit où tu as placé le fichier carac_names.csv
2/ Ligne 30 tu indique l'endroit où tu as placé le fichier csv contenant les données que tu étudies
3/ Ligne 33 tu peux modifier ça pour prendre les joueurs ayant plus de X minutes seulement (ici X = 800, une bonne valeur c'est genre 2000)
4/ Ligne 66 tu indiques le nom du joueur que tu veux étudier, de la même manière que la façon dont il est écrit dans le .csv que tu étudies
5/ Ligne 70 tu choisis les caractéristiques que tu veux utiliser.
6/ Ligne 94 et 96 tu choisis la couleur de la pizza. En ce moment on essaye d'alterner les couleurs du club.
7/ Ligne 121, 124, 129 et 133 tu choisis les différentes couleurs des bordures et du texte autour de la pizza
8/ Ligne 142 tu changes le titre du document
9/ Ligne 161, 162, 163 tu indiques le chemin à des différences images que tu utilises. Image c'est notre logo, Image2 c'est la photo du joueur et image3 c'est le logo de son club
"""
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from mplsoccer import PyPizza, add_image
from scipy import stats

def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    #Ici indique l'endroit où tu as placé le fichier carac_names.csv
    with open('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/carac_names.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val
    return carac_dict[carac]

#Ici indique l'endroit où tu as placé le fichier csv contenant les données que tu étudies
df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/gakpo.csv', header=0)

#Tu peux modifier ça pour prendre les joueurs ayant plus de X minutes seulement (ici X = 800, une bonne valeur c'est genre 2000)
df_filter = (df['Minutes jouées'] >= 2000)
player_filter = df[df_filter]
players_final = pd.DataFrame()

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jouées']
players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']
players_final['Tkl'] = player_filter['Tacles glissés PAdj']
players_final['Int'] = player_filter['Interceptions PAdj']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']
players_final['LgPass'] = player_filter['Passes longues par 90']
players_final['ShAst'] = player_filter['Passes décisives avec tir par 90']
players_final['xA'] = player_filter['xA par 90']
players_final['xG'] = player_filter['xG par 90']
players_final['PenAreaTouches'] = player_filter['Touches de balle dans la surface de réparation sur 90']
players_final['SuccOff'] = player_filter['Attaques réussies par 90']
players_final['Run'] = player_filter['Courses progressives par 90']
players_final['Shots'] = player_filter['Tirs par 90']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Fouls'] = player_filter['Fautes subies par 90']
players_final['FoulsDone'] = player_filter['Fautes par 90']
players_final['Crosses'] = player_filter['Centres par 90']
players_final['Drib'] = player_filter['Dribbles par 90']
players_final['DuelOff'] = player_filter['Duels offensifs par 90']
players_final['Acc'] = player_filter['Accélérations par 90']
players_final['PasseRec'] = player_filter['Passes réceptionnées par 90']
players_final['PasseProf'] = player_filter['Réalisations en profondeur par 90']
players_final['Aerien'] = player_filter['Duels aériens par 90']
players_final['Header'] = player_filter['Buts de la tête par 90']

#Ici tu indiques le nom du joueur que tu veux étudier, de la même manière que la façon dont il est écrit dans le .csv que tu étudies
players_filter = ((players_final['Player'] == 'C. Gakpo'))
player_of_i = players_final[players_filter]

#Ici tu choisis les caractéristiques que tu veux utiliser. La liste des caractéristiques dispo facilement est juste au dessus genre SuccOff = Attaques réussies par 90
carac_list = ['OffWon', 'xA', 'Drib', 'PasseProf', 'Prog', 'PenAreaTouches', 'Crosses' , 'xG', 'SuccOff', 'Acc']

values_list = []
# Calcul des centiles pour chaque stat
for i in carac_list:
    carac1 = list(players_final[i])
    carac_player = list(player_of_i[i])
    centile = stats.percentileofscore(carac1, carac_player)
    if i =="FoulsDone":
        values_list.append(100 - int(centile))
    else:
        values_list.append(int(centile))

carac_names = []
# Récupération du nom de la stat
for i in carac_list:
    carac_new = carac_abbreviation_to_real_name(i)
    if len(carac_new.split(" ")) >= 3:
        carac_new = (" ").join(carac_new.split(" ")[:2]) + "\n" + (" ").join(carac_new.split(" ")[2:])
    carac_names.append(carac_new)


# color for the slices and text
#Ici tu choisis la couleur de la pizza. En ce moment on essaye d'alterner les couleurs du club.
slice_colors = ["#DA291C"] + ["#FBE122"] + ["#DA291C"] + ["#FBE122"] + ["#DA291C"] + ["#FBE122"] + ["#DA291C"] + ["#FBE122"] + ["#DA291C"] + ["#FBE122"]
#Ici les couleurs du texte
text_colors = ["#000000"] * 10 # + ["#F2F2F2"] * 5

# instantiate PyPizza class
baker = PyPizza(
    params=carac_names,                  # list of parameters
    background_color="#111C33",     # background color
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_color="#000000",    # color for last line
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
    inner_circle_size=20            # size of inner circle
)

# plot pizza
fig, ax = baker.make_pizza(
    values_list,                          # list of values
    figsize=(30, 25),                # adjust the figsize according to your need
    param_location=113,
    color_blank_space="same",        # use the same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.7,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#000000", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
        color="#FFFFFF", fontsize=20,
        #fontproperties=font_normal.prop,
        va="center"
    ),                               # values to be used when adding parameter labels
    kwargs_values=dict(
        color="#000000", fontsize=20,
        #fontproperties=font_normal.prop,
        zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values labels
)

#Ici tu changes le titre du document
fig.text(
    0.525, 0.97,
    "Percentile de C. Gakpo vs Ailiers des 5 grands championnats | 365 derniers jours",
    size=20,
    ha="center", color="#ffffff"
)


# add credits
CREDIT_1 = "Visualisation réalisée par Data'Scout @datascout_"
CREDIT_2 = "Données par 90 min issues de WyScout."
CREDIT_3 = "Inspiré par: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


fig.text(
    0.85, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=7, color="#ffffff",
    ha="right"
)

#Ici tu indiques le chemin à des différences images que tu utilises. Image c'est notre logo, Image2 c'est la photo du joueur et image3 c'est le logo de son club
# Charge l'image
# image = Image.open("E:/Documents/JTM GRAPHICS/Cible DS Blanche.png")
# image2 = Image.open("E:/Documents/JTM GRAPHICS/TAP-IN/gakpo.jpg")
# image3 = Image.open("E:/Documents/JTM GRAPHICS/TAP-IN/manu.png")
# 
# #ici tu peux choisir la position des images en modifiant les valeurs de left et bottom
# # add image
# ax_image = add_image(
#     image, fig, left=0.4548, bottom=0.4385, width=0.115, height=0.115
# )   # these values might differ when you are plotting
# 
# ax_image = add_image(
#     image2, fig, left=0.1748, bottom=0.7385, width=0.20, height=0.20
# )
# ax_image = add_image(
#     image3, fig, left=0.6768, bottom=0.7385, width=0.21, height=0.21
# )


plt.show()