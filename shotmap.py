import matplotlib
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager

# Sur le site Understat, chercher un joueur et aller sur sa page. Son id se trouve dans l'URL.
player_id = 11055 #undestat player id
is_season = True #if is_season = True, then specify season
season = 2022 #2020 corresponds to 2020/21
highlight_goals = False
image = Image.open(r"C:\Users\Matis\Documents\Sorare_Data\Graph_Building\hojlund.png")
#import libraries

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
from mplsoccer.pitch import Pitch, VerticalPitch
import requests
#data scraping
print(matplotlib.matplotlib_fname())

base = "https://understat.com/player/"
player_id = str(player_id)
base_url = base + player_id
url = base_url
res = requests.get(url)
soup = BeautifulSoup(res.content,"lxml")

scripts = soup.find_all('script')
strings = scripts[3].string

ind_start = strings.index("('")+2
ind_end = strings.index("')")

json_data = strings[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

data = json.loads(json_data)

finaldata = pd.DataFrame.from_dict(data)
# Data Wrangling

finaldata["X"] = pd.to_numeric(finaldata["X"])
finaldata["Y"] = pd.to_numeric(finaldata["Y"])
finaldata["season"] = pd.to_numeric(finaldata["season"])
finaldata["minute"] = pd.to_numeric(finaldata["minute"])
finaldata["xG"] = pd.to_numeric(finaldata["xG"])

finaldata["X"] = finaldata["X"] * 120
finaldata["Y"] = finaldata["Y"] * 80

finaldata = finaldata[finaldata["situation"] != "Penalty"]
finaldata = finaldata[["result", "X", "Y", "xG", "player", "season"]]

if is_season == True:
        finaldata = finaldata[finaldata["season"] == season]
        year = {2014: "2014/15", 2015: "2015/16", 2016: "2016/17", 2017: "2017/18", 2018: "2018/19",
                2019: "2019/20", 2020: "2020/21", 2021: "2021/22", 2022 : "2022/23"}
        finaldata["season"] = finaldata["season"].map(year)
        szn = finaldata["season"].values[0]
        x = 45.2
        y = 62
elif is_season == False:
        finaldata["all"] = finaldata["season"]
        finaldata["all"] = "All Seasons"
        szn = finaldata["all"].values[0]
        x = 47
        y = 62
#plotting

if highlight_goals == False:
        colours = {'Goal':'#6BAB90', 'SavedShot':'#648DE5', 'MissedShots':'#FE5E41',
                   'BlockedShot':'#AF4D98', 'ShotOnPost':'#F4D35E'}
        player_name = finaldata["player"].values[0]
        print(player_name)
        res = {"Goal": 1, "SavedShot": 0, "BlockedShot": 0, "ShotOnPost": 0,
               "MissedShots": 0, "OwnGoal": 0}
        finaldata["isGoal"] = finaldata["result"].map(res)
        finaldata["col"] = finaldata["result"].map(colours)
        finaldata = finaldata.dropna()

        xG = sum(finaldata["xG"])
        xG = str(round(xG, 2))
        xgst = sum(finaldata["xG"]) / len(finaldata.index)
        xgst = str(round(xgst, 2))
        gls = sum(finaldata["isGoal"])

        g = mpatches.Patch(color = "#6BAB90", label = "But")
        ss = mpatches.Patch(color = "#648DE5", label = "Tir arrêté")
        ms = mpatches.Patch(color = "#FE5E41", label = "Tir non cadré")
        bs = mpatches.Patch(color = "#AF4D98", label = "Tir contré")
        sop = mpatches.Patch(color = "#F4D35E", label = "Tir sur le poteau")

        pitch = VerticalPitch(pitch_color='#1B2631', line_color = "#707B7C", stripe=False, half = True)
        pitch = VerticalPitch(pitch_color='#000C32', line_color="#FBFBFF", stripe=False, half=True)
        fig, ax = pitch.draw()
        plt.scatter(x = finaldata["Y"], y = finaldata["X"], s = finaldata["xG"] * 800, c = finaldata["col"],
                    edgecolors="white")
        plt.gca().invert_xaxis()
        plt.text(17.5, 61, f"xG = {xG}\nxG/tir = {xgst}\nButs = {gls}", size = 16, color = "white")
        plt.text(79, 56.5, "Visualisation réalisée par @datascout_\nDonnées issues d\'Understat\nCode par : @placeholder2004", color = "white", size = 6)
        plt.text(40.2, 71, f"{player_name}\n{szn}", size=20, color="white", fontweight="bold", horizontalalignment='center')
        # plt.title(f"{player_name}", color = "white", fontweight = "bold", size = 25, pad = -25)
        leg = plt.legend(handles = [g, ss, ms, bs, sop], frameon = False, loc = "center left",
                         bbox_to_anchor=(0.043,0.15), prop={'size': 12})

        for text in leg.get_texts():
            text.set_color("white")

elif highlight_goals == True:
        gls = {'Goal': "Goal", 'SavedShot': "NoGoal", 'MissedShots': "NoGoal",
               'BlockedShot': "NoGoal", 'ShotOnPost': "NoGoal"}
        colours = {'Goal': "#E74C3C", 'NoGoal': "#1B2631"}
        finaldata["result"] = finaldata["result"].map(gls)
        player_name = finaldata["player"].values[0]
        res = {"Goal": 1, "NoGoal": 0}
        finaldata["isGoal"] = finaldata["result"].map(res)
        finaldata["col"] = finaldata["result"].map(colours)
        finaldata = finaldata.dropna()

        xG = sum(finaldata["xG"])
        xG = str(round(xG, 2))
        xgst = sum(finaldata["xG"]) / len(finaldata.index)
        xgst = str(round(xgst, 2))
        gls = sum(finaldata["isGoal"])

        g = mpatches.Patch(color="#E74C3C", label="But")
        ss = mpatches.Patch(color="#ffffff", label="Pas de but")

        pitch = VerticalPitch(pitch_color='#1B2631', line_color="#707B7C", stripe=False, half=True)
        fig, ax = pitch.draw()
        plt.scatter(x=finaldata["Y"], y=finaldata["X"], s=finaldata["xG"] * 600, c=finaldata["col"],
                    edgecolors="white")
        plt.gca().invert_xaxis()

        # plt.text(x, y, f"{szn}", color="white", size= 18, fontweight = "bold")
        plt.text(17.5, 61, f"xG = {xG}\nxG/tir = {xgst}\nButs = {gls}", size = 16, color = "white")
        plt.text(79, 56.5,
                 "Visualisation réalisée par @datascout_\nDonnées issues d\'Understat\nCode par : @placeholder2004",
                 color="white", size=6)
        plt.text(40.2, 71, f"{player_name}\n{szn}", size=20, color="white", fontweight="bold", horizontalalignment='center')
        leg = plt.legend(handles = [g, ss], frameon = False, loc = "center left",
                         bbox_to_anchor=(0.05,0.1), prop={'size': 12})

        # ax_image = add_image(
        #         image, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
        # )

        for text in leg.get_texts():
            text.set_color("white")

fig.set_size_inches(10, 8)
plt.savefig("Shotmap_%s_%s.png" % (player_name, szn[:4]), dpi = 900)
plt.show()
