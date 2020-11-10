# -*- coding: utf-8 -*-
import re
import execjs
import sqlite3
import requests
from time import time
from urllib.parse import urlencode

qq = 000000  # QQ号
header = {
    "referer": "https://y.qq.com/portal/player.html",
    "user-agent": "Safari/537.36"
}


def _getSign(dat):
    js = """
        function sign(n) {
            function l(n, t) {
                var o = (65535 & n) + (65535 & t);
                return (n >> 16) + (t >> 16) + (o >> 16) << 16 | 65535 & o
            }
            function r(n, t, o, e, u, p) {
                return l((i = l(l(t, n), l(e, p))) << (r = u) | i >>> 32 - r, o);
                var i, r
            }
            function g(n, t, o, e, u, p, i) {
                return r(t & o | ~t & e, n, t, u, p, i)
            }
            function a(n, t, o, e, u, p, i) {
                return r(t & e | o & ~e, n, t, u, p, i)
            }
            function s(n, t, o, e, u, p, i) {
                return r(t ^ o ^ e, n, t, u, p, i)
            }
            function v(n, t, o, e, u, p, i) {
                return r(o ^ (t | ~e), n, t, u, p, i)
            }
            function t(n) {
                return function(n) {
                    var t, o = "";
                    for (t = 0; t < 32 * n.length; t += 8) o += String.fromCharCode(n[t >> 5] >>> t % 32 & 255);
                    return o
                } (function(n, t) {
                    n[t >> 5] |= 128 << t % 32,
                    n[14 + (t + 64 >>> 9 << 4)] = t;
                    var o, e, u, p, i, r = 1732584193,
                    f = -271733879,
                    h = -1732584194,
                    c = 271733878;
                    for (o = 0; o < n.length; o += 16) r = g(e = r, u = f, p = h, i = c, n[o], 7, -680876936),
                    c = g(c, r, f, h, n[o + 1], 12, -389564586),
                    h = g(h, c, r, f, n[o + 2], 17, 606105819),
                    f = g(f, h, c, r, n[o + 3], 22, -1044525330),
                    r = g(r, f, h, c, n[o + 4], 7, -176418897),
                    c = g(c, r, f, h, n[o + 5], 12, 1200080426),
                    h = g(h, c, r, f, n[o + 6], 17, -1473231341),
                    f = g(f, h, c, r, n[o + 7], 22, -45705983),
                    r = g(r, f, h, c, n[o + 8], 7, 1770035416),
                    c = g(c, r, f, h, n[o + 9], 12, -1958414417),
                    h = g(h, c, r, f, n[o + 10], 17, -42063),
                    f = g(f, h, c, r, n[o + 11], 22, -1990404162),
                    r = g(r, f, h, c, n[o + 12], 7, 1804603682),
                    c = g(c, r, f, h, n[o + 13], 12, -40341101),
                    h = g(h, c, r, f, n[o + 14], 17, -1502002290),
                    r = a(r, f = g(f, h, c, r, n[o + 15], 22, 1236535329), h, c, n[o + 1], 5, -165796510),
                    c = a(c, r, f, h, n[o + 6], 9, -1069501632),
                    h = a(h, c, r, f, n[o + 11], 14, 643717713),
                    f = a(f, h, c, r, n[o], 20, -373897302),
                    r = a(r, f, h, c, n[o + 5], 5, -701558691),
                    c = a(c, r, f, h, n[o + 10], 9, 38016083),
                    h = a(h, c, r, f, n[o + 15], 14, -660478335),
                    f = a(f, h, c, r, n[o + 4], 20, -405537848),
                    r = a(r, f, h, c, n[o + 9], 5, 568446438),
                    c = a(c, r, f, h, n[o + 14], 9, -1019803690),
                    h = a(h, c, r, f, n[o + 3], 14, -187363961),
                    f = a(f, h, c, r, n[o + 8], 20, 1163531501),
                    r = a(r, f, h, c, n[o + 13], 5, -1444681467),
                    c = a(c, r, f, h, n[o + 2], 9, -51403784),
                    h = a(h, c, r, f, n[o + 7], 14, 1735328473),
                    r = s(r, f = a(f, h, c, r, n[o + 12], 20, -1926607734), h, c, n[o + 5], 4, -378558),
                    c = s(c, r, f, h, n[o + 8], 11, -2022574463),
                    h = s(h, c, r, f, n[o + 11], 16, 1839030562),
                    f = s(f, h, c, r, n[o + 14], 23, -35309556),
                    r = s(r, f, h, c, n[o + 1], 4, -1530992060),
                    c = s(c, r, f, h, n[o + 4], 11, 1272893353),
                    h = s(h, c, r, f, n[o + 7], 16, -155497632),
                    f = s(f, h, c, r, n[o + 10], 23, -1094730640),
                    r = s(r, f, h, c, n[o + 13], 4, 681279174),
                    c = s(c, r, f, h, n[o], 11, -358537222),
                    h = s(h, c, r, f, n[o + 3], 16, -722521979),
                    f = s(f, h, c, r, n[o + 6], 23, 76029189),
                    r = s(r, f, h, c, n[o + 9], 4, -640364487),
                    c = s(c, r, f, h, n[o + 12], 11, -421815835),
                    h = s(h, c, r, f, n[o + 15], 16, 530742520),
                    r = v(r, f = s(f, h, c, r, n[o + 2], 23, -995338651), h, c, n[o], 6, -198630844),
                    c = v(c, r, f, h, n[o + 7], 10, 1126891415),
                    h = v(h, c, r, f, n[o + 14], 15, -1416354905),
                    f = v(f, h, c, r, n[o + 5], 21, -57434055),
                    r = v(r, f, h, c, n[o + 12], 6, 1700485571),
                    c = v(c, r, f, h, n[o + 3], 10, -1894986606),
                    h = v(h, c, r, f, n[o + 10], 15, -1051523),
                    f = v(f, h, c, r, n[o + 1], 21, -2054922799),
                    r = v(r, f, h, c, n[o + 8], 6, 1873313359),
                    c = v(c, r, f, h, n[o + 15], 10, -30611744),
                    h = v(h, c, r, f, n[o + 6], 15, -1560198380),
                    f = v(f, h, c, r, n[o + 13], 21, 1309151649),
                    r = v(r, f, h, c, n[o + 4], 6, -145523070),
                    c = v(c, r, f, h, n[o + 11], 10, -1120210379),
                    h = v(h, c, r, f, n[o + 2], 15, 718787259),
                    f = v(f, h, c, r, n[o + 9], 21, -343485551),
                    r = l(r, e),
                    f = l(f, u),
                    h = l(h, p),
                    c = l(c, i);
                    return [r, f, h, c]
                } (function(n) {
                    var t, o = [];
                    for (o[(n.length >> 2) - 1] = void 0, t = 0; t < o.length; t += 1) o[t] = 0;
                    for (t = 0; t < 8 * n.length; t += 8) o[t >> 5] |= (255 & n.charCodeAt(t / 8)) << t % 32;
                    return o
                } (n), 8 * n.length))
            }
            function o(n) {
                return t(unescape(encodeURIComponent(n)))
            }
            return function(n) {
                var t, o, e = "0123456789abcdef",u = "";
                for (o = 0; o < n.length; o += 1)
                    t = n.charCodeAt(o),
                    u += e.charAt(t >>> 4 & 15) + e.charAt(15 & t);
                return u
            } (o(n))
        }
    """
    ctx = execjs.compile(js)
    dat = str(dat).replace("\'", '\"').replace(' ', '')
    return 'zzaqmb18p03j3bwp2' + ctx.call('sign', "CJBPACrRuNy7" + dat)


def getSongUrl(mid):
    data = {
        "req": {"module": "CDN.SrfCdnDispatchServer", "method": "GetCdnDispatch",
                "param": {"guid": "4099348000", "calltype": 0, "userip": ""}},
        "req_0": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                  "param": {"guid": "4099348000", "songmid": [mid], "songtype": [0],
                            "uin": "%s" % qq, "loginflag": 1, "platform": "20"}},
        "comm": {"uin": qq, "format": "json", "ct": 24, "cv": 0}
    }
    sign = _getSign(data)

    param = {
        "-": "getplaysongvkey3697931411814759", "g_tk": "1835240802", "sign": sign, "loginUin": qq, "hostUin": 0,
        "format": "json", "inCharset": "utf8", "outCharset": "utf-8",
        "notice": 0, "platform": "yqq.json", "needNewCode": 0, "data": data
    }
    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?' + urlencode(param).replace("%27", "%22").replace("+", "")

    target = requests.get(url, headers=header).json()
    if target['code'] == 0:
        songUrl = 'http://isure.stream.qqmusic.qq.com/' + target['req_0']['data']['midurlinfo'][0]['purl']
        return songUrl


def findMid(topId, period):
    data = {"detail": {"module": "musicToplist.ToplistInfoServer", "method": "GetDetail",
                       "param": {
                           "topId": int(topId),
                           "offset": 0, "num": 20,
                           "period": period  # 2020_37
                       }},
            "comm": {"ct": 24, "cv": 0}}
    sign = _getSign(data)
    param = {"-": "getUCGI49055385410842267", "g_tk": 754132771, "sign": sign, "loginUin": 000000000, "hostUin": 0,
             "format": "json", "inCharset": "utf8", "outCharset": "utf-8", "notice": 0, "platform": "yqq.json",
             "needNewCode": 0, "data": data}

    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?' + urlencode(param).replace("%27", "%22").replace("+", "")
    target = requests.get(url).json()
    if target['code'] == 0 and target['detail']['code'] == 0:
        s_list = target['detail']['data']['songInfoList']
        s_ = []
        for songinfo in s_list:
            s_.append({
                "src": '/static/music/' + songinfo['mid'] + ".m4a",
                "title": songinfo['name'] + "--" + songinfo["singer"][0]["name"]
            })
        return s_

    else:
        return False


def get_lyric(songmid):
    par = {
        "-": "MusicJsonCallback_lrc",
        "pcachetime": int(time() * 1000),
        "songmid": songmid,
        "g_tk_new_20200303": "484192640",
        "g_tk": "484192640",
        "loginUin": qq,
        "hostUin": "0",
        "format": "json",
        "inCharset": "utf8",
        "outCharset": "utf-8",
        "notice": "0",
        "platform": "yqq.json",
        "needNewCode": "0"
    }

    header["referer"] = "https://y.qq.com/"
    url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?" + urlencode(par)
    lyric = requests.get(url, headers=header).json().get("lyric", "")
    js = """
        function lyric(e) {
            var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

            var o, t, n, c, d, a, h = "",
                C = 0;
            for (e = e.replace(/[^A-Za-z0-9\+\/\=]/g, ""); C < e.length;)
                o = _keyStr.indexOf(e.charAt(C++)) << 2 | (c = _keyStr.indexOf(e.charAt(C++))) >> 4,
                t = (15 & c) << 4 | (d = _keyStr.indexOf(e.charAt(C++))) >> 2,
                n = (3 & d) << 6 | (a = _keyStr.indexOf(e.charAt(C++))),
                h += String.fromCharCode(o),
                64 != d && (h += String.fromCharCode(t)),
                64 != a && (h += String.fromCharCode(n));
            for (var e = "", o = 0, t = c1 = c2 = 0; o < h.length;)
                (t = h.charCodeAt(o)) < 128 ? (e += String.fromCharCode(t),
                    o++) : t > 191 && t < 224 ? (c2 = h.charCodeAt(o + 1),
                    e += String.fromCharCode((31 & t) << 6 | 63 & c2),
                    o += 2) : (c2 = h.charCodeAt(o + 1),
                    c3 = h.charCodeAt(o + 2),
                    e += String.fromCharCode((15 & t) << 12 | (63 & c2) << 6 | 63 & c3),
                    o += 3);
            return e;
        }
    """
    ctx = execjs.compile(js)
    return ctx.call('lyric', lyric)


def findSong(songName):
    songList = []
    fdata = {
        "ct": 24, "qqmusic_ver": 1298, "new_json": 1, "remoteplace": "txt.yqq.song", "searchid": 54452660604165950,
        "t": 0, "aggr": 1, "cr": 1, "catZhida": 1, "lossless": 0, "flag_qc": 0, "p": 1, "n": 10,
        "w": "%s" % songName,
        "g_tk_new_20200303": 139034212, "g_tk": 139034212, "loginUin": qq, "hostUin": 0, "format": "json",
        "inCharset": "utf8", "outCharset": "utf-8", "notice": 0, "platform": "yqq.json", "needNewCode": 0
    }
    p = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?"
    url = p + urlencode(fdata)
    response = requests.get(url, headers=header)
    target = response.json()['data']['song']['list']
    for song in target:
        songList.append({
            "src": '/static/music/' + song['mid'] + ".m4a",
            "title": song['name'] + "--" + song['singer'][0]['name']
        })
    return songList


class Mys:
    def __init__(self):
        self.conn = sqlite3.connect("WEB.db")
        self.cursor = self.conn.cursor()
        self._crete()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def _crete(self):
        sql = """create table if not exists music(
                    mid varchar(20) primary key,
                    name varchar(50) ,
                    singer varchar(50)
                    );"""
        self.cursor.execute(sql)

    def find(self, mid):
        sql = "select * from music where mid=?"
        self.cursor.execute(sql, [mid])
        res = self.cursor.fetchall()
        return res

    def into(self, info):
        sql = f"insert into music(mid, name, singer) values(?, ?, ?)"
        self.cursor.execute(sql, info)
        self.conn.commit()

    def delinfo(self, mid):
        sql = "delete from music where mid=?"
        self.cursor.execute(sql, [mid])
        self.conn.commit()

    def test(self):
        sql = "desc music"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res
