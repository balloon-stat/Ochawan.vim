#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import urllib
import urllib2
import socket
import threading
import time
import datetime
import cookielib
from xml.etree import ElementTree
from Bouyomi import Bouyomi

class ConnectNicolive:
    def __init__(self, cookiePath, lvid=None):
        self.lvid = lvid
        self.cookiejar = cookielib.LWPCookieJar(cookiePath)
        if os.path.exists(cookiePath):
            self.cookiejar.load()
        ckprocesser = urllib2.HTTPCookieProcessor(self.cookiejar)
        self.opener = urllib2.build_opener(ckprocesser)
        self.token = None

    def login(self, mail, password):
         url = "https://secure.nicovideo.jp/secure/login"
         values = {"mail" : mail, "password" : password}
         data = urllib.urlencode(values)
         res = self.opener.open(url, data)
         return res.read()

    def isLogin(self):
        url = "http://live.nicovideo.jp/notifybox"
        res = self.opener.open(url)
        count = len(res.read())
        return count > 146

    def getPlayerStatus(self):
        url = "http://live.nicovideo.jp/api/getplayerstatus?v=" + self.lvid
        res = self.opener.open(url).read()
        elem = ElementTree.fromstring(res)

        if elem.get("status") != "ok":
            return None
        addr       = elem.findtext(".//addr")
        port       = elem.findtext(".//port")
        thread     = elem.findtext(".//thread")
        base_time  = elem.findtext(".//base_time")
        user_id    = elem.findtext(".//user_id")
        is_premium = elem.findtext(".//is_premium")
        return (addr, port, thread, base_time, user_id, is_premium)

    def getPostkey(self, count, thread):
        block_no = count // 100
        url = "http://live.nicovideo.jp/api/getpostkey?thread=%s&block_no=%s" % (thread, block_no)
        res = self.opener.open(url).read()
        return res[8:]

    def getToken(self):
        url = "http://live.nicovideo.jp/api/getpublishstatus?v="
        res = self.opener.open(url + self.lvid).read()
        elem = ElementTree.fromstring(res)
        return elem.findtext(".//token")

    def sendMsg(self, body, mail=None):
        urlprefix = "http://watch.live.nicovideo.jp/api/broadcast/"
        if mail is None:
            query = [
                ("body",  body),
                ("token", self.token)
            ]
        else:
            query = [
                ("body",  body),
                ("mail",  mail),
                ("token", self.token)
            ]
        url = urlprefix + self.lvid + "?" + urllib.urlencode(query)
        res = self.opener.open(url)
        return res.read()

    def is_broadcaster(self):
        if self.token is None:
            self.token = self.getToken()
        return len(self.token) > 0

class SendMsgThread(threading.Thread):
    def __init__(self, text, anonym, cliObj, nicoObj):
        threading.Thread.__init__(self)
        self.text = text
        self.anonym = anonym
        self.comc = cliObj
        self.conn = nicoObj

    def run(self):
        try:
            if self.conn.is_broadcaster():
                self.conn.sendMsg(self.text)
            else:
                self.comc.msgWrite(self.text, self.anonym, self.conn.getPlayerStatus)
        except Exception as e:
            print e.message

class CommClient:
    def __init__(self):
        self.sock = None
        self.is_connect = False
        self.do_bouyomi = False

    def initialize(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connect = False
        self.prev = ""
        self.count = 0
        self.cntBlock = 0
        self.postkey = ""
        self.queue = []

    def connect(self, info):
        if not self.sock is None:
            self.close()
        self.initialize()
        (addr, port, thread, base_time, user_id, is_premium) = info
        host = socket.gethostbyname(addr)
        self.sock.connect( (host, int(port)) )
        self.thread = thread
        self.base_time = base_time
        self.user_id = user_id
        self.is_premium = is_premium
        self.is_connect = True

    def sendReq(self):
        try:
            req = "<thread thread=\"" + self.thread + "\" version=\"20061206\" res_from=\"-100\"/>\0"
            self.sock.sendall(req)
        except:
            self.is_connect = False

    def msgWrite(self, msg, anonym, getPlayerStatus):
        if self.postkey == "" or self.count - self.cntBlock * 100 > 100:
            self.postkey = getPostkey(self.count, self.thread)
            self.cntBlock = self.count // 100
        if self.postkey == "":
            raise "Can not get postkey"
        anonymous = ""
        if anonym != 0: anonymous = " mail=\"184\""
        srvTimeSpan = int(self.srvtime) - int(self.base_time)
        localTimeSpan = int(time.mktime(datetime.datetime.now().timetuple())) - self.datetimeStart
        vpos = str((srvTimeSpan + localTimeSpan) * 100)
        text = "<chat thread=\"{0}\" ticket=\"{1}\" vpos=\"{2}\" postkey=\"{3}\" user_id=\"{4}\" premium=\"{5}\"{6}>{7}</chat>\0".format(
                    self.thread,
                    self.ticket,
                    vpos,
                    self.postkey,
                    self.user_id,
                    self.is_premium,
                    anonymous, msg)
        self.sock.sendall(text)

    def read(self):
        res = ""
        while res == "":
            res = self.sock.recv(1024)
        if self.prev == "" or res.startswith("<chat"):
            xml = res
            self.prev = ""
        else:
            xml = self.prev + res
            self.prev = ""

        for line in xml.split("\0"):
            # print line.decode("utf-8")
            if line.startswith("<thread"):
                elem = ElementTree.fromstring(line)
                # self.count = int(elem.get("last_res"))
                self.ticket = elem.get("ticket")
                self.srvtime = elem.get("server_time")
                self.datetimeStart = int(time.mktime(datetime.datetime.now().timetuple()))
                continue

            if not line.endswith("</chat>"):
                self.prev = line
                continue

            if line.startswith("<chat_result"):
                continue

            if line.startswith("<chat"):
                elem = ElementTree.fromstring(line)
                text = elem.text
                self.recvProc(elem.get("no"), elem.get("user_id"), text)
                if text == "/disconnect" and elem.get("premium") == "3":
                    self.close()
                    self.is_connect = False
                    continue
                self.count = int(elem.get("no"))
                continue

    def recv(self):
        try:
            self.sendReq()
            while self.is_connect:
                self.read()
        except Exception as e:
            print e.message

    def keepSession(self):
        try:
            while self.is_connect:
                time.sleep(600)
                self.sock.sendall("\0")
        except Exception as e:
            print e.message

    def close(self):
        #print "close..."
        self.sock.close()
        self.is_connect = False

    def recvProc(self, no, uid, text):
        #print no + ": " + uid
        #print text
        self.count = int(no)
        self.queue.append((no, uid, text))
        if self.do_bouyomi:
            bouyomi = Bouyomi()
            bouyomi.connect()
            bouyomi.send(text.encode("utf-8"))
            bouyomi.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "usage: ConnectNicolive.py <cookie> lvxxxxxx"
        exit()
    con = ConnectNicolive(sys.argv[1], sys.argv[2])
    comc = CommClient(con)
    comc.connect(con.getPlayerStatus())
    th_keep = threading.Thread(target=comc.keepSession)
    th_keep.daemon = True
    th_keep.start()
    th_recv = threading.Thread(target=comc.recv)
    th_recv.start()
    comc.msg = "test"
    th_send = SendMsgThread(comc, con)
    th_send.start()
    th_recv.join()

