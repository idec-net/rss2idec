#!/usr/bin/env python3

import feedparser, html2text, urllib.request, urllib.parse, base64, sys

node = ""
authkey = ""
echoarea = ""
base = ""
url = ""
config = "rss2idec.cfg"

def load_config():
    try:
        global node, authkey, echoarea, base, url
        cfg = open(config, "r").read().split("\n")
        for line in cfg:
            param = line.split(" ")
            if param[0] == "node":
                node = param[1]
            elif param[0] == "auth":
                authkey = " ".join(param[1:])
            elif param[0] == "echo":
                echoarea = param[1]
            elif param[0] == "base":
                base = " ".join(param[1:])
            elif param[0] == "url":
                url = " ".join(param[1:])
    except:
        print("Config not found.")
        quit()

def render_msg(item):
    msg = echoarea + "\n"
    msg = msg + "All" + "\n"
    msg = msg + item["title"] + "\n\n"
    msg = msg + h.handle(item["description"]).strip() + "\n\n"
    msg = msg + "Ссылка: " + item["link"]
    msg = msg.replace("&gt;", ">").replace("&lt;", "<").replace("\-", "—")
    return msg

def show_help():
    print("Usage: idec2rss.py [-f filename] [-h]\n")
    print("  -f filename Set config file.")
    print("  -h          This message.\n")
    print("If not -f set then script try load rss2idec.cfg file as config.")
    quit()

args = sys.argv[1:]
if "-h" in args:
    show_help()
if "-f" in args:
    config = args[args.index("-f") + 1]

load_config()
rss = feedparser.parse(url)

try:
    guids = open(base, "r").read().split("\n")
except:
    open(base, "w")
    guids = []

h = html2text.HTML2Text()
h.body_width = 0
h.ignore_links = True
h.ignore_images = True
h.emphasis_mark = ""
h.strong_mark = ""

for item in rss["entries"]:
    if not item["guid"] in guids:
        body = base64.b64encode(render_msg(item).encode("utf-8"))
        data = urllib.parse.urlencode({"tmsg": body,"pauth": authkey}).encode("utf-8")
        request = urllib.request.Request(node + "u/point")
        result = urllib.request.urlopen(request, data).read().decode("utf-8")
        if result.startswith("msg ok"):
            open(base, "a").write(item["guid"] + "\n")
        elif result == "msg big!":
            print ("ERROR: very big message (limit 64K)!")
        elif result == "auth error!":
            print ("ERROR: unknown auth!")
        else:
            print ("ERROR: unknown error!")
