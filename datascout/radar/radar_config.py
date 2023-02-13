from radar.radar_template import Radar
from utils import choose_carac_and_player, prepare_radar_data, calculate_centile, color_name_to_hex, prepare_radar_formatting

def single_graph(df, name, carac, minimum_minutes, couleur_dominante, couleur_secondaire, image1_path,
               black_version):
    df_interet, df_all = choose_carac_and_player(df, name, carac, minimum_minutes)
    quantiles = calculate_centile(df_all, carac)
    params, ranges, values = prepare_radar_data(df_interet, quantiles)
    title_name, subtitle_name, file_name = prepare_radar_formatting(name, df_interet)
    title = dict(
        title_name=title_name,
        title_color=color_name_to_hex(couleur_secondaire),
        subtitle_name=subtitle_name,
        subtitle_color=color_name_to_hex(couleur_secondaire),
        subtitle_color_2=color_name_to_hex(couleur_secondaire),
        title_fontsize=18,
        subtitle_fontsize=15,
    )

    if black_version:
        file_name = "output_files/" + name + "/" + name + "_black.jpg"
    else:
        file_name = "output_files/" + name + "/" + name + "_white.jpg"

    endnote = "Visualisation réalisée par Data'Scout @datascout_\n Data/90mins, " \
              ">" + str(minimum_minutes) + "mins" + "\nSource : Wyscout"

    if black_version:
        radar = Radar(fontfamily="Liberation Serif", background_color="#121212", patch_color="#28252C",
                      label_color="#FFFFFF",
                      range_color="#FFFFFF", label_fontsize=17, range_fontsize=13)
        end_color = "#95919B"
    else:
        radar = Radar(fontfamily="Liberation Serif", background_color="#FFFFFF", patch_color="#D6D6D6",
                      label_color="#000000",
                      range_color="#000000", label_fontsize=15, range_fontsize=11)
        end_color = "#000000"

    _, ax = radar.plot_radar(ranges=ranges, params=params, values=values,
                             radar_color=[color_name_to_hex(couleur_dominante),
                                          color_name_to_hex(couleur_secondaire)],
                             title=title, endnote=endnote, filename=file_name,
                             logo="input_files/logos/logo_blanc.png", logo_coord=[0.4123, 0.4035, 0.2, 0.15],  # ,
                             image_1=image1_path, image_coord_1=[0.29, 0.75, 0.15, 0.15],
                             #image_2="input_images/godoy.png", image_coord_2=[0.59, 0.75, 0.15, 0.15],
                             #image_3="input_images/marseille.png", image_coord_3=[0.436, 0.80, 0.15, 0.15],
                             end_color=end_color)
    # logo_coord = [0.493, 0.43, 0.04, 0.1])

    print("Image saved at", file_name)

def double_graph(df, name_1, name_2, carac, minimum_minutes,
                 couleur_dominante_1, couleur_dominante_2, image1_path, image2_path, black_version):
    df_interet_1, df_all = choose_carac_and_player(df, name_1, carac, minimum_minutes)
    df_interet_2, df_all = choose_carac_and_player(df, name_2, carac, minimum_minutes)

    quantiles = calculate_centile(df_all, carac)
    params_1, ranges_1, values_1 = prepare_radar_data(df_interet_1, quantiles)
    params_2, ranges_2, values_2 = prepare_radar_data(df_interet_2, quantiles)

    values = [values_1, values_2]

    try:
        name_1 = name_1.split(" ")[1]
    except IndexError:
        name_1 = name_1

    try:
        name_2 = name_2.split(" ")[1]
    except IndexError:
        name_2 = name_2

    _, subtitle_name_1, file_name_1 = prepare_radar_formatting(name_1, df_interet_1)
    _, subtitle_name_2, file_name_2 = prepare_radar_formatting(name_2, df_interet_1)

    title_name_1 = name_1
    title_name_2 = name_2

    team_1 = df_interet_1["Squad"].values[0]
    age_1 = df_interet_1["Age"].values[0]
    minutes_1 = df_interet_1["Min"].values[0]

    team_2 = df_interet_2["Squad"].values[0]
    age_2 = df_interet_2["Age"].values[0]
    minutes_2 = df_interet_2["Min"].values[0]

    subtitle_name_1 = team_1.split(" ")[:][0] + " - " + str(minutes_1) + "mins" + " - " + str(age_1) + " ans"
    subtitle_name_2 = team_2.split(" ")[-1] + " - " + str(minutes_2) + "mins" + " - " + str(age_2) + " ans"

    if black_version:
        couleur_secondaire_1 = "lightgrey"
        couleur_secondaire_2 = "lightgrey"

    else:
        couleur_secondaire_1 = "black"
        couleur_secondaire_2 = "black"

    title = dict(
        title_name=title_name_1,
        title_color=color_name_to_hex(couleur_dominante_1),
        subtitle_name=subtitle_name_1,
        subtitle_color=color_name_to_hex(couleur_secondaire_1),
        title_name_2=title_name_2,
        title_color_2=color_name_to_hex(couleur_dominante_2),
        subtitle_name_2=subtitle_name_2,
        subtitle_color_2=color_name_to_hex(couleur_secondaire_2),
        title_fontsize=18,
        subtitle_fontsize=15,
    )
    endnote = "Visualisation réalisée par Data'Scout @datascoutsorare\n Data/90mins, " \
              ">" + str(minimum_minutes) + "mins. Source : Wyscout \n Tacles et interceptions ajustés à la possession"

    if black_version:
        radar = Radar(fontfamily="Liberation Serif", background_color="#121212", patch_color="#28252C",
                      label_color="#FFFFFF",
                      range_color="#FFFFFF", label_fontsize=15, range_fontsize=11)
        end_color = "#95919B"
        file_name = "output_files/" + name_1 + "/" + name_1 + "_"+ name_2 + "_black.jpg"
    else:
        radar = Radar(fontfamily="Liberation Serif", background_color="#FFFFFF", patch_color="#D6D6D6",
                      label_color="#000000",
                      range_color="#000000", label_fontsize=15, range_fontsize=11)
        end_color = "#000000"
        file_name = "output_files/" + name_1 + "/" + name_1 + "_"+ name_2 + "_white.jpg"

    _, ax = radar.plot_radar(ranges=ranges_1, params=params_1, values=values,
                             radar_color=[color_name_to_hex(couleur_dominante_1),
                                          color_name_to_hex(couleur_dominante_2)],
                             title=title, alphas=[0.8, 0.55], endnote=endnote, end_color=end_color, end_size=11,
                             compare=True, filename=file_name,
                             logo="input_files/logos/logo_noir.png", logo_coord=[0.4125, 0.4025, 0.2, 0.15],
                             image_1=image1_path, image_coord_1=[0.33, 0.79, 0.04, 0.1],
                             image_2=image2_path, image_coord_2=[0.65, 0.79, 0.04, 0.1])

    print("Radar saved at", file_name)
