import argparse


def get_arguments():
    """
    Parsing arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--joueur_analyse", type=str, default="A. Hakimi", help="joueur que l'on analyse")
    parser.add_argument("--team", type=str, default="PSG", help="équipe du joueur")
    parser.add_argument("--joueur_compa", type=str, default="D. Raum", help="joueur de référence pour comparer")
    parser.add_argument("--archetype", type=str, default="piston", help="set de donnée utilisé")
    parser.add_argument("--minimum_minutes", type=int, default=1000, help="nombre de minutes minimums")
    parser.add_argument("--bdd", type=str, default="Latéraux des 5 grands Championnats", help="y'a qui dans le .csv")
    parser.add_argument("--année", type=str, default="365 derniers jouers", help="le .csv correspond a quelle période")
    parser.add_argument("--couleur1", type=str, default="psg1", help="Couleur du joueur analysé dans le radar")
    parser.add_argument("--couleur2", type=str, default="psg2", help="Couleur du joueur de comparaison dans le radar")

    return parser


def get_archetypes(archetype):
    archetypes = {"Buteur": ["xG par 90",
                             "Buts par 90",
                             "xA par 90",
                             "Passes décisives par 90",
                             "Passes vers la surface de réparation par 90",
                             "Touches de balle dans la surface de réparation sur 90",
                             "Duels offensifs par 90",
                             "Dribbles par 90",
                             "Courses progressives par 90",
                             "Accélérations par 90",
                             "Interceptions par 90",
                             "Duels défensifs par 90"],
                  "Sentinelle":
                      ["xG par 90",
                       "xA par 90",
                       "Dribbles par 90",
                       "Courses progressives par 90",
                       "Accélérations par 90",
                       "Passes vers l'avant par 90"
                       "Tacles glissés PAdj",
                       "Interceptions PAdj",
                       "Duels défensifs gagnés%",
                       "Duels défensifs par 90",
                       "Duels aériens gagnés%",
                       "Duels aériens par 90"]}

    return archetypes[archetype]


def get_slices_types(archetype):
    slice = []
    if archetype == "Buteur":
        slice = [6, 4, 2]
    if archetype == "Sentinelle":
        slice = [2, 4, 6]

    return slice