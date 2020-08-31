#!/usr/bin/python3

import os
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from glob import glob
import json
import subprocess
from subprocess import check_output
import time

app = Flask(__name__, template_folder="")

with open("/home/pi/Discord-bot-ture/autodeploy/config.json", encoding="utf-8") as f:
    config = json.load(f)

def get_commit(bytestring):
    if(len(bytestring) > 0 and bytestring != None):
        # The string can look like this:
        # b'8be682d [FIX] Forgot to remove '1'\n"
        string = str(bytestring).split(" ") # b'8be682d
        string = string[0][2:] # 8be682d 
        return string
        #return str(bytestring).split(" ")[0].split('"')[1]
    else:
        return "0"

def start_bot(path):
    subprocess.run(["git", "pull"], cwd=path)
    commit = get_commit(check_output(["git", "log", "-1", "--oneline"], cwd=path))
    subprocess.run(["python3", "bot.py", "boken123", commit], cwd=path)

def deploy(js):
    if js["repository"]["name"] not in config:
        return "REPOSITORY NOT FOUND", 404

    p = config[js["repository"]["name"]]
    start_bot(p["path"])
    subprocess.run(["git", "pull"], cwd=p["path"])
    subprocess.run(["sudo", "systemctl", "restart", p["service"]])
    #commit = get_commit(check_output(["git", "log", "-1", "--oneline"], cwd=p["path"]))
    #subprocess.run(["python3", "bot.py", "boken123", commit], cwd=p["path"])


@app.route("/", methods=["POST", "GET"])
def idx():
    if request.method == "POST":
        return deploy(request.json)

    return str(list(config.keys()))

@app.route("/start", methods=["GET"])
def start():
    if request.method == "GET":
        start_bot(config["Discord-bot-ture"]["path"])
    return "Ture is now deployed"

if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("PORT", 8080)))
