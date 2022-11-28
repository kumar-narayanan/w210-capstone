from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('session.html')

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

if __name__ == '__main__':
    socketio.run(app, host='172.31.86.221',port=5000 )
