
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

image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\logo png.png")

##############################################################################
# Dark Theme
# ----------
# Below is an example code for dark theme.

df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/kvara.csv', header=0)
print(df)

## Filtering
df_filter = (df['Minutes jouées'] >= 100)
player_filter = df[df_filter]

players_final = pd.DataFrame()

player_name = 'K. Kvaratskhelia'

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jouées']
players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']
players_final['DefWons'] = player_filter['Duels défensifs gagnés. %']
players_final['TklPAdj'] = player_filter['Tacles glissés PAdj']
players_final['IntPAdj'] = player_filter['Interceptions PAdj']

players_final['Tkl+Int'] = players_final['TklPAdj'] + players_final['IntPAdj']

players_final['AerWons'] = player_filter['Duels aériens gagnés. %']
# players_final['Blk'] = player_filter['Tirs bloqués par 90']

players_final['Pass'] = player_filter['Passes par 90']
players_final['AccPasses'] = player_filter['Passes précises. %']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']
players_final['LgPass'] = player_filter['Passes longues par 90']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Forward'] = player_filter['Passes avant par 90']
players_final['Lateral'] = player_filter['Passes latérales par 90']
players_final['KP'] = player_filter['Passes quasi décisives par 90']
players_final['Smart'] = player_filter['Passes judicieuses par 90']
players_final['ShAst'] = player_filter['Passes décisives avec tir par 90']
players_final['Run'] = player_filter['Courses progressives par 90']
players_final['Recept'] = player_filter['Passes réceptionnées par 90']

players_final['PreAst'] = player_filter['Secondes passes décisives par 90'] + player_filter['Troisièmes passes décisives par 90']

players_final['TouchBox'] = player_filter['Touches de balle dans la surface de réparation sur 90']
players_final['Acc'] = player_filter['Accélérations par 90']
players_final['Fouled'] = player_filter['Fautes subies par 90']
players_final['BoxPasses'] = player_filter['Passes vers la surface de réparation par 90']

players_final['xA'] = player_filter['xA par 90']
players_final['xG'] = player_filter['xG par 90']
players_final['Head'] = player_filter['Buts de la tête par 90']
players_final['SuccOff'] = player_filter['Attaques réussies par 90']
players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Cross'] = player_filter['Centres par 90']
players_final['npG'] = player_filter['Buts hors penalty par 90']
players_final['Ast'] = player_filter['Passes décisives par 90']

players_final['DS'] = player_filter['Buts hors penalty par 90'] + player_filter['Passes décisives par 90']
players_final['Shots'] = player_filter['Tirs par 90']
players_final['ShCad%'] = player_filter['Tirs à la cible. %']
players_final['Taux'] = player_filter['Taux de conversion but/tir']

print(players_final)

players_filter = ((players_final['Player'] == player_name))
player_of_i = players_final[players_filter]
print(player_of_i)

carac_list = ['TouchBox', 'xG', 'xA', 'Drib', 'Shots', 'KP', 'Cross', 'ShAst']

values_list = []
# Calcul des centiles pour chaque stat
for i in carac_list:
    carac1 = list(players_final[i])
    carac_player = list(player_of_i[i])
    centile = stats.percentileofscore(carac1, carac_player)
    values_list.append(int(centile))

carac_names = []
# Récupération du nom de la stat
for i in carac_list:
    carac_new = carac_abbreviation_to_real_name(i)
    if len(carac_new.split(" ")) >= 3:
        carac_new = (" ").join(carac_new.split(" ")[:2]) + "\n" + (" ").join(carac_new.split(" ")[2:])
    carac_names.append(carac_new[:-1])


# color for the slices and text
# Nombre de parties pour chaque catégorie : attaque - possession - défense
slice_colors = ["#12A0D7"] + ["#ffffff"] + ["#12A0D7"] + ["#ffffff"] + ["#12A0D7"] + ["#ffffff"] + ["#12A0D7"] + ["#ffffff"]
text_colors = ["#000000"] * 8

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
        color="#F2F2F2", fontsize=13, va="center"
    ),                               # values to be used when adding parameter labels
    kwargs_values=dict(
        color="#F2F2F2", fontsize=11, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                                # values to be used when adding parameter-values labels
)

# # add title
# fig.text(
#     0.515, 0.975, "Brenden Aa - Red Bull Salzburg - 21 ans", size=16, weight='bold',
#     ha="center", color="#df003c"
# )

# add subtitle
fig.text(
    0.515, 0.955,
    "Rang de Percentile vs Ailiers du top 5 européen",
    size=13,
    ha="center", color="#12A0D7", weight='bold'
)


# add credits
CREDIT_1 = "Visualisation réalisée par Data'Scout @datascoutsorare"
CREDIT_2 = "Données issues de WyScout : Data/90 min, Tacles et Interceptions ajustés à la possession"
CREDIT_3 = "Inspiré par: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


fig.text(
    0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=6, color="#ffffff",
    ha="right"
)

CREDIT_4 = "Uniquement les joueurs avec 100+ minutes joués en 2021-2022"
CREDIT_5 = "Ligues européennes de l'échantillon : Top 5 européen"
fig.text(
    0.01, 0.005, f"{CREDIT_4}\n{CREDIT_5}", size=6, color="#ffffff",
    ha="left"
)

# add image
ax_image = add_image(
    image, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
)   # these values might differ when you are plotting

plt.show()
fig.savefig("Graph_%s_PizzaFlash.png" % (player_name), dpi=220)
