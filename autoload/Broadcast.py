#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import ast
import vim
import threading
import ConnectNicolive as CN
from TakeWak import TakeWak

class Broadcast:
    def __init__(self, spath):
        self.spath = spath
        self.initialize()

    def initialize(self):
        self.conn = self.createConnection(self.spath)
        if self.conn is None:
            return False
        self.comc = CN.CommClient()
        return True

    def createConnection(self, path):
        fname = "ochwan_cookie.dat"
        fpath = os.path.join(path, fname)
        con = CN.ConnectNicolive(fpath)
        if con.isLogin():
            return con
        mail = vim.eval("input('nico e-mail address? ')")
        password = vim.eval("inputsecret('nico password? ')")
        con.login(mail, password)
        if con.isLogin():
            con.cookiejar.save()
            return con
        print " "
        print "Can not Login"
        return None

    def is_connect(self):
        return self.conn != None and self.comc != None and self.comc.is_connect

    def connect(self, lvid):
        if self.is_connect():
            self.stop()
        self.conn.lvid = lvid
        info = self.conn.getPlayerStatus()
        if info is None:
            print "Fail GetPlayerStatus()"
            return
        self.comc.connect(info)
        self.conn.getToken()
        th_keep = threading.Thread(target=self.comc.keepSession)
        th_keep.daemon = True
        th_keep.start()
        th_recv = threading.Thread(target=self.comc.recv)
        th_recv.daemon = True
        th_recv.start()

    def start(self, title, content, community, category, livetags):
        if not self.conn.isLogin():
            self.conn = self.createConnection(self.spath)
            if self.conn is None:
                return
        tw = TakeWak(title, content, community, category, livetags)
        tempfile = "ochawan_temp.html"
        lvid = tw.take(self.conn.cookiejar, tempfile)
        if lvid == "":
            vim.command("OpenBrowser " + tempfile)
            return
        self.connect(lvid)
        url = "http://live.nicovideo.jp/watch/" + lvid
        vim.command("OpenBrowser " + url)

    def stop(self):
        self.comc.close()
        self.comc = CN.CommClient()

    def live(self):
        title = ""
        community = ""
        content = []
        category = ""
        catedic = { "1":u"一般(その他)", "2":u"政治", "3":u"動物", "4":u"料理", "5":u"演奏してみた",
                    "6":u"歌ってみた", "7":u"踊ってみた", "8":u"描いてみた", "9":u"講座", "10":u"ゲーム",
                    "11":u"動画紹介", "12":u"R18" }
        in_description = False
        for line in vim.current.buffer:
            line = line.decode(vim.eval("&encoding"))
            if line.startswith(">>") and "Description" in line:
                in_description = True
                continue
            if line.startswith("Description") and "<<" in line:
                in_description = False
                continue
            if in_description:
                content.append(line)
            community += self.match(line, u"Broadcast_on:")
            title     += self.match(line, u"Title:")
            category  += self.match(line, u"Category:")
            if line.startswith(u"Tags:"):
                livetags = ast.literal_eval(line.replace(u"Tags:", "").strip())
        if title == "" or content == [] or community == "":
            print "Live description is wrong"
            empty = ""
            if title == "":
                empty += "title: "
            if content == []:
                empty += "content: "
            if community == "":
                empty += "community: "
            print "Empty is -> " + empty
            return
        self.start(title, content, community, catedic[category], livetags)

    @staticmethod
    def match(text, pattern):
        if text.startswith(pattern):
            return text.replace(pattern, "").strip()
        return ""

    def rendering(self, buf):
        if self.is_connect():
            enc = vim.eval("&encoding")
            if self.comc.queue != []:
                for (no, uid, text) in self.comc.queue:
                    text = text.encode(enc, "ignore")
                    buf.append(no + ":" + uid[:6] + ":" + text, 1)
                self.comc.queue = []

    def send(self, body, anonym):
        if self.is_connect():
            th = CN.SendMsgThread(body, anonym, self.comc, self.conn)
            th.start()

