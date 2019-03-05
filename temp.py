# -*- coding: utf-8 -*-

from pymongo import MongoClient
from LTML import LTML
import sys
import time
import urllib
import urllib2
import json
import jieba.posseg
import jieba.analyse


reload(sys)
sys.setdefaultencoding("utf-8")
jieba.load_userdict("userdict2.txt")
jieba.analyse.set_stop_words("stopwords.txt")

# connect to database
try:
    client = MongoClient("mongodb://xxx")
    db_mongo = client.Simba
    collect = db_mongo.entity_product
    print "Connect to MongoDB!"
except Exception, e:
    print e
    sys.exit()


def find_index(s1, s2, ss):
    a = None
    b = None
    for i in range(len(ss)):
        if ss[i]["cont"] == s1:
            a = i
        elif ss[i]["cont"] == s2:
            b = i
    return a, b


def my_str(s):
    if isinstance(s, list):
        if isinstance(s[0], dict):
            ss = ""
            for i in range(len(s)):
                for key, value in s[i].items():
                    ss += "%s: %s\n" % (key, value)
            return ss
        else:
            return " ".join(s)
    else:
        return s


def pos(sentence):
    # 分词，词性标注
    segment = []
    seg_list = jieba.posseg.cut(sentence)
    for word, flag in seg_list:
        # print ("%s, %s" % (word, flag))
        segment.append((word.encode("utf-8"), flag.encode("utf-8")))
    # print segment
    print "POS completed!"
    return segment


def parsing(segment):
    # 语法依存分析
    ltml = LTML()
    ltml.build_from_words(segment)
    xml = ltml.tostring()
    # print xml

    # uri_base = "http://api.ltp-cloud.com/analysis/?"  # from HIT
    uri_base = "http://ltpapi.voicecloud.cn/analysis/?"  # from USTC

    data = {
            # "api_key": "p1D280Q923TgJsxCHdDVUseO9eYurYzusZzD6UeS",  # from HIT
            "api_key": "J1W4B9X7U4j2g4K4J4Y0hlgWyCEWEzZNLmJbLIhR",  # from USTC
            "text": xml,
            "format": "json",
            "pattern": "dp",
            "xml_input": "true"
            }
    params = urllib.urlencode(data)
    try:
        request = urllib2.Request(uri_base)
        response = urllib2.urlopen(request, params)
        content = response.read().strip()
        # print content.decode("utf-8")
        print "Parsing completed!"
        return json.loads(content)[0][0]
    except urllib2.HTTPError, ee:
        print >> sys.stderr, ee.reason


def find_key(sentence):
    # 关键字提取
    seg = pos(sentence)
    par_list = parsing(seg)
    name, prop = None, None
    # 方法一
    tag_list = jieba.analyse.extract_tags(sentence, topK=2, withWeight=False, allowPOS=())
    a, b = find_index(tag_list[0], tag_list[1], par_list)
    if par_list[a]["parent"] == par_list[b]["id"]:
        name, prop = tag_list[0], tag_list[1]
    elif par_list[b]["parent"] == par_list[a]["id"]:
        name, prop = tag_list[1], tag_list[0]
    # 方法二
    if name is None:
        tag_list = jieba.analyse.extract_tags(sentence, topK=2, withWeight=False, allowPOS=("nz", "n", ))
        a, b = find_index(tag_list[0], tag_list[1], par_list)
        if a < b:
            name, prop = par_list[a]["cont"], par_list[b]["cont"]
        else:
            name, prop = par_list[b]["cont"], par_list[a]["cont"]
    # print name, prop
    return name.decode("utf-8"), prop.decode("utf-8")


def search(t, collection):
    # 检索
    name, prop = t[0], t[1]
    answer = "产品无此属性"
    cursor = collection.find_one({"name": name})
    if cursor is None:
        answer = "查无此项"
    else:
        for i in range(len(cursor["props"])):
            if cursor["props"][i]["name"] == prop or prop in cursor["props"][i]["alias"]:
                answer = my_str(cursor["props"][i]["value"])
                break
    # print "Search completed!"
    return answer


if __name__ == "__main__":
    sent = "友邦全佑至珍重疾保险计划的保障利益是什么？"
    t1 = time.time()
    tt = find_key(sent)
    print "name: %s\t property: %s" % tt
    ans = search(tt, collect)
    t2 = time.time()
    tc = t2-t1
    print sent.decode("utf-8")
    print ans.replace(u'\xa0', u'').decode("utf-8"), tc
