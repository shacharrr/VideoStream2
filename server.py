from threading import Thread
import signal
import sys
import json

from flask import Flask, send_from_directory, render_template, request, send_file
from websocket_handler import WebSocketServer
from db_conn import DataBase

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    server.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

with open("server.json", "r") as f:
    json_load_file = json.load(f)

app = Flask(__name__)
database = DataBase('storage/database.db')
server = WebSocketServer(database, json_load_file["host"], json_load_file["wsport"], json_load_file["ssl"])

SERVER_NAME = f"http{"s" if json_load_file["ssl"] else ""}://{json_load_file["host"]}:{json_load_file["port"]}/"

@app.route('/')
def index():
    return render_template('index.html', server=SERVER_NAME)

@app.route("/login")
def login():
    return render_template('login.html', server=SERVER_NAME)

@app.route("/signup")
def signup():
    return render_template('signup.html', server=SERVER_NAME)

@app.route("/search")
def search():
    return render_template('search.html', server=SERVER_NAME)

@app.route("/watch")
def watch():
    key = request.args.get('v', default=1, type=int)
    return render_template('watch.html', server=SERVER_NAME, key=key)

@app.route("/upload")
def upload():
    return render_template('upload.html', server=SERVER_NAME)

@app.route('/<path:path>')
def catch_all(path):
    try:
        if path.startswith('storage'):
            return send_file(path)

        return send_from_directory('templates', path)
    except Exception as e:
        print(e)
        return "404"

if __name__ == '__main__':
    if json_load_file["ssl"]:
        Thread(target=app.run, kwargs={"ssl_context": ("./encryption/server.crt", "./encryption/server.key"), "host": json_load_file["host"], "port": json_load_file["port"]}).start()
    else:
        Thread(target=app.run, kwargs={"host": json_load_file["host"], "port": json_load_file["port"]}).start()
    server.start()