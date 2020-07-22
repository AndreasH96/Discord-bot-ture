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

with open("/home/pi/Discord-bot-ture/config.json") as f:
    config = json.load(f)

def get_commit(bytestring):
    if(len(bytestring) > 0 and bytestring != None):
        return str(bytestring).split(" ")[0].split('"')[1]
    else:
        return "0"

def deploy(js):
    if js["repository"]["name"] not in config:
        return "REPOSITORY NOT FOUND", 404

    p = config[js["repository"]["name"]]
    subprocess.run(["git", "pull"], cwd=p["path"])
    #subprocess.run(["sudo", "systemctl", "restart", p["service"]])
    commit = get_commit(check_output(["git", "log", "-1", "--oneline"], cwd=p["path"]))
    subprocess.run(["python3", "bot.py", "boken123", commit], cwd=p["path"])


@app.route("/", methods=["POST", "GET"])
def idx():
    if request.method == "POST":
        return deploy(request.json)

    return str(list(config.keys()))


if __name__ == "__main__":
    app.run("0.0.0.0", port=int(os.getenv("PORT", 8080)))
