# -*- coding:utf-8 -*-
# this module is used to implement user_dict and stop_words for jieba

import jieba
import jieba.analyse
import jieba.posseg
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

jieba.load_userdict("userdict2.txt")
jieba.analyse.set_stop_words("stopwords.txt")

sent = "友邦全佑至珍重疾保险计划的险种是什么？"

term = jieba.cut(sent)
print("word segment: " + '/'.join(term))

tag_list = jieba.analyse.extract_tags(sent, topK=10, withWeight=False, allowPOS=())
# tag_list = jieba.analyse.extract_tags(sent, topK=2, withWeight=False, allowPOS=("nz", "n", ))
print("key words: " + "/ ".join(tag_list))
# print tag_list[0], tag_list[1]

seg = []
seg_list = jieba.posseg.cut(sent)
for word, flag in seg_list:
    print ("%s, %s" % (word.decode("utf-8"), flag.decode("utf-8")))
    seg.append((word, flag))
# print seg
