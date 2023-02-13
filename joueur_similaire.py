import plotly.graph_objects as go
import plotly.offline as pyo

import statistics
import pandas as pd
from mplsoccer import PyPizza, add_image, FontManager
from scipy import stats
from xlwt import Workbook, Formula  # exporter en excel
import statistics

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
    print(j)
    for m in carac_list[1:]:
        carac1 = list(players_final[m])
        carac_player = list(players_final[(players_final['Player'] == j)][m])
        print(m)
        print(carac1)
        print(carac_player)
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

# Duels défensifs
carac_list = ['Player', 'DefDuel', 'DefWons', 'AerWons', 'AerDuel']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]

mean_list = []
mean = int(somme / cnt)
mean_list.append(mean)

# Interventions défensives
carac_list = ['Player', 'SuccDef', 'TklPAdj', 'IntPAdj', 'Blk']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Aggressivité
carac_list = ['Player', 'Foul', 'Yellow', 'Red']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Passes simples
carac_list = ['Player', 'Pass', 'AccPasses', 'Forward', 'Forward%', 'Back', 'Back%', 'Lateral', 'Lateral%', 'Short', 'Short%']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Vision de jeu
carac_list = ['Player', 'LgPass', 'LgPass%', 'Smart', 'Smart%', 'Third', 'Third%',
              'Through', 'Through%', 'Prog', 'Prog%']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Création d'occasion
carac_list = ['Player', 'ShAst', 'PreAst', '3Ast', 'KP', 'BoxPasses', 'BoxPasses%']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Aspect décisif
carac_list = ['Player', 'xA', 'xG', 'npG', 'Goals', 'Ast']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Vitesse
carac_list = ['Player', 'Acc', 'Run']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Centres
carac_list = ['Player', 'Cross', 'Cross%', 'BoxCross']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Dribbles
carac_list = ['Player', 'SuccOff', 'Drib', 'Drib%', 'OffDuel', 'Off%']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Tirs
carac_list = ['Player', 'Shots', 'ShCad%', 'Taux']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Présence dans la surface
carac_list = ['Player', 'TouchBox', 'Recept', 'LgRecept']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

# Jeu aérien
carac_list = ['Player', 'AerWons', 'AerDuel', 'Head']
cnt = 0
somme = 0
df = pd.DataFrame()
for i in carac_list[1:]:
    cnt += 1
    carac_player = list(player_filter[(player_filter['Player'] == player_name)][i])
    somme += carac_player[0]
    print(i)
    print(carac_player[0])

mean = int(somme / cnt)
print(mean)
mean_list.append(mean)

print(mean_list)

score = []
for i in mean_list:
    score.append(i/5)

categories = ['Duels défensifs', 'Interventions défensives', 'Aggressivité', 'Passes', 'Vision de jeu', 'Création d\'occasion',
              'Aspect décisif', 'Percussion', 'Centres', 'Technique', 'Tirs', 'Présence offensive', 'Jeu aérien']

categories = [*categories, categories[0]]

fig = go.Figure(
    data=[
        go.Scatterpolar(r=score, theta=categories, fill='toself', name='Yari Verschaeren')
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Yari Verschaeren'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True,
    )
)

pyo.plot(fig)