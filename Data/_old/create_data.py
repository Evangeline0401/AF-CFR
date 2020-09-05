import csv
import json
import pandas as pd


train = open("train.csv", "r")
reg   = open("reg_pbp_2019.csv", "r")
df_t  = pd.read_csv("train.csv")
df_r  = pd.read_csv("reg_pbp_2019.csv")

#print (df.iat[0, 3])

t_reader = csv.reader(train)
t_header = next(t_reader)
r_reader = csv.reader(reg)
r_header = next(r_reader)

tr_dict = {}
for i, row in enumerate(t_reader):
    if row[13] == "2019":
        if row[1] not in tr_dict:
            tr_dict[row[1]] = i

reg_dict = {}
for i, row in enumerate(r_reader):
    if len(row[0]) == 2:
        num = row[1]+"00"+row[0]
    elif len(row[0]) == 3:
        num = row[1]+"0"+row[0]
    elif len(row[0]) == 4:
        num = row[1]+row[0]
    reg_dict[num] = i

data = []
for k, v in tr_dict.items():
    if k in reg_dict:
        hoge = {
            "GameID": str(k),
            "YardLine": str(df_t.iat[v, 14]),
            "YardLine_100": str(df_r.iat[reg_dict[k], 8]),
            "Quarter": str(df_t.iat[v, 15]),
            "Down": str(df_t.iat[v, 18]),
            "Distance": str(df_t.iat[v, 19]),
            "OffenseFormation": str(df_t.iat[v, 24]),
            "OffensePersonnel": str(df_t.iat[v, 25]),
            "OffPlayType": str(df_r.iat[reg_dict[k], 25]),
            "Gain": str(df_r.iat[reg_dict[k], 26]),
            "Pass_Length": str(df_r.iat[reg_dict[k], 33]),
            "Pass_Location": str(df_r.iat[reg_dict[k], 34]),
            "Run_Location": str(df_r.iat[reg_dict[k], 37]),
            "Run_Gap": str(df_r.iat[reg_dict[k], 38]),
            "DefendersInTheBox": str(df_t.iat[v, 26]),
            "DefensePersonnel": str(df_t.iat[v, 27]),
            "Desc": str(df_r.iat[reg_dict[k], 24]),
        }
        data.append(hoge)

j = open("/Users/shimano/webappSample/GameTheory/data.json", "w")
json.dump(data, j, indent=3)

train.close()
reg.close()