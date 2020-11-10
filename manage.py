# -*- coding: utf-8 -*-
from fun import *
import time, os, re
from flask import Flask, render_template, request, abort, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html", er="您访问的页面去浪迹天涯了……\n%s" % e)


@app.route("/find", methods=["POST"])
def find():
    li = findSong(request.form.get('target'))
    return jsonify(li)


@app.route("/lrc", methods=["POST"])
def ric():
    mid = request.form.get("target")
    mid = mid.split("/")[-1].replace(".m4a", "")
    lyricList = []
    ly = get_lyric(mid)
    for i in ly.replace("\r","").split("\n"):
        k = re.findall("^\[(.*?):(.*?)\](.+?)$", i)
        if k and len(k[0]) == 3:
            lyricList.append({"t": int(k[0][0]) * 60 + float(k[0][1]), "c":k[0][2]})
    return jsonify(lyricList)


@app.route("/music", methods=["POST"])
def music():
    arg_key = request.form.get('target')
    s = time.localtime(time.time())
    tm_mon = s.tm_mon if s.tm_mon > 9 else '0%s' % s.tm_mon
    tm_mday = s.tm_mday if s.tm_mday > 9 else '0%s' % s.tm_mday
    ks = ['%s-%s-%s' % (s.tm_year, tm_mon, tm_mday),
          '%s_%s' % (s.tm_year, int(s.tm_yday / 7)),
          '%s_%s' % (s.tm_year, int(s.tm_yday / 7) - 1)]
    for k in ks:
        print(k)
        s_list = findMid(arg_key, k)
        if s_list:
            a = Mys()
            for i in s_list:
                x, y = i.get('title').split('--')
                z = i.get('src').replace('/static/music/', '').replace(".m4a", "")
                info = [z, x, y]
                try:
                    a.into(info)
                except:
                    pass
            return jsonify(s_list)
    abort(404)


@app.before_request
def play():
    if r"static/music/" in request.url:
        filename = request.url.split("/")[-1]
        p = './static/music/%s' % filename
        if not os.path.exists(p):
            songUrl = getSongUrl(filename.replace(".m4a", ""))
            header['referer'] = 'https://y.qq.com/portal/player.html'
            response = requests.get(songUrl, headers=header)
            with open(p, "wb") as f:
                f.write(response.content)
                f.close()
        if os.path.getsize(p) < 600:
            os.remove(p)
            return "您没有权限获取歌曲……"
        else:
            get_lyric(filename.replace(".m4a", ""))

    if r"=" in request.url:
        abort(404)
    if r".php" in request.url:
        abort(404)
    try:
        if r"M" not in request.headers.get("User-Agent"):
            abort(404)
    except:
        abort(404)


@app.after_request
def process(resp):
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
