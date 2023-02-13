import pandas as pd
from utils import trad_french_english, clean_names
from pizza.pizza_config import pizza_graph
from radar.radar_config import double_graph, single_graph
from parameters import get_arguments, get_archetypes, get_slices_types
import os


def main():
    # Take CSV file
    print("Get CSV file...")
    df = pd.read_csv('/home/abennetot/Light_Datascout/data/jota.csv', header=0)

    # Clean dataset
    print("Clean Dataset...")
    trad_french_english(french=True, df=df)
    clean_names(df)

    # Get graph parameters
    print("Get parameters...")
    opts = get_arguments().parse_args()
    joueur_analyse = opts.joueur_analyse
    team = opts.team
    print("Analysed Player is", joueur_analyse, "playing for", team)
    joueur_compa = opts.joueur_compa
    print("Compared Player is", joueur_compa)
    archetype = opts.archetype
    print("Player Archetype is", archetype)
    minimum_minutes = opts.minimum_minutes
    print("Minimum minutes played are", minimum_minutes)
    bdd = opts.bdd
    print("Percentiles will be calculated against", bdd)
    année = opts.année
    print("during the time period :", bdd)
    couleur1 = opts.couleur1
    couleur2 = opts.couleur2
    print("Graph colors will be", couleur1, "and", couleur2)
    pizza_color1 = "#FCB9B2"
    pizza_color2 = "#B23A48"
    pizza_color3 = "#8C2F39"
    pizza_background = "#000000"
    print("Pizza colors ready")

    try:
        name_joueur_analyse = joueur_analyse.split(" ")[1]
    except IndexError:
        name_joueur_analyse = joueur_analyse

    try:
        name_joueur_compa = joueur_compa.split(" ")[1]
    except IndexError:
        name_joueur_compa = joueur_compa

    # Prepare path to save photos
    if not os.path.exists("output_files/" + name_joueur_analyse):
        os.mkdir("output_files/" + name_joueur_analyse)
    print("Prepare path to save photos")

    # Get photos
    print("Check photos")
    photo_path1 = "input_files/photos/" + name_joueur_analyse + ".png"
    photo_path2 = "input_files/photos/" + name_joueur_compa + ".png"
    equipe_path = "input_files/photos/" + team + ".png"

    carac = get_archetypes(archetype)
    print("Get important caracs for", archetype)
    slices = get_slices_types(archetype)
    print("We have", slices[0], "caracs in Attaque", slices[1], "caracs in Possession and", slices[2], "carcs in Defense")

    # Pizza Graph
    print("Plot Pizza Graph of", joueur_analyse)
    pizza_graph(df, joueur_analyse, carac, minimum_minutes, photo_path1, equipe_path, pizza_color1, pizza_color2,
                pizza_color3, pizza_background, bdd, année, slices)

    # Single Radar Graph in black and white versions
    print("Plot Single Radar Graph of", joueur_analyse)
    single_graph(df, joueur_analyse, carac, minimum_minutes, couleur1, couleur2, photo_path1,
               black_version=True)
    single_graph(df, joueur_analyse, carac, minimum_minutes, couleur1, couleur2, photo_path1,
               black_version=False)


    # Comparison Radar Graph in black and white versions
    print("Plot Double Radar Graph of", joueur_analyse, "compared to", joueur_compa)
    double_graph(df, joueur_analyse, joueur_compa, carac, minimum_minutes,
                 couleur1, couleur2, photo_path1, photo_path2, black_version=True)
    double_graph(df, joueur_analyse, joueur_compa, carac, minimum_minutes,
                 couleur1, couleur2, photo_path1, photo_path2, black_version=False)


if __name__ == '__main__':
    main()
