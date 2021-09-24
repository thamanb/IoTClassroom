import threading
import socket
import struct
import numpy as np
import io
import cv2
import mediapipe as mp


class Pi_Stream:
    # static list to hold pi objects
    pi_objs = []

    @staticmethod
    def face_detect():
        while True:
            for obj in Pi_Stream.pi_objs:
                if obj.vid_frame_cnt >= 15:
                    obj.vid_frame_cnt = 0
                    with obj.mp_face_detection.FaceDetection(
                    model_selection=1, min_detection_confidence=0.5) as face_detection:
                        image = cv2.imdecode(obj.video_stream, 1)
                        obj.test = image
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False
                        results = face_detection.process(image)
                        if results.detections:
                            obj.face_count = results.detections
                            obj.faces = True    
                        else:
                            obj.face_count = 0
                            obj.faces = False
    
    def __init__(self, connection, addr):
        self.video_stream = 0
        self.vid_frame_cnt = 0
        self.audio_stream = 0
        self.face_count = 0
        self.faces = False
        self.connection = connection
        self.addr = addr
        self.pi_threads()
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        
        
    def pi_threads(self):
            vid_thread = threading.Thread(target=self.get_vid_stream)
            vid_thread.start()    
    

    def get_vid_stream(self):
        conn = self.connection.makefile('rb')
        while True:
            image_len = struct.unpack('<L', conn.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            image_stream = io.BytesIO()
            image_stream.write(conn.read(image_len))
            image_stream.seek(0)
            self.video_stream = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            self.vid_frame_cnt += 1
                    
                    
                    




    
