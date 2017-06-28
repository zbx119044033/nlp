# -*- coding: utf-8 -*-
# This example shows how to use LTP API to perform POS tags on the custom word segmentation result.

from LTML import LTML
import sys
import urllib
import urllib2


def parsing(segment):
    ltml = LTML()
    ltml.build_from_words(segment)
    xml = ltml.tostring()
    print xml
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
        print content.decode("utf-8")
    except urllib2.HTTPError, e:
        print >> sys.stderr, e.reason

if __name__ == "__main__":
    seg = [("鑫享至尊", "nz"), ("的", "uj"), ("承保公司", "nz"), ("是", "v"), ("哪个", "r"), ("?", "x")]
    parsing(seg)
