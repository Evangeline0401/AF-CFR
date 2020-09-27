import csv
import json
import statistics
import math
import pandas as pd
import openpyxl as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN


plays = open("Origin/plays.csv", "r")

p_reader = csv.reader(plays)
p_header = next(p_reader)

data, off_list, def_list = [], [], []
play_dict, num_dict, play_dictList, play_distdict = {}, {}, {}, {}

for i, row in enumerate(p_reader):
    if row[19] == "FALSE" and row[18] == "FALSE" and row[20] == "NA" and "TWO-POINT" not in row[26]:
        if str(row[9]) != "NA" and str(row[10]) != "NA" and str(row[11]) != "NA" and str(row[13]) != "NA":
            if "WR" not in str(row[13]) and "OL" not in str(row[13]) and "TE" not in str(row[13]):
                if "4 DL, 3 LB" in str(row[13]) or "4 DL, 2 LB" in str(row[13]) or "3 DL, 4 LB" in str(row[13]):# or "4 DL, 1 LB" in str(row[13]):
                    if "pass" in str(row[26]):
                        hoge = {
                            "Down": str(row[4]),
                            "YardLineNumber": str(row[8]),
                            "OffenseFormation": str(row[9]),
                            "OffensePersonnel": str(row[10]),
                            "DefenseInTheBox": str(row[11]),
                            "DefensePersonnel": str(row[13]),
                            "PlayType": "Pass",
                            "RunGap": "NA",
                            "PassLength": "short" if " short " in str(row[26]) else "deep",
                            "ActionSide": "middle" if " middle " in str(row[26]) else "right" if " right " in str(row[26]) else "left",
                            "PassYards": str(row[22]),
                            "PassResult": str(row[23]),
                            "YardsAfterCatch": str(row[24]),
                            "PlayResult": str(row[25]),
                            "Description": str(row[26]),
                        }
                        #off_name = hoge["OffenseFormation"]+"/"+hoge["OffensePersonnel"]+"/"+hoge["PlayType"]+"/"+hoge["PassLength"]+"/"+hoge["ActionSide"]
                        #def_name = hoge["DefenseInTheBox"]+"/"+hoge["DefensePersonnel"]
                        off_name = hoge["PlayType"]+" "+hoge["PassLength"]+" "+hoge["ActionSide"]
                        if "4 DL, 3 LB" in str(row[13]):
                            def_name = "4-3"
                        elif "4 DL, 2 LB" in str(row[13]):
                            def_name = "4-2"
                        elif "3 DL, 4 LB" in str(row[13]):
                            def_name = "3-4"
                        elif "4 DL, 1 LB" in str(row[13]):
                            def_name = "4-1"
                        action_profile = off_name+"    "+def_name
                        if action_profile not in play_dict:
                            play_dict[action_profile] = int(hoge["PlayResult"])
                            num_dict[action_profile]  = [off_name, def_name, 1]#1
                            play_dictList[action_profile] = [int(hoge["PlayResult"])]
                            play_distdict[action_profile] = {str(hoge["PlayResult"]): 1}
                        else:
                            play_dict[action_profile] += int(hoge["PlayResult"])
                            num_dict[action_profile][2]  += 1
                            play_dictList[action_profile].append(int(hoge["PlayResult"]))
                            if str(hoge["PlayResult"]) not in play_distdict[action_profile]:
                                play_distdict[action_profile][str(hoge["PlayResult"])] = 1
                            else:
                                play_distdict[action_profile][str(hoge["PlayResult"])] += 1
                    else:
                        hoge = {
                            "Down": str(row[4]),
                            "YardLineNumber": str(row[8]),
                            "OffenseFormation": str(row[9]),
                            "OffensePersonnel": str(row[10]),
                            "DefenseInTheBox": str(row[11]),
                            "DefensePersonnel": str(row[13]),
                            "PlayType": "Run",
                            "RunGap": "end" if " end " in str(row[26]) else "guard" if " guard " in str(row[26]) else "tackle" if " tackle " in str(row[26]) else "NA",
                            "PassLength": "NA",
                            "ActionSide": "left" if " left " in str(row[26]) else "right" if " right " in str(row[26]) else "middle",
                            "PassYards": str(row[22]),
                            "PassResult": str(row[23]),
                            "YardsAfterCatch": str(row[24]),
                            "PlayResult": str(row[25]),
                            "Description": str(row[26]),
                        }
                        #off_name = hoge["OffenseFormation"]+"/"+hoge["OffensePersonnel"]+"/"+hoge["PlayType"]+"/"+hoge["RunGap"]+"/"+hoge["ActionSide"]
                        #def_name = hoge["DefenseInTheBox"]+"/"+hoge["DefensePersonnel"]
                        off_name = hoge["PlayType"]+" "+hoge["RunGap"]+" "+hoge["ActionSide"]
                        if "4 DL, 3 LB" in str(row[13]):
                            def_name = "4-3"
                        elif "4 DL, 2 LB" in str(row[13]):
                            def_name = "4-2"
                        elif "3 DL, 4 LB" in str(row[13]):
                            def_name = "3-4"
                        elif "4 DL, 1 LB" in str(row[13]):
                            def_name = "4-1"
                        action_profile = off_name+"    "+def_name
                        if action_profile not in play_dict:
                            play_dict[action_profile] = int(hoge["PlayResult"])
                            num_dict[action_profile]  = [off_name, def_name, 1]#1
                            play_dictList[action_profile] = [int(hoge["PlayResult"])]
                            play_distdict[action_profile] = {str(hoge["PlayResult"]): 1}
                        else:
                            play_dict[action_profile] += int(hoge["PlayResult"])
                            num_dict[action_profile][2]  += 1
                            play_dictList[action_profile].append(int(hoge["PlayResult"]))
                            if str(hoge["PlayResult"]) not in play_distdict[action_profile]:
                                play_distdict[action_profile][str(hoge["PlayResult"])] = 1
                            else:
                                play_distdict[action_profile][str(hoge["PlayResult"])] += 1
                    
                    data.append(hoge)


j = open("/Users/shimano/webappSample/GameTheory/Algorithm/Data/Create/data2017.json", "w")
json.dump(data, j, indent=3)

plays.close()

num_dict = sorted(num_dict.items(), key=lambda x: x[1][2], reverse=True)
for i in num_dict:
    if i[1][0] not in off_list:
        off_list.append(i[1][0])
    if i[1][1] not in def_list:
        def_list.append(i[1][1])



#箱ひげ図の作成
IQR = {}
for key, item in play_dictList.items():
    sample = item
    points = (sample)
    fig, ax = plt.subplots()
    bp = ax.boxplot(points, whis=1.5)
    # IQRの取得
    q25, q75 = np.percentile(sample, [25, 75])
    IQR[key] = [q25, q75, q75 - q25]

    # PNG作成
    plt.title(key+"    DataNum :"+str(len(sample)))
    #plt.xlabel('Play')
    plt.ylabel('Yards')
    plt.ylim([min(sample)-5, max(sample)+5])
    plt.grid()
    fig.savefig("Create/PNG/BoxPlot/"+key+".png")
    plt.close()

#ヒストグラムの作成
for key, item in play_dictList.items():
    #外れ値削除
    del_list = []
    for i in item:
        if IQR[key][0]-IQR[key][2]*1.5 > int(i):
            del_list.append(i)
        if IQR[key][1]+IQR[key][2]*1.5 < int(i):
            del_list.append(i)
    for j in del_list:
        item.remove(j)
    
    fig = plt.figure()
    plt.title(key+"    DataNum :"+str(len(item)))
    plt.xlabel("Yard")
    plt.ylabel("Num")
    n, bins, patches = plt.hist(item, bins=3, density=True) #######
    print (key)
    hogehoge = []
    for i in range(len(n)):
        print ( n[i]*(bins[i+1]-bins[i]) )
    print ("===")
    fig.savefig("Create/PNG/Hist/"+key+".png")
    plt.close()

"""
#KDE処理（未完）
for key, item in play_dictList.items():
    #外れ値削除
    del_list = []
    for i in item:
        if IQR[key][0]-IQR[key][2]*1.5 > int(i):
            del_list.append(i)
        if IQR[key][1]+IQR[key][2]*1.5 < int(i):
            del_list.append(i)
    for j in del_list:
        item.remove(j)
    
    #sns.displot(item, bins=50, kde=True)
    #plt.figure()
    #plt.savefig("Create/PNG/Hist_kde/"+key+".png")
    #plt.close()
    # #画像出力方法考える！！！！！！

"""

#分布図の作成
for key, item in play_distdict.items():
    #外れ値削除
    del_list = []
    for i in item:
        if IQR[key][0]-IQR[key][2]*1.5 > int(i):
            del_list.append(i)
        if IQR[key][1]+IQR[key][2]*1.5 < int(i):
            del_list.append(i)
    for j in del_list:
        del item[j]
    
    s_play_distdict = sorted(item.items(), key=lambda x: int(x[0]))
    yard, num = [], []
    for dist in s_play_distdict:
        yard.append(int(dist[0]))
        num.append(dist[1])
    
    fig = plt.figure()
    plt.bar(yard, num)
    plt.title(key)
    plt.xlabel("Yard")
    plt.ylabel("Num")
    fig.savefig("Create/PNG/Dist/"+key+".png")
    plt.close()
