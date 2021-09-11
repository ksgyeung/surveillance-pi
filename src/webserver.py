from flask import Flask, make_response
import cv2

app = Flask(__name__)


last_frame = None


@app.route('/')
def home():
    return 'OK'

@app.route('/lastframe')
def get_last_frame():
    retval, buffer = cv2.imencode('.png', last_frame)
    if retval:
        return make_response(buffer.tobytes())

    return 404



