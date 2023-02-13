import pandas as pd


def trad_french_english(french, df):
    # Traduit certains passages du df en anglais pour éviter tout bug et nettoie les caractères spéciaux
    if french:
        df["Player"] = df["Joueur"]
        df["Squad"] = df["Équipe"]
        df["Age"] = df["Âge"]
        df["Buts attendus"] = df["xG"]
        df["Passes décisives attendues"] = df["xA"]
        df["Min"] = df["Minutes jouées  "]
        df["Duels défensifs gagnés%"] = df["Duels défensifs gagnés, %"]
        df["Duels aériens gagnés%"] = df["Duels aériens gagnés, %"]
        df["Сentres précises%"] = df["Сentres précises, %"]
        df["Сentres du flanc gauche précises%"] = df["Centres du flanc gauche précises, %"]

    return


def clean_names(df):
    # Nettoie les noms des joueurs
    if "\\" in df["Player"][0]:
        for i in range(0, len(df)):
            try:
                df["Player"][i] = df["Player"][i].split("\\")[0]
            except NameError:
                break

    return


def choose_carac_and_player(df, name="Alex Bono", carac=None, minimum_minutes=540):
    # Fonction qui permet d'isoler les caractéristiques d'intêret du joueur d'intêret
    if carac is None:
        carac = ["PSxG"]
    df_filter_player = (df['Player'] == name)
    df_interet = df[df_filter_player]
    df_interet_filtered = pd.DataFrame()
    df_interet_filtered["Player"] = df_interet["Player"]
    df_interet_filtered["Squad"] = df_interet["Squad"]
    df_interet_filtered["Min"] = df_interet["Min"]
    df_interet_filtered["Age"] = df_interet["Âge"]

    try:
        df_filter_player = df['Min'] >= minimum_minutes
    except TypeError:
        df_filter_player = df['Min'].astype("int32") >= minimum_minutes
    df_all_filtered = df[df_filter_player]
    df_all_filtered["Player"] = df["Player"]
    df_all_filtered["Squad"] = df["Squad"]
    df_all_filtered["Min"] = df["Min"]
    df_interet_filtered["Age"] = df_interet["Âge"]

    for i in carac:
        df_interet_filtered[i] = df_interet[i]
        df_all_filtered[i] = df[i]

    return df_interet_filtered, df_all_filtered


def prepare_radar_formatting(name, df_interet):

    minutes = df_interet["Min"].values[0]
    title_name = "Pierre Bourdin vs défenseurs centraux de JPL"
    subtitle_name = "Sans club" + " - " + "Défenseur Central" + " - " + str(28) + " ans" + " - " + str(minutes) + " mins"
    file_name = "images/" + name + ".jpg"

    return title_name, subtitle_name, file_name


def calculate_centile(df_all, carac):
    quantiles = []
    for i in carac:
        low_quantile = df_all[i].astype("float").quantile(0.05)
        top_quantile = df_all[i].astype("float").quantile(0.95)
        quantiles.append([i, low_quantile, top_quantile])
    return quantiles


def prepare_radar_data(df_interet, quantiles):
    params = []
    ranges = []
    values = []
    for i in quantiles:
        parameter = carac_abbreviation_to_real_name(i[0])
        params.append(parameter)
        ranges.append((float(i[1]), float(i[2])))
        values.append(float(df_interet[i[0]].values[0]))
    return params, ranges, values


def color_name_to_hex(color_name):
    color_dict = dict()
    with open('input_files/color.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line[:-2].split(",")
            color_dict[key] = val
        try:
            final_color = color_dict[color_name]
        except KeyError as e:
            print(e, "n'existe pas dans color.csv, prends une autre couleur stp. Je mets du vert en attendant")
            final_color = color_dict["green"]
        return final_color


def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    with open('input_files/carac_names.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val

    return carac_dict[carac]
