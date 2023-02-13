import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from mplsoccer import PyPizza, add_image, FontManager
from scipy import stats
from utils import carac_abbreviation_to_real_name, choose_carac_and_player

def pizza_graph(df, name, carac, minimum_minutes, player_path, team_path, color1, color2, color3, color_background, bdd, année, slices):

        image_joueur = Image.open(player_path)
        image_equipe = Image.open(team_path)

        df_interet, df_all = choose_carac_and_player(df, name, carac, minimum_minutes)
        df_all = df_all.fillna(0)
        carac_list = carac
        age = df_interet["Age"].values[0]
        club = df_interet["Squad"].values[0]

        values_list = []

        # Calcul des centiles pour chaque stat
        for i in carac_list:
                carac1 = list(df_all[i])
                carac_player = list(df_interet[i])
                centile = stats.percentileofscore(carac1, carac_player)
                values_list.append(int(centile))

        carac_names = []
        # Récupération du nom de la stat
        for i in carac_list:
                carac_new = carac_abbreviation_to_real_name(i)
                if len(carac_new.split(" ")) >= 3:
                        carac_new = (" ").join(carac_new.split(" ")[:2]) + "\n" + (" ").join(carac_new.split(" ")[2:])
                carac_names.append(carac_new)

        text_color="#000000"
        if color_background=="#000000":
                text_color = "#FFFFFF"

        slice_colors = [color1] * slices[0] + \
                       [color2] * slices[1] + \
                       [color3] * slices[2]
        text_colors = [text_color] * len(carac_list)

        # instantiate PyPizza class

        # instantiate PyPizza class
        baker = PyPizza(
                params=carac_names,  # list of parameters
                background_color="#FED0BB",  # background color #222222
                straight_line_color="#000000",  # color for straight lines
                straight_line_lw=1,  # linewidth for straight lines
                last_circle_color="#000000",  # color for last line
                last_circle_lw=1,  # linewidth of last circle
                other_circle_lw=0,  # linewidth for other circles
                inner_circle_size=20  # size of inner circle
        )

        # plot pizza
        fig, ax = baker.make_pizza(
                values_list,  # list of values
                figsize=(10, 12),
                param_location=107,  # adjust the figsize according to your need
                color_blank_space="same",  # use the same color to fill blank space
                slice_colors=slice_colors,  # color for individual slices
                value_colors=text_colors,  # color for the value-text
                value_bck_colors=slice_colors,  # color for the blank spaces
                blank_alpha=0.4,  # alpha for blank-space colors
                kwargs_slices=dict(
                        edgecolor="#000000", zorder=2, linewidth=1
                ),  # values to be used when plotting slices
                kwargs_params=dict(
                        color="#000000", fontsize=14,
                        # fontproperties=font_normal.prop,
                        va="center"
                ),  # values to be used when adding parameter labels
                kwargs_values=dict(
                        color="#000000", fontsize=13,
                        # fontproperties=font_normal.prop,
                        zorder=3,
                        bbox=dict(
                                edgecolor="#000000", facecolor="cornflowerblue",
                                boxstyle="round,pad=0.2", lw=1
                        )
                )  # values to be used when adding parameter-values labels
        )

        # add title

        fig.text(
                0.515, 0.96, f"{name} - {club} - {age} ans", size=18,
                ha="center", color="#000000"
        )

        # add credits
        CREDIT_1 = bdd
        CREDIT_2 = "Data/90mins, joueurs avec >" + str(minimum_minutes) + " - " + str(année)
        CREDIT_3 = "Par @datascout_ inspiré par: @FootballSlices. Source : Wyscout"


        fig.text(
                0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=10, color="#000000",
                ha="right"
        )

        carac_exemple = (" ").join(carac_list[0].split(" ")[:-2])

        CREDIT_4 = "Le percentile représente le classement de " + str(name) + " par rapport\naux joueurs à son poste par exemple " + \
                   str(values_list[0]) + " en " + str(carac_exemple) + "\nsignifie qu'il a plus de " + \
                   str(carac_exemple) + " que " + str(values_list[0]) + "% des ailiers d'Europe."

        fig.text(
                0.01, -0.01, f"{CREDIT_4}\n", size=10, color="#000000",
                ha="left"
        )

        # add text
        fig.text(
                0.85, 0.905, "Attaque \nPossession \nDéfense", size=18, color="#000000"
        )

        # add rectangles
        fig.patches.extend([
                plt.Rectangle(
                        (0.82, 0.96), 0.025, 0.021, fill=True, color="#FCB9B2",
                        transform=fig.transFigure, figure=fig
                ),
                plt.Rectangle(
                        (0.82, 0.93), 0.025, 0.021, fill=True, color="#B23A48",
                        transform=fig.transFigure, figure=fig
                ),
                plt.Rectangle(
                        (0.82, 0.90), 0.025, 0.021, fill=True, color="#8C2F39",
                        transform=fig.transFigure, figure=fig
                ),
        ])

        # add image
        ax_image = add_image(
                image_joueur, fig, left=0.462, bottom=0.445, width=0.10, height=0.10
        )  # these values might differ when you are plotting

        # add image
        ax_image = add_image(
                image_equipe, fig, left=0.02, bottom=0.775, width=0.20, height=0.20
        )  # these values might differ when you are plotting

        filename = "output_files/" + name + "/" + name + "_pizza.jpg"

        fig.savefig(filename, dpi=300, bbox_inches='tight')

        print("Pizza saved at", filename)

