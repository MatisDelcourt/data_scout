"""
==============================
Dark Theme Pizza (Percentiles)
==============================

* Author: `slothfulwave612 <https://twitter.com/slothfulwave612>`_

* ``mplsoccer``, ``py_pizza`` module helps one to plot pizza charts in a few lines of code.

* The design idea is inspired by `Tom Worville <https://twitter.com/Worville>`_, \
`Football Slices <https://twitter.com/FootballSlices>`_ and \
`Soma Zero FC <https://twitter.com/somazerofc>`_

* We have re-written `Soumyajit Bose's <https://twitter.com/Soumyaj15209314>`_  pizza chart code \
to enable greater customisation.

Here we plot a pizza chart with a dark theme.
"""

from urllib.request import urlopen

import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from mplsoccer import PyPizza, add_image, FontManager
from scipy import stats

def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    with open('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/carac_names_fr.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val
    return carac_dict[carac]

##############################################################################
# Load some fonts
# ---------------
# We will use mplsoccer's FontManager to load some fonts from Google Fonts.
# We borrowed the FontManager from the excellent
# `ridge_map library <https://github.com/ColCarroll/ridge_map>`_.

font_normal = FontManager(("https://github.com/openmaptiles/fonts/blob/master/open-sans/OpenSans-Regular.ttf"))
font_italic = FontManager(("https://github.com/openmaptiles/fonts/blob/master/open-sans/OpenSans-Italic.ttf"))
font_bold = FontManager(("https://github.com/openmaptiles/fonts/blob/master/open-sans/OpenSans-Bold.ttf"))

##############################################################################
# Load Image
# ----------
# Load a cropped image of Frenkie de Jong.

image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\zerrouki.png")

##############################################################################
# Dark Theme
# ----------
# Below is an example code for dark theme.

df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/zerrouki.csv', header=0)
print(df)

## Filtering
df_filter = (df['Minutes jou??es  '] >= 1000)
player_filter = df[df_filter]

players_final = pd.DataFrame()

player_name = 'R. Zerrouki'

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jou??es  ']
players_final['SuccDef'] = player_filter['Actions d??fensives r??ussies par 90']
players_final['DefWons'] = player_filter['Duels d??fensifs gagn??s. %']
players_final['TklPAdj'] = player_filter['Tacles gliss??s PAdj']
players_final['IntPAdj'] = player_filter['Interceptions PAdj']

players_final['Tkl+Int'] = players_final['TklPAdj'] + players_final['IntPAdj']

players_final['AerWons'] = player_filter['Duels a??riens gagn??s. %']
players_final['Blk'] = player_filter['Tirs contr??s par 90']

players_final['Pass'] = player_filter['Passes par 90']
players_final['AccPasses'] = player_filter['Passes pr??cises. %']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']
players_final['LgPass'] = player_filter['Passes longues par 90']
players_final['Through'] = player_filter['Passes p??n??trantes par 90']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Forward'] = player_filter['Passes avant par 90']
players_final['Lateral'] = player_filter['Passes lat??rales par 90']
players_final['KP'] = player_filter['Passes quasi d??cisives par 90']
players_final['Smart'] = player_filter['Passes judicieuses par 90']
players_final['ShAst'] = player_filter['Passes d??cisives avec tir par 90']
players_final['Run'] = player_filter['Courses progressives par 90']
players_final['Recept'] = player_filter['Passes r??ceptionn??es par 90']
players_final['Deep'] = player_filter['R??alisations en profondeur par 90']

players_final['PreAst'] = player_filter['Secondes passes d??cisives par 90'] + player_filter['Troisi??mes passes d??cisives par 90']

players_final['TouchBox'] = player_filter['Touches de balle dans la surface de r??paration sur 90']
players_final['Acc'] = player_filter['Acc??l??rations par 90']
players_final['Fouled'] = player_filter['Fautes subies par 90']
players_final['BoxPasses'] = player_filter['Passes vers la surface de r??paration par 90']

players_final['xA'] = player_filter['xA par 90']
players_final['xG'] = player_filter['xG par 90']
players_final['Head'] = player_filter['Buts de la t??te par 90']
players_final['SuccOff'] = player_filter['Attaques r??ussies par 90']
players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Cross'] = player_filter['Centres par 90']
players_final['npG'] = player_filter['Buts hors penalty par 90']
players_final['Ast'] = player_filter['Passes d??cisives par 90']

players_final['DS'] = player_filter['Buts hors penalty par 90'] + player_filter['Passes d??cisives par 90']
players_final['xDS'] = player_filter['xG par 90'] + player_filter['xA par 90']
players_final['DiffA'] = players_final['xA'] - players_final['Ast']
players_final['DiffB'] = players_final['xG'] - players_final['npG']
players_final['Shots'] = player_filter['Tirs par 90']
players_final['ShCad%'] = player_filter['Tirs ?? la cible. %']
players_final['Taux'] = player_filter['Taux de conversion but/tir']

print(players_final)

players_filter = ((players_final['Player'] == player_name))
player_of_i = players_final[players_filter]
print(player_of_i)

carac_list = ['DS', 'xG', 'xA', 'Shots',
              'AccPasses', 'Pass', 'Third', 'BoxPasses', 'Prog',
              'SuccDef', 'IntPAdj', 'AerWons', 'TklPAdj', 'DefWons']

values_list = []
# Calcul des centiles pour chaque stat
for i in carac_list:
    carac1 = list(players_final[i])
    carac_player = list(player_of_i[i])
    centile = stats.percentileofscore(carac1, carac_player)
    print(i)
    values_list.append(int(centile))

carac_names = []
# R??cup??ration du nom de la stat
for i in carac_list:
    carac_new = carac_abbreviation_to_real_name(i)
    if len(carac_new.split(" ")) >= 3:
        carac_new = (" ").join(carac_new.split(" ")[:2]) + "\n" + (" ").join(carac_new.split(" ")[2:])
    carac_names.append(carac_new[:-1])


# color for the slices and text
# Nombre de parties pour chaque cat??gorie : attaque - possession - d??fense
# slice_colors = ["#b00000"] * 6 + ["#eab900"] * 7 + ["#007500"] * 2
couleur1 ="#FE354B" # "#DB324D"
couleur2 ="#E7E4E4" # "#EDF2F4"
couleur3 ="#6A6262"
slice_colors = [couleur1] * 4 + [couleur2] * 5 + [couleur3] * 5
text_colors = ["#000000"] * 14 # + ["#F2F2F2"] * 5

# instantiate PyPizza class
baker = PyPizza(
    params=carac_names,                  # list of parameters
    background_color="#222222",     # background color
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
    figsize=(8, 8.5),                # adjust the figsize according to your need
    color_blank_space="same",        # use the same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#000000", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
        color="#F2F2F2", fontsize=9, va="center"
    ),                               # values to be used when adding parameter labels
    kwargs_values=dict(
        color="#F2F2F2", fontsize=11, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values labels
)

# add title
fig.text(
    0.515, 0.975, "Ramiz Zerrouki - 24 ans - FC Twente", size=14, weight='bold',
    ha="center", color="#ffffff"
)

# add subtitle
fig.text(
    0.515, 0.955,
    "Rang de Percentile vs Milieux centraux du top 7 europ??en | 2022/2023",
    size=9.5,
    ha="center", color="#ffffff"
)


# add credits
CREDIT_1 = "Visualisation r??alis??e par Data'Scout @datascout_"
CREDIT_2 = "Donn??es issues de WyScout : Data/90 min, Tacles et Interceptions ajust??s ?? la possession"
CREDIT_3 = "Inspir?? par: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


fig.text(
    0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=6, color="#ffffff",
    ha="right"
)

CREDIT_4 = "Uniquement les joueurs avec 1000+ minutes jou??s en 2022-2023"
# CREDIT_5 = "Ligues europ??ennes de l'??chantillon : Top 5 europ??en, Pays-Bas, Autriche, Portugal"
fig.text(
    0.01, 0.005, f"{CREDIT_4}", size=6, color="#ffffff",
    ha="left"
)


# add text
fig.text(
    0.34, 0.9275, "Attaque       Possession     D??fense", size=14, color="#F2F2F2"
)

# add rectangles
fig.patches.extend([
    plt.Rectangle(
        (0.31, 0.9225), 0.025, 0.021, fill=True, color=couleur1,
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.462, 0.9225), 0.025, 0.021, fill=True, color=couleur2,
        transform=fig.transFigure, figure=fig
    ),
    plt.Rectangle(
        (0.632, 0.9225), 0.025, 0.021, fill=True, color=couleur3,
        transform=fig.transFigure, figure=fig
    ),
])

# add image
ax_image = add_image(
    image, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
)   # these values might differ when you are plotting

plt.show()
fig.savefig("Graph_%s_Pizza.png" % (player_name), dpi=220)
