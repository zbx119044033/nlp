# -*- coding: utf-8 -*-
# This example shows how to use Python to access the LTP API

import urllib2
import urllib
import sys


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ["xml", "json", "conll", "plain"]:
        print >> sys.stderr, "usage: %s [xml/json/conll]" % sys.argv[0]
        sys.exit(1)

    # uri_base = "http://ltpapi.voicecloud.cn/analysis/?"
    uri_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = "p1D280Q923TgJsxCHdDVUseO9eYurYzusZzD6UeS"
    text = "鑫享至尊的承保公司是哪个?"
    text = urllib.quote(text)
    form = sys.argv[1]
    pattern = "dp"
    # pattern = ws | pos | ner | dp | sdp | sdp_graph | srl | all
    url = (uri_base + "api_key=" + api_key + "&" + "text=" + text + "&" + "format=" + form + "&" + "pattern=" + pattern)

    try:
        response = urllib2.urlopen(url)
        content = response.read().strip()
        print content.decode("utf-8")
    except urllib2.HTTPError, e:
        print >> sys.stderr, e.reason
