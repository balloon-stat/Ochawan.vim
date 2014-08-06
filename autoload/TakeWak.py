#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import MultipartPostHandler
from HTMLParser import HTMLParser

class ExtractContentParser(HTMLParser):

    def __init__(self):
        self.content = ""
        self.confirm = ""
        HTMLParser.__init__(self)

    def handle_starttag(self,tagname,attribute):
        if tagname == "input":
            for i in attribute:
                if i[0] == "name" and i[1] == "description":
                    for j in attribute:
                        if j[0] == "value":
                            self.content = j[1]
                if i[0] == "name" and i[1] == "confirm":
                    for j in attribute:
                        if j[0] == "value":
                            self.confirm = j[1]

class ExtractLvidParser(HTMLParser):

    def __init__(self):
        self.lvurl = ""
        self.lvid = ""
        HTMLParser.__init__(self)

    def handle_starttag(self,tagname,attribute):
        if tagname == "meta":
            for i in attribute:
                if i[0] == "property" and i[1] == "og:url":
                    for j in attribute:
                        if j[0] == "content":
                            self.lvurl = j[1]
                            self.lvid = self.lvurl.replace("http://live.nicovideo.jp/watch/", "")

class TakeWak:

    def __init__(self, title, content, community, category, livetags):
        self.title = title.encode("utf-8")
        self.community = community.encode("utf-8")
        self.category = category.encode("utf-8")
        self.content = content
        self.livetags = livetags

    def set_params(self):
        content = u"<br />\r\n".join(self.content).encode("utf-8")
        params = { "is_wait" : "", "usecoupon": "", "title": self.title,
                "default_community": self.community, "timeshift_enabled": 1,
                    "tags[]": self.category, "description": content}
        index = 1
        for tag in self.livetags:
            params["livetags" + str(index)] = tag
            index += 1

        self.params = params

    def take(self, cookiejar, tempfile):
        url_editstream = "http://live.nicovideo.jp/editstream"

        self.set_params()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar),
                MultipartPostHandler.MultipartPostHandler)
        res = opener.open(url_editstream, self.params).read()

        cparser = ExtractContentParser()
        cparser.feed(res)
        cparser.close()
        self.params["description"] = cparser.content
        self.params["confirm"] = cparser.confirm
        self.params["kiyaku"] = "true"

        res = opener.open(url_editstream, self.params).read()

        lvparser = ExtractLvidParser()
        lvparser.feed(res.decode("utf-8"))
        lvparser.close()
        if lvparser.lvid == "":
            f = open(tempfile, "w")
            f.write(res)
            f.close()
        return lvparser.lvid

