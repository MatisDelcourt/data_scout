from urllib.request import urlopen

import matplotlib.pyplot as plt
from PIL import Image
import statistics
import pandas as pd
from mplsoccer import PyPizza, add_image, FontManager
from scipy import stats
from xlwt import Workbook, Formula  # exporter en excel
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def carac_abbreviation_to_real_name(carac):
    carac_dict = dict()
    with open('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/carac_names_fr.csv', newline='') as f:
        for line in f:
            line = line.strip('\n')
            (key, val) = line.split(",")
            carac_dict[key] = val
    return carac_dict[carac]


df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/beljo.csv', header=0)

## Filtering
df_filter = (df['Minutes jouées  '] >= 900)
player_filter = df[df_filter]

players_final = pd.DataFrame()
player_name = 'D. Beljo'

# Player and squad names
players_final['Player'] = player_filter['Joueur']
players_final['Min'] = player_filter['Minutes jouées  ']

# DEFENSE
players_final['SuccDef'] = player_filter['Actions défensives réussies par 90']
players_final['DefDuel'] = player_filter['Duels défensifs par 90']
players_final['DefWons'] = player_filter['Duels défensifs gagnés. %']
players_final['TklPAdj'] = player_filter['Tacles glissés PAdj']
players_final['IntPAdj'] = player_filter['Interceptions PAdj']
# players_final['Tkl+Int'] = players_final['TklPAdj'] + players_final['IntPAdj']
players_final['AerWons'] = player_filter['Duels aériens gagnés. %']
players_final['AerDuel'] = player_filter['Duels aériens par 90']
players_final['Blk'] = player_filter['Tirs contrés par 90']
players_final['Foul'] = player_filter['Fautes par 90']
players_final['Yellow'] = player_filter['Cartons jaunes par 90']
players_final['Red'] = player_filter['Cartons rouges par 90']

# POSSESSION
players_final['Pass'] = player_filter['Passes par 90']
players_final['AccPasses'] = player_filter['Passes précises. %']
players_final['Forward'] = player_filter['Passes avant par 90']
players_final['Forward%'] = player_filter['Passes en avant précises. %']
players_final['Back'] = player_filter['Passes arrière par 90']
players_final['Back%'] = player_filter['Passes arrière précises. %']
players_final['Lateral'] = player_filter['Passes latérales par 90']
players_final['Lateral%'] = player_filter['Passes latérales précises. %']
players_final['Short'] = player_filter['Passes courtes / moyennes par 90']
players_final['Short%'] = player_filter['Passes courtes / moyennes précises. %']
players_final['LgPass'] = player_filter['Passes longues par 90']
players_final['LgPass%'] = player_filter['Longues passes précises. %']
players_final['Longueur'] = player_filter['Longueur moyenne des passes. m']
players_final['Longueur2'] = player_filter['Longueur moyenne des passes longues. m']
players_final['ShAst'] = player_filter['Passes décisives avec tir par 90']
players_final['PreAst'] = player_filter['Secondes passes décisives par 90']
players_final['3Ast'] = player_filter['Troisièmes passes décisives par 90']
players_final['Smart'] = player_filter['Passes judicieuses par 90']
players_final['Smart%'] = player_filter['Passes intelligentes précises. %']
players_final['KP'] = player_filter['Passes quasi décisives par 90']
players_final['Third'] = player_filter['Passes dans tiers adverse par 90']
players_final['Third%'] = player_filter['Passes dans tiers adverse précises. %']
players_final['BoxPasses'] = player_filter['Passes vers la surface de réparation par 90']
players_final['BoxPasses%'] = player_filter['Passes vers la surface de réparation précises. %']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Through%'] = player_filter['Passes en profondeur précises. %']
players_final['Deep'] = player_filter['Réalisations en profondeur par 90']
players_final['Deep2'] = player_filter['Centres en profondeur. par 90']
players_final['Through'] = player_filter['Passes pénétrantes par 90']
players_final['Prog'] = player_filter['Passes progressives par 90']
players_final['Prog%'] = player_filter['Passes progressives précises. %']

# ATTAQUE
players_final['TouchBox'] = player_filter['Touches de balle dans la surface de réparation sur 90']
players_final['Acc'] = player_filter['Accélérations par 90']
players_final['Fouled'] = player_filter['Fautes subies par 90']
players_final['xA'] = player_filter['xA par 90']
players_final['xG'] = player_filter['xG par 90']
players_final['Head'] = player_filter['Buts de la tête par 90']
players_final['SuccOff'] = player_filter['Attaques réussies par 90']
players_final['Drib'] = player_filter['Dribbles par 90']
players_final['Drib%'] = player_filter['Dribbles réussis. %']
players_final['Cross'] = player_filter['Centres par 90']
players_final['Cross%'] = player_filter['Сentres précises. %']
players_final['LeftCross'] = player_filter['Centres du flanc gauche par 90']
players_final['LeftCross%'] = player_filter['Centres du flanc gauche précises. %']
players_final['RightCross'] = player_filter['Centres du flanc droit par 90']
players_final['RightCross%'] = player_filter['Centres du flanc droit précises. %']
players_final['BoxCross'] = player_filter['Centres dans la surface de but par 90']
players_final['npG'] = player_filter['Buts hors penalty par 90']
players_final['Goals'] = player_filter['Buts par 90']
players_final['Ast'] = player_filter['Passes décisives par 90']
players_final['OffDuel'] = player_filter['Duels offensifs par 90']
players_final['Off%'] = player_filter['Duels de marquage. %']
players_final['Run'] = player_filter['Courses progressives par 90']
players_final['Recept'] = player_filter['Passes réceptionnées par 90']
players_final['LgRecept'] = player_filter['Longues passes réceptionnées par 90']
# players_final['DS'] = player_filter['Buts hors penalty par 90'] + player_filter['Passes décisives par 90']
players_final['Shots'] = player_filter['Tirs par 90']
players_final['ShCad%'] = player_filter['Tirs à la cible. %']
players_final['Taux'] = player_filter['Taux de conversion but/tir']

players_filter = ((players_final['Player'] == player_name))
player_of_i = players_final[players_filter]

carac_list = ['Player', 'SuccDef', 'DefDuel', 'DefWons', 'TklPAdj', 'IntPAdj', 'AerWons', 'AerDuel', 'Blk', 'Foul', 'Yellow', 'Red',
              'Pass', 'AccPasses', 'Forward', 'Forward%', 'Back', 'Back%', 'Lateral', 'Lateral%', 'Short', 'Short%', 'LgPass', 'LgPass%',
              'Longueur', 'Longueur2', 'ShAst', 'PreAst', '3Ast', 'Smart', 'Smart%', 'KP', 'Third', 'Third%', 'BoxPasses', 'BoxPasses%',
              'Through', 'Through%', 'Deep', 'Deep2', 'Through', 'Prog', 'Prog%',
              'TouchBox', 'Acc', 'Fouled', 'xA', 'xG', 'Head', 'SuccOff', 'Drib', 'Drib%', 'Cross', 'Cross%', 'LeftCross',
              'LeftCross%', 'RightCross', 'RightCross%', 'BoxCross', 'npG', 'Goals', 'Ast', 'OffDuel', 'Off%',
              'Run', 'Recept', 'LgRecept', 'Shots', 'ShCad%', 'Taux']

values_list = []
# Calcul des centiles pour chaque stat

classeur = Workbook()
feuille = classeur.add_sheet("Centiles")

for i in range(0, len(carac_list)):
    feuille.write(0, i, carac_list[i])

k = 0
l = 0
for j in players_final['Player']:
    values_list = []
    l = 0
    feuille.write(k+1, 0, j)
    for m in carac_list[1:]:
        carac1 = list(players_final[m])
        carac_player = list(players_final[(players_final['Player'] == j)][m])
        centile = stats.percentileofscore(carac1, carac_player)
        values_list.append(int(centile))
        l += 1
        feuille.write(k+1, l, int(centile))
    k += 1


classeur.save("ALGO.xls")

read_file = pd.read_excel("ALGO.xls")
read_file.to_csv("ALGO.csv",
                 index=None,
                 header=True)

df = pd.DataFrame(pd.read_csv("ALGO.csv"))
print(df)

## Filtering
df_filter = (df['Blk'] >= 0)
player_filter = df[df_filter]

players_final = pd.DataFrame()
# player_name = 'S. Kalajdžić'

carac_list = ['Player', 'SuccDef', 'DefDuel', 'DefWons', 'TklPAdj', 'IntPAdj', 'AerWons', 'AerDuel', 'Blk', 'Foul', 'Yellow', 'Red',
              'Pass', 'AccPasses', 'Forward', 'Forward%', 'Back', 'Back%', 'Lateral', 'Lateral%', 'Short', 'Short%', 'LgPass', 'LgPass%',
              'Longueur', 'Longueur2', 'ShAst', 'PreAst', '3Ast', 'Smart', 'Smart%', 'KP', 'Third', 'Third%', 'BoxPasses', 'BoxPasses%',
              'Through', 'Through%', 'Deep', 'Deep2', 'Through', 'Prog', 'Prog%',
              'TouchBox', 'Acc', 'Fouled', 'xA', 'xG', 'Head', 'SuccOff', 'Drib', 'Drib%', 'Cross', 'Cross%', 'LeftCross',
              'LeftCross%', 'RightCross', 'RightCross%', 'BoxCross', 'npG', 'Goals', 'Ast', 'OffDuel', 'Off%',
              'Run', 'Recept', 'LgRecept', 'Shots', 'ShCad%', 'Taux']

carac_list = ['Player',
              'TouchBox', 'Acc', 'Fouled', 'xA', 'xG', 'Head', 'SuccOff', 'Drib', 'Drib%', 'Cross', 'Cross%',
              'BoxCross', 'npG', 'Goals', 'Ast', 'OffDuel', 'Off%',
              'Run', 'Recept', 'LgRecept', 'Shots', 'ShCad%', 'Taux']

values_list = []
dev_list = []
df = pd.DataFrame()
for j in player_filter['Player']:
    values_list = []
    coeff_list = []
    for i in carac_list[1:]:
        if j != player_name:
            carac1 = list(player_filter[(player_filter['Player'] == j)][i])
            carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
            if 0 <= carac_player[0] < 25:
                coeff = 0.25
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 25 <= carac_player[0] < 50:
                coeff = 0.5
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 50 <= carac_player[0] < 75:
                coeff = 0.75
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 75 <= carac_player[0] <= 100:
                coeff = 1
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            # ecart = abs(carac1[0]-carac_player[0])
            # values_list.append(ecart)
    if j != player_name:
        produits = []
        for i in range(len(values_list)):
            produits.append(values_list[i]*coeff_list[i])
        mean = sum(produits) / sum(coeff_list)
        # mean = sum(values_list) / len(values_list)
        var = sum((l - mean) ** 2 for l in values_list) / len(values_list)
        st_dev = math.sqrt(var)
        dev = statistics.pstdev(values_list)
        df = df.append({'Player': j, 'Ecart-Type': st_dev}, ignore_index=True)

df_top5 = df.sort_values(by = 'Ecart-Type').head(5)

names_list_off = []
for j in df_top5['Player']:
    names_list_off.append(j)

carac_list = ['Player', 'Pass', 'AccPasses', 'Forward', 'Forward%', 'Back', 'Back%', 'Lateral', 'Lateral%', 'Short', 'Short%', 'LgPass', 'LgPass%',
              'Longueur', 'Longueur2', 'ShAst', 'PreAst', '3Ast', 'Smart', 'Smart%', 'KP', 'Third', 'Third%', 'BoxPasses', 'BoxPasses%',
              'Through', 'Through%', 'Deep', 'Deep2', 'Through', 'Prog', 'Prog%']

values_list = []
dev_list = []
df = pd.DataFrame()
for j in player_filter['Player']:
    values_list = []
    for i in carac_list[1:]:
        if j != player_name:
            carac1 = list(player_filter[(player_filter['Player'] == j)][i])
            carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
            if 0 <= carac_player[0] < 25:
                coeff = 0.25
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 25 <= carac_player[0] < 50:
                coeff = 0.5
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 50 <= carac_player[0] < 75:
                coeff = 0.75
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 75 <= carac_player[0] <= 100:
                coeff = 1
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            # ecart = abs(carac1[0]-carac_player[0])
            # values_list.append(ecart)
    if j != player_name:
        produits = []
        for i in range(len(values_list)):
            produits.append(values_list[i]*coeff_list[i])
        mean = sum(produits) / sum(coeff_list)
        # mean = sum(values_list) / len(values_list)
        var = sum((l - mean) ** 2 for l in values_list) / len(values_list)
        st_dev = math.sqrt(var)
        dev = statistics.pstdev(values_list)
        df = df.append({'Player': j, 'Ecart-Type': st_dev}, ignore_index=True)

df_top5 = df.sort_values(by = 'Ecart-Type').head(5)

names_list_pos = []
for j in df_top5['Player']:
    names_list_pos.append(j)

carac_list = ['Player', 'SuccDef', 'DefDuel', 'DefWons', 'TklPAdj', 'IntPAdj', 'AerWons', 'AerDuel', 'Blk', 'Foul', 'Yellow', 'Red']

values_list = []
dev_list = []
df = pd.DataFrame()
for j in player_filter['Player']:
    values_list = []
    for i in carac_list[1:]:
        if j != player_name:
            carac1 = list(player_filter[(player_filter['Player'] == j)][i])
            carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
            if 0 <= carac_player[0] < 25:
                coeff = 0.25
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 25 <= carac_player[0] < 50:
                coeff = 0.5
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 50 <= carac_player[0] < 75:
                coeff = 0.75
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            elif 75 <= carac_player[0] <= 100:
                coeff = 1
                ecart = abs(carac1[0]-carac_player[0])
                values_list.append(ecart)
                coeff_list.append(coeff)
            # ecart = abs(carac1[0]-carac_player[0])
            # values_list.append(ecart)
    if j != player_name:
        produits = []
        for i in range(len(values_list)):
            produits.append(values_list[i]*coeff_list[i])
        mean = sum(produits) / sum(coeff_list)
        # mean = sum(values_list) / len(values_list)
        var = sum((l - mean) ** 2 for l in values_list) / len(values_list)
        st_dev = math.sqrt(var)
        dev = statistics.pstdev(values_list)
        df = df.append({'Player': j, 'Ecart-Type': st_dev}, ignore_index=True)

df_top5 = df.sort_values(by = 'Ecart-Type').head(5)

names_list_def = []
for j in df_top5['Player']:
    names_list_def.append(j)

print("Joueurs similaires offensivement à", player_name, ":", names_list_off[0], ",", names_list_off[1], ",", names_list_off[2], ",", names_list_off[3], ",", names_list_off[4])
print("Joueurs similaires dans le jeu de passes à", player_name, ":", names_list_pos[0], ",", names_list_pos[1], ",", names_list_pos[2], ",", names_list_pos[3], ",", names_list_pos[4])
print("Joueurs similaires défensivement à", player_name, ":", names_list_def[0], ",", names_list_def[1], ",", names_list_def[2], ",", names_list_def[3], ",", names_list_def[4])