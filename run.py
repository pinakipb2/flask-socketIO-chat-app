from flask import Flask, render_template, request, url_for, session, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )

@app.route('/', methods=['GET','POST'])
def home():
    if('username' in session):
        return redirect(url_for('chat'))
    if request.method == "POST":
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if('username' in session):
        username = session['username']
        return render_template('chat.html',username=username)
    else:
        return redirect(url_for('home'))

@app.route('/logout',methods=['GET','POST'])
def logout():
    if('username' in session):
        del session['username']
    return redirect(url_for('home'))

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
    print( 'recived my event: ' + str( json ) )
    socketio.emit( 'my response', json)


if __name__ == '__main__':
  socketio.run( app, debug = True )