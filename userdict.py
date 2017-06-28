# -*- coding:utf-8 -*-
# interpreted via python3.6

from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# connect to database
try:
    client = MongoClient("mongodb://lionking:Tv6pAzDp@60.205.187.223:27017/Simba?authMechanism=SCRAM-SHA-1")
    db_mongo = client.Simba
    collection = db_mongo.zbx_product
except Exception as e:
    print(e)
    sys.exit()

items = []
for item in collection.find():
    items.append(item["name"].strip("."))
    # items.append(item["name"])
    if item["name"] is None:
        print(item["_id"])

with open("dictionary.txt", "w") as f:
    for index, item in enumerate(items):
        # print(index, item)
        # f.write(item + " " + "3" + " " + "nz" + "\n")
        # f.write(str(index) + item + "\n")
        f.write(item + "\n")
