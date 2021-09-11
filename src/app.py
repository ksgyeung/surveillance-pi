from os import close
import sys
import cv2
import json
import signal
import time

from config import DCConfig

loop = True

def init_config():
    file = open('config.json')
    data = json.load(file)
    file.close()

    return DCConfig(
        cameraIndex=data['cameraIndex'],
        smbhost=data['smbhost'],
        username=data['username'],
        password=data['password'],
        terminator=data['terminator']
    )

def handle_ctrl_c(sig, frame):
    global loop
    loop = False
    print('ctrl c pressed')

def run():
    # init config
    config = init_config()

    #prepare to open camera
    print('opening camera #' + str(config.cameraIndex))
    cap = cv2.VideoCapture(config.cameraIndex)
    if not cap.isOpened():
        print('cannot open camera ' + str(config.cameraIndex))
        sys.exit(1)


    # init for mp4 codec
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    # register signal
    signal.signal(signal.SIGINT, handle_ctrl_c)

    last_frame = None
    last_motion_timestamp = None
    video_writer = None

    # main loop for capturing image from camera and processing
    while(loop):
        current_time = int(time.time())

        ret, frame = cap.read()
        if not ret:
            print('Cannot read camera')
            break

        #cv2.imshow('diff_frame', frame)
        process_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        process_frame = cv2.GaussianBlur(process_frame, (21, 21), 0)

        if last_frame is not None:
            diff_frame = cv2.absdiff(last_frame, process_frame)
            _, thresh_frame = cv2.threshold(diff_frame, 5, 255, cv2.THRESH_BINARY)
            thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
            contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < 100:
                    continue

                #print('motion detected')
                (x, y, w, h) = cv2.boundingRect(contour)
                # making green rectangle around the moving object
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                last_motion_timestamp = current_time

        last_frame = process_frame
        last_motion_timestamp = current_time

        cv2.imshow('aaaa', frame)
        cv2.waitKey(1)
        
        if last_motion_timestamp is not None:
            if last_motion_timestamp < current_time - 3:
                if video_writer is not None:
                    video_writer.release()
                video_writer = None
            else:
                if video_writer is None:
                    #video_writer = cv2.VideoWriter('{}.avi'.format(current_time), fourcc, 23.0, (3840, 2160))
                    video_writer = cv2.VideoWriter('{}.avi'.format(current_time), fourcc, 30.0, (640, 480))
                    if not video_writer.isOpened():
                        print('cannot save video')
                        sys.exit(1)

        if video_writer is not None:
            video_writer.write(frame)


    #output = cv2.VideoWriter('output.mp4', fourcc, 30.0, (3840, 2160))
    cap.release()
    if video_writer is not None:
        video_writer.release()

"""
import cv2
 
capture = cv2.VideoCapture(2)
 
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
videoWriter = cv2.VideoWriter('video.avi', fourcc, 30.0, (640,480))
 
while (True):
 
    ret, frame = capture.read()
     
    if ret:
        cv2.imshow('video', frame)
        videoWriter.write(frame)
 
    if cv2.waitKey(1) == 27:
        break
 
capture.release()
videoWriter.release()
 
cv2.destroyAllWindows()
"""