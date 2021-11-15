#Importing flask and OpenCVS. Also rendering template for camera.

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

#Selecting the capture device. "O" is for local camera. Could also use RTSP camera with IP.
camera = cv2.VideoCapture(0)

#Generate frame by frame from camera
def generate_frames():
    while True:
        # Using .read() to capture camera frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        # Link frame one by one and show the results.
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
