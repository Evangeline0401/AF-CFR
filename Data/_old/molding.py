import json


json_open = open("data.json", "r")
json_load = json.load(json_open)

hoge = {}
for i in json_load:
    tag = i["OffPlayType"]+"/"+i["Run_Location"]+"/"+i["Run_Gap"]+"/"+i["OffenseFormation"]+"/"+i["OffensePersonnel"]+"/"+i["DefendersInTheBox"]+"/"+i["DefensePersonnel"]
    if tag not in hoge:
        hoge[tag] = int(i["Gain"])
    else:
        hoge[tag] = hoge[tag]+int(i["Gain"])

for k, v in hoge.items():
    print (v, k)
print (len(hoge))