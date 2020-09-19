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


def createInitialData():

    play_dictList, off_list, def_list = get_playDictList()

    action, o_a_list, d_a_list = [], [], []
    o_a_dict, d_a_dict = {}, {}
    for i in range(len(off_list)):
        o_a_dict[off_list[i]] = i
        o_a_list.append(i)
    action.append(o_a_list)
    for i in range(len(def_list)):
        d_a_dict[def_list[i]] = i
        d_a_list.append(i)
    action.append(d_a_list)

    get_yard, possibilities, p_prob = [], [], []
    IQR = {}
    for key_a, item_a in o_a_dict.items():
        for_off_action = []
        for key_d, item_d in d_a_dict.items():
            for_def_action = []
            for key, item in play_dictList.items():
                if key_a in key and key_d in key:
                    # IQRの取得
                    q25, q75 = np.percentile(item, [25, 75])
                    IQR[key] = [q25, q75, q75 - q25]
                    #外れ値削除
                    del_list = []
                    for i in item:
                        if IQR[key][0]-IQR[key][2]*1.5 > int(i):
                            del_list.append(i)
                        if IQR[key][1]+IQR[key][2]*1.5 < int(i):
                            del_list.append(i)
                    for j in del_list:
                        item.remove(j)
                    
                    n, bins, _ = plt.hist(item, bins=10, density=True)
                    print (n)
                    print (bins)
                    print ("===")

                    for_mode_list = []
                    for Bin in range(len(bins)-1):
                        if n[Bin] > 0:
                            print ()
                        else:
                            print ()
    

    exit()













    action = [ [], [] ]
    

    wb = px.load_workbook("/Users/shimano/webappSample/GameTheory/Data/Create/create2017xl.xlsx")
    ws = wb["Sheet1"]

    for i in range(50):
        if ws.cell(row=2+i, column=1).value == None:
            break
        action[0].append(i)
        get_yard.append([])
        possibilities.append([])
        p_prob.append([])
        for j in range(50):
            if ws.cell(row=1, column=2+j).value == None:
                break
            if j not in action[1]:
                action[1].append(j)
            for k in play_dictList:
                if ws.cell(row=2+i, column=1).value in k and ws.cell(row=1, column=2+j).value in k:
                    #確率関数作成
                    Min = math.floor(norm.ppf(0.00001, statistics.mean(play_dictList[k]), statistics.stdev(play_dictList[k])))
                    if Min < -10:
                        Min = -100
                    Max = math.floor(norm.ppf(0.99999, statistics.mean(play_dictList[k]), statistics.stdev(play_dictList[k])))
                    if Max > 100:
                        Max = 100
                    yard_and_prob, def_yard_clum, def_possib_clum, def_prob_clum = {}, [], [], []
                    itenum = 0
                    while Min < Max:
                        p1 = norm.cdf(Min-0.5, statistics.mean(play_dictList[k]), statistics.stdev(play_dictList[k]))
                        p2 = norm.cdf(Min+0.5, statistics.mean(play_dictList[k]), statistics.stdev(play_dictList[k]))
                        yard_and_prob[str(Min)] = Decimal(p2-p1)
                        def_yard_clum.append(Min)
                        if len(str(itenum)) == 1:
                            def_possib_clum.append("00"+str(itenum))
                        elif len(str(itenum)) == 2:
                            def_possib_clum.append("0"+str(itenum))
                        else:
                            def_possib_clum.append(str(itenum))
                        def_prob_clum.append(p2-p1)
                        itenum += 1
                        Min += 1
                    get_yard[i].append(def_yard_clum)
                    possibilities[i].append(def_possib_clum)
                    p_prob[i].append(def_prob_clum)

    return action, get_yard, possibilities, p_prob


def get_playDictList():

    plays = open("/Users/shimano/webappSample/GameTheory/Algorithm/Data/Origin/plays.csv", "r")

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
                            off_name = hoge["PlayType"]+":"+hoge["PassLength"]+":"+hoge["ActionSide"]
                            if "4 DL, 3 LB" in str(row[13]):
                                def_name = "4-3"
                            elif "4 DL, 2 LB" in str(row[13]):
                                def_name = "4-2"
                            elif "3 DL, 4 LB" in str(row[13]):
                                def_name = "3-4"
                            elif "4 DL, 1 LB" in str(row[13]):
                                def_name = "4-1"
                            action_profile = off_name+" :: "+def_name
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
                            off_name = hoge["PlayType"]+":"+hoge["RunGap"]+":"+hoge["ActionSide"]
                            if "4 DL, 3 LB" in str(row[13]):
                                def_name = "4-3"
                            elif "4 DL, 2 LB" in str(row[13]):
                                def_name = "4-2"
                            elif "3 DL, 4 LB" in str(row[13]):
                                def_name = "3-4"
                            elif "4 DL, 1 LB" in str(row[13]):
                                def_name = "4-1"
                            action_profile = off_name+" :: "+def_name
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
    
    plays.close()

    num_dict = sorted(num_dict.items(), key=lambda x: x[1][2], reverse=True)
    for i in num_dict:
        if i[1][0] not in off_list:
            off_list.append(i[1][0])
        if i[1][1] not in def_list:
            def_list.append(i[1][1])
    
    return play_dictList, off_list, def_list