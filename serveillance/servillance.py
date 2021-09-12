from os import close
import sys
import cv2
import json
import signal
import time
from os import path
import os
from datetime import datetime
import numpy as np
import statistics
import math

from .config import load_config
from . import globalvar
from .video_record import VideoRecord
from . import motion_detect
from . import message
from . import draw_text
from .fast_videocap import FastVideoCap

loop = True

def handle_ctrl_c(sig, frame):
    global loop
    if not loop:
        sys.exit(2)
    loop = False
    print('ctrl c pressed')

def run():
    # init config
    config = load_config() 

    #font = draw_text.load_font(path.join(path.join(globalvar.ROOT, 'font'), 'cwTeXYen-zhonly.ttf'))
    font = draw_text.load_font(path.join(path.join(globalvar.ROOT, 'font'), 'irohamaru-Medium.ttf'))

    # init for mp4 codec
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    video_record = VideoRecord(fourcc, config.fps, config.cwidth, config.cheight)
    video_record.start('test')
    for i in range(0, config.fps):
        video_record.write(np.zeros((config.cwidth, config.cheight, 3), np.uint8))
    video_record.stop()
    os.remove(path.join(globalvar.ROOT, 'test.mkv'))

    #prepare to open camera
    print('opening camera #' + str(config.cameraIndex))
    #cap = cv2.VideoCapture(config.cameraIndex) #FastVideoCap(config.cameraIndex)
    cap = cv2.VideoCapture(path.join(globalvar.ROOT, 'demo30.mkv'))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.cwidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.cheight)
    cap.set(cv2.CAP_PROP_FPS, config.fps)
    #cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # register signal
    signal.signal(signal.SIGINT, handle_ctrl_c)

    last_process_frame = None 
    last_detected_time = set()
    message_cooldown = 0
    fps_delay = 1 / config.fps
    counting_fps_unix_time = None
    counting_fps_unix_time_count = 0
    fps_counter = 0
    last_frame_time = None
    avg_time = []

    #cap.startBuffering()

    # main loop for capturing image from camera and processing
    while(loop):
        if last_frame_time is not None:
            delta = abs(time.time_ns() - last_frame_time) / (10 ** 9)
            if delta < fps_delay:
                sleep = abs(fps_delay * 0.9 - delta)
                #time.sleep(sleep)

            
        now_ms = time.time()
        now = int(now_ms)
        
        if counting_fps_unix_time != now:
            #print('FPS: ' + str(counting_fps_unix_time_count))
            counting_fps_unix_time = now
            counting_fps_unix_time_count = 0

        p = time.time()
        ret, frame = cap.read()
        #print(time.time() - p)
        last_frame_time = time.time_ns()

        if not ret:
            print('Cannot read camera')
            break


        globalvar.LAST_FRAME = frame

        if fps_counter % 2 == 0:
            process_frame = motion_detect.make_motion_detect_frame(frame, config.cwidth, config.cheight)
            if last_process_frame is not None:
                detected = motion_detect.detect_motion(frame, last_process_frame, process_frame)
                if detected > 0:
                    name = '{identifier}-{timestamp}'.format(identifier=config.identifier, timestamp=datetime.utcfromtimestamp(now).strftime('%Y-%m-%d-%H-%M-%S'))
                    #video_record.start(name)
                    last_detected_time.add(now)
            last_process_frame = process_frame
        fps_counter = fps_counter + 1
        

        if len(last_detected_time) > 10 and message_cooldown + 60 < now:
            msg = 'Motion detected execced 10 second on {identifier}'.format(identifier=config.identifier)
            #message.send_message(msg)
            print(msg)
            message_cooldown = now
        if len(last_detected_time) > 0 and now - min(last_detected_time) > 3600:
            last_detected_time = set(map(lambda x: x > now - 3600, last_detected_time))


        if video_record.is_recording():
            timestr = datetime.utcfromtimestamp(now).strftime(u'%Y-%m-%d %H:%M:%S.') + str(round(now_ms - now, 2))[2:]
            #timestr = datetime.utcfromtimestamp(now).strftime(u'%Y年%m月%d日 %H時%M分%S秒 %A %Z ') + str(round(now_ms - now, 2))[2:]
            text = '{identifier}\n{timestr}'.format(identifier=config.identifier, timestr=timestr)
            frame2 = draw_text.draw_text(frame, config.cwidth, config.cheight, font, text)
            
            #video_record.write(frame2)
            #cv2.imshow('frame', frame2)
            #cv2.waitKey(1)
        video_record.tick(15)

        counting_fps_unix_time_count = counting_fps_unix_time_count + 1
        avg_time.append(time.time() - p)
        

        #cv2.imshow('frame', frame)
        #cv2.waitKey(1)
        #time.sleep(fps_delay)

    cap.release()
    video_record.stop()

    avg_time = statistics.mean(avg_time)
    fps = 1 / avg_time
    print('avg ' + str(avg_time))
    print('fps ' + str(fps))

