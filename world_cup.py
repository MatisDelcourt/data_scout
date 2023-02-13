from urllib.request import urlopen

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import statistics
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
from scipy import stats
from xlwt import Workbook, Formula  # exporter en excel
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('C:/Users/Matis/Documents/Sorare_Data/Graph_Building/worldcup.csv', header=0)

liste_equipe = ['Qatar', 'Equateur', 'Sénégal', 'Pays-Bas',
                'Angleterre', 'Iran', 'USA', 'Pays de Galles',
                'Argentine', 'Arabie Saoudite', 'Mexique', 'Pologne',
                'Danemark', 'Tunisie', 'France', 'Australie',
                'Allemagne', 'Japon', 'Espagne', 'Costa Rica',
                'Maroc', 'Croatie', 'Belgique', 'Canada',
                'Suisse', 'Cameroun', 'Brésil', 'Serbie',
                'Uruguay', 'Corée du Sud', 'Portugal', 'Ghana'
                ]

liste_carac = ['Equipe', 'BU Unopposed', 'BU Opposed', 'Progression', 'Final Third', 'Long Ball', 'Attacking Transition',
               'Counter Attack', 'Set Piece', 'High Press', 'Mid Press', 'Low Press', 'HighPress%', 'MidPress%',
               'LowPress%', 'Press', 'High Block', 'Mid Block', 'Low Block', 'Block', 'HighBlock%', 'MidBlock%', 'LowBlock%',
               'Recovery', 'Defensive Transition', 'Counter-press', 'Possession', 'Possession adverse',
               'Contest', 'Goals', 'Attempts', 'On target', 'Total Passes', 'Complete Passes', 'Completed Line Breaks Padj',
               'Defensive Line Breaks Padj', 'Completed Line Breaks',
               'Defensive Line Breaks', 'Receptions Final Third', 'Crosses', 'Ball Progressions', 'Defensive pressures applied Padj',
               'Direct pressures Padj', 'Forced TO', 'Second balls', 'Distance', 'High Speed Distance', 'OM Final Third Padj',
               'OM Mid Third Padj', 'OM Def Third Padj', 'OM Total Padj', 'Offers received Padj', 'OM Inside Shape Padj', 'OM Outside Shape Padj',
               'Opp OM Final Third Padj', 'Opp OM Mid Third Padj', 'Opp OM Def Third Padj', 'Opp OM Total Padj',
               'Opp Offers received Padj', 'Opp OM Inside Shape Padj', 'Opp OM Outside Shape Padj',
               'Possession regained Padj', 'Interceptions Padj', 'Tackles Padj', 'Ratio Poss Def Actions', 'Pressure Duration',
               'Ball recovery Time', 'Pressing direction inside', 'Pressing direction outside', 'xG', 'Min']

classeur = Workbook()
feuille = classeur.add_sheet("Moyennes")

df_filter = (df['BU Unopposed'] >= 0)
team_filter = df[df_filter]

team_filter['Press'] = team_filter['High Press'] + team_filter['Mid Press'] + team_filter['Low Press']
team_filter['HighPress%'] = (team_filter['High Press'] / team_filter['Press']) * 100
team_filter['MidPress%'] = (team_filter['Mid Press'] / team_filter['Press']) * 100
team_filter['LowPress%'] = (team_filter['Low Press'] / team_filter['Press']) * 100
team_filter['Block'] = team_filter['High Block'] + team_filter['Mid Block'] + team_filter['Low Block']
team_filter['HighBlock%'] = (team_filter['High Block'] / team_filter['Block']) * 100
team_filter['MidBlock%'] = (team_filter['Mid Block'] / team_filter['Block']) * 100
team_filter['LowBlock%'] = (team_filter['Low Block'] / team_filter['Block']) * 100

for i in range(0, len(liste_carac)):
    feuille.write(0, i, liste_carac[i])

moy = []
k=0
l=0
for i in liste_equipe:
    l=0
    feuille.write(k+1, 0, i)
    for j in liste_carac[1:]:
        if j == 'Goals' or j == 'Attempts' or j == 'On target' or j == 'Total Passes' or j == 'Complete Passes'\
        or j == 'Completed Line Breaks Padj' or j == 'Defensive Line Breaks Padj' or j == 'Completed Line Breaks'\
        or j == 'Defensive Line Breaks' or j == 'Receptions Final Third' or j == 'Crosses' or j == 'Ball Progressions'\
        or j == 'Defensive pressures applied Padj' or j == 'Direct pressures Padj' or j == 'Forced TO'\
        or j == 'Second balls' or j == 'Distance' or j == 'High Speed Distance' or j == 'OM Final Third Padj'\
        or j == 'OM Mid Third Padj' or j == 'OM Def Third Padj' or j == 'OM Total Padj' or j == 'Offers received Padj'\
        or j == 'OM Inside Shape Padj' or j == 'OM Outside Shape Padj' or j == 'Opp OM Final Third Padj'\
        or j == 'Opp OM Mid Third Padj' or j == 'Opp OM Def Third Padj' or j == 'Opp OM Total Padj'\
        or j == 'Opp Offers received Padj' or j == 'Opp OM Inside Shape Padj' or j == 'Opp OM Outside Shape Padj'\
        or j == 'Possession regained Padj' or j == 'Interceptions Padj' or j == 'Tackles Padj'\
        or j == 'Pressing direction inside' or j == 'Pressing direction outside':
            carac_values = list(team_filter[(team_filter['Equipe'] == i)][j])
            min = list(team_filter[(team_filter['Equipe'] == i)]['Min'])
            moy = np.mean(carac_values)
            coeff = (np.sum(min)/(len(min)*90))
            moy = moy / coeff
            l+= 1
            feuille.write(k+1, l, round(moy, 2))
        else:
            carac_values = list(team_filter[(team_filter['Equipe'] == i)][j])
            moy = np.mean(carac_values)
            l += 1
            feuille.write(k+1, l, round(moy, 2))
    k += 1

classeur.save("WC_Moyenne.xls")