#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import imagiz
import cv2
from EmotionDetection.face_detection import FaceClass

app = Flask(__name__)
server=imagiz.TCP_Server(8095)
server.start()
face_class = FaceClass()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    # import camera driver
    # Raspberry Pi camera module (requires picamera package)
    # from camera_pi import Camera
    if os.environ.get('CAMERA'):
        Camera = import_module('camera_' + os.environ['CAMERA']).Camera
    else:
        from camera import Camera
    camera = Camera()
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_streamed():
    while True:
        try:
            message=server.receive()
            if not message.image is None:     
                frame = cv2.imdecode(message.image,cv2.IMREAD_UNCHANGED)
                with_faces = face_class.find_faces(frame)
                img_str = cv2.imencode('.jpg', with_faces)[1].tostring()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img_str + b'\r\n')
        except:
            pass



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_streamed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
