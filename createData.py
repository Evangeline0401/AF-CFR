import csv
import json
import statistics
import math
import pandas as pd
import openpyxl as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
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
    for key_a, _ in o_a_dict.items():
        for_off_action, for_off_action_poss, for_off_action_p = [], [], []

        for key_d, _ in d_a_dict.items():
            for_def_action, for_def_action_poss, for_def_action_p = [], [], []

            for key, item in play_dictList.items():
                if key_a in key and key_d in key:
                    q25, q75 = np.percentile(item, [25, 75])
                    IQR[key] = [q25, q75, q75 - q25]
                    
                    del_list = []
                    for i in item:
                        if IQR[key][0]-IQR[key][2]*1.5 > int(i):
                            del_list.append(i)
                        if IQR[key][1]+IQR[key][2]*1.5 < int(i):
                            del_list.append(i)
                    for j in del_list:
                        item.remove(j)
                    
                    n, bins, _ = plt.hist(item, bins=3, density=True) ########

                    num = 0
                    for Bin in range(len(bins)-1):
                        for_mode_list = []
                        if n[Bin] > 0:
                            for yard in item:
                                if bins[Bin] <= yard and bins[Bin+1] >= yard:
                                    for_mode_list.append(yard)
                            M = stats.mode(for_mode_list)
                            for_def_action.append(M.mode[0])
                            if len(str(num)) == 1:
                                for_def_action_poss.append("00"+str(num))
                            elif len(str(num)) == 2:
                                for_def_action_poss.append("0"+str(num))
                            for_def_action_p.append(n[Bin])
                            num += 1
            
            for_off_action.append(for_def_action)
            for_off_action_poss.append(for_def_action_poss)
            for_off_action_p.append(for_def_action_p)
        
        get_yard.append(for_off_action)
        possibilities.append(for_off_action_poss)
        p_prob.append(for_off_action_p)

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