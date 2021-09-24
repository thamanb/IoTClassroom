
import socket 
import threading
from flask import Flask, render_template, Response
import numpy as np
from pi_stream import Pi_Stream


PORT = 5050
# SERVER should be changed based on the server computers IP
SERVER = '192.168.200.242'
ADDR = (SERVER, PORT)
server = socket.socket()
server.bind(ADDR)







  

def start_thread():

    # listens for new connections
    server.listen()

    while True:
        # waits for connection and then creates socket object
        connection, addr = server.accept()
        Pi_Stream.pi_objs.append(Pi_Stream(connection, addr))
        print(Pi_Stream.pi_objs[-1].addr[0])
        
        

video = 0
start = True




#Flask
app = Flask(__name__)

@app.route("/")
def home():
    return render_template ('index.html')


#generator function   
def gen():
    global video
    global start
    while True:
        if start:
            start = False
            video = Pi_Stream.pi_objs[0].video_stream
        else:           
            for obj in Pi_Stream.pi_objs:
                if obj.faces:
                    video = obj.video_stream
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
        bytearray(video) + b'\r\n')
            



@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(gen(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    
    socketListener = threading.Thread(target=start_thread)
    socketListener.start()
    faceDetect = threading.Thread(target=Pi_Stream.face_detect)
    faceDetect.start()
    app.run(host='0.0.0.0', debug=False)
    