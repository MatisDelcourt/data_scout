import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager, add_image
import pandas as pd
from scipy import stats
from PIL import Image

def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    with open('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/carac_names_fr.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val
    return carac_dict[carac]

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))

df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/dc_top5.csv', header=0)

## Filtering for players with more than 10 npxG+xA, 1000 mins and 1 goal
df_filter = (df['Minutes jouées'] >= 1000)
player_filter = df[df_filter]


players_final = pd.DataFrame()

player_name = 'L. Balerdi'

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jouées']

players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']
players_final['DefWons'] = player_filter['Duels défensifs gagnés. %']
players_final['TklPAdj'] = player_filter['Tacles glissés PAdj']
players_final['IntPAdj'] = player_filter['Interceptions PAdj']
players_final['AerWons'] = player_filter['Duels aériens gagnés. %']
players_final['Blk'] = player_filter['Tirs bloqués par 90']

players_final['AccPasses'] = player_filter['Passes précises. %']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']
players_final['LgPass'] = player_filter['Passes longues par 90']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Forward'] = player_filter['Passes avant par 90']
players_final['KP'] = player_filter['Passes quasi décisives par 90']
# players_final['ShAst'] = player_filter['Passes décisives avec tir par 90']
players_final['Run'] = player_filter['Courses progressives par 90']
# players_final['Recept'] = player_filter['Passes réceptionnées par 90']

players_final['PreAst'] = player_filter['Secondes passes décisives par 90'] + player_filter['Troisièmes passes décisives par 90']

players_final['TouchBox'] = player_filter['Touches de balle dans la surface de réparation sur 90']
# players_final['Acc'] = player_filter['Accélérations par 90']
# players_final['Fouled'] = player_filter['Fautes subies par 90']
players_final['BoxPasses'] = player_filter['Passes vers la surface de réparation par 90']

players_final['xA'] = player_filter['xA par 90']
players_final['xG'] = player_filter['xG par 90']
players_final['Head'] = player_filter['Buts de la tête par 90']
players_final['SuccOff'] = player_filter['Attaques réussies par 90']
players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Cross'] = player_filter['Centres par 90']
players_final['npG'] = player_filter['Buts hors penalty par 90']

players_final['DS'] = player_filter['Buts hors penalty par 90'] + player_filter['Passes décisives par 90']
players_final['Shots'] = player_filter['Tirs par 90']
players_final['ShCad%'] = player_filter['Tirs à la cible. %']

players_filter = ((players_final['Player'] == player_name))
player_of_i = players_final[players_filter]
print(player_of_i)

carac_list = ['xG', 'xA',
              'KP', 'Forward', 'AccPasses', 'Third', 'LgPass', 'Through', 'Prog',
              'SuccDef', 'TklPAdj', 'DefWons', 'IntPAdj', 'AerWons', 'Blk']

values_list = []
for i in carac_list:
    carac1 = list(players_final[i])
    carac_player = list(player_of_i[i])
    centile = stats.percentileofscore(carac1, carac_player)
    values_list.append(int(centile))

carac_names = []
for i in carac_list:
    carac_new = carac_abbreviation_to_real_name(i)
    if len(carac_new.split(" ")) >= 3:
        carac_new = (" ").join(carac_new.split(" ")[:2]) + "\n" + (" ").join(carac_new.split(" ")[2:])
    carac_names.append(carac_new)
# for i in carac_list:
#     carac_new = carac_abbreviation_to_real_name(i)
#     carac_names.append(carac_new)

# instantiate PyPizza class
baker = PyPizza(
    params=carac_names,                  # list of parameters
    background_color="#EBEBE9",     # background color
    straight_line_color="#222222",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    last_circle_color="#222222",    # color of last circle
    other_circle_ls="-.",           # linestyle for other circles
    other_circle_lw=1               # linewidth for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values_list,                     # list of values
    # compare_values=values_2,    # comparison values
    figsize=(8, 8),             # adjust figsize according to your need
    kwargs_slices=dict(
        facecolor="#2faee0", edgecolor="#222222",
        zorder=2, linewidth=1
    ),                          # values to be used when plotting slices
    # kwargs_compare=dict(
    #     facecolor="#FF9300", edgecolor="#222222",
    #     zorder=2, linewidth=1,
    # ),
    kwargs_params=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, va="center"
    ),                          # values to be used when adding parameter
    kwargs_values=dict(
        color="#ffffff", fontsize=12,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="#000000",
            boxstyle="round,pad=0.2", lw=1
        )
    ),                          # values to be used when adding parameter-values labels
    kwargs_compare_values=dict(
        color="#000000", fontsize=12, fontproperties=font_normal.prop, zorder=3,
        bbox=dict(edgecolor="#000000", facecolor="#FF9300", boxstyle="round,pad=0.2", lw=1)
    ),                          # values to be used when adding parameter-values labels
)

# add title
fig_text(
    0.515, 0.99, "<Pau López>", size=17, fig=fig,
    highlight_textprops=[{"color": '#000000'}],
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add subtitle
fig.text(
    0.515, 0.942,
    "vs Gardiens du top 5 européen | 2021/2022",
    size=15,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\lopez.png")
ax_image = add_image(
    image, fig, left=0.035, bottom=0.825, width=0.15, height=0.15
)

# add credits
CREDIT_1 = "Visualisation réalisée par Data'Scout @datascoutsorare"
CREDIT_2 = "Données issues de WyScout, Data /90 min, 2000+ minutes"
CREDIT_3 = "Inspiré par: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"


fig.text(
    0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=7,
    fontproperties=font_italic.prop, color="#000000",
    ha="right"
)

# CREDIT_4 = "Top 7 européen : Premier League, Liga, Bundesliga, Serie A, \nLigue 1, Liga Bwin, Eredivisie"
#
#
# fig.text(
#     0.01, 0.001, f"{CREDIT_4}\n", size=7,
#     fontproperties=font_italic.prop, color="#000000",
#     ha="left"
# )

fig.savefig("GraphPizza_%s_Solo.png" % (player_name), dpi=220)

