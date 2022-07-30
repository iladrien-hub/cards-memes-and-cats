from flask import Flask
from flask_sock import Sock

from simple_websocket.ws import Server

app = Flask(__name__)
sock = Sock(app)


@sock.route('/reverse')
def reverse(ws: Server):
    print(type(ws))

    text = ws.receive()
    ws.send(text[::-1])
