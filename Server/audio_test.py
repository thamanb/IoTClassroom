
from os import name
import io
import socket
import struct
from flask import Flask, render_template, Response
import numpy as np





#Sockets
server_socket = socket.socket()
server_socket.bind(('192.168.1.101', 5050))
server_socket.listen(0)

connection, addr = server_socket.accept()
#connection = connection[0].makefile('rb')




#Flask
app = Flask(__name__)

@app.route("/")
def home():
    return render_template ('index.html')

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o





def audio_gen():
        wav_header = genHeader(44110, 16, 1)
        first_run = True
        while True:
            data = connection.recv(2048)
            
            if first_run:
                audio_stream = wav_header + data
                first_run = False
                
            else:
                audio_stream = data
                
            yield(audio_stream)




@app.route('/audio')
def audio():
    return Response(audio_gen(),
        mimetype="audio/x-wav")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)