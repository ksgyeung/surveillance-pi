from surveillance.frame import Frame
from surveillance import detect_frame, frame_queue
import cv2
from os import path
import sys
import time
from datetime import datetime
import signal 
import statistics

from .buffered_videocapture import BufferedVideoCapture
from .fps_counter import FpsCounter
from .fps_stabliser import FpsStabliser
from . import motion_detector
from . import frame_draw
from .background_task import BackgroundTask, STATE_IDLE, STATE_RUNNING, STATE_RESULT_AVAILABLE
from .buffered_videowriter import BufferedVideoWriter
from .timebase_fps_counter import TimeBaseFpsCounter
from .task_worker import TaskWorker
from .frame_queue import FrameQueue

FPS = 30
WIDTH = 1920
HEIGHT = 1080

def file_time(time: int) -> str:
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d-%H-%M-%S')

def frame_time(time: int) -> str:
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

loop = True

def handle_ctrl_c(sig, frame):
    global loop
    if not loop:
        print('force quit')
        sys.exit(1)
    loop = False
    print('ctrl c pressed')

def run(root):
    signal.signal(signal.SIGINT, handle_ctrl_c)

    fourcc = cv2.VideoWriter_fourcc(*'H264')

    camera = 2
    cap = BufferedVideoCapture(path.join(root, 'demo30.mkv'), 30)
    #cap = BufferedVideoCapture(2, 30)
    if not cap.isOpened():
        print('Canont open capture')
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    #cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.start()


    print('Opening capture '.format(camera))

    fps_stabliser = FpsStabliser(FPS)
    fps_counter = FpsCounter()

    background_task3 = BackgroundTask()
    background_task3_fps_counter = TimeBaseFpsCounter()
    background_task3_task_worker = TaskWorker(background_task3_fps_counter)

    frame_queue = FrameQueue()

    last_detected_time = None
    last_detected_rects = None
    #detected_time_list = []
    recent_detected_count = 0
    recent_detected_count_sec = 0

    video_recoder = None

    try:
        while loop:
            now = time.time()
            #detected_time_list = list(filter(lambda x: x >= now - 1800 , detected_time_list))

            fps_counter.tick(callback=lambda fps: print('FPS: {}'.format(fps)))
            fps_stabliser.stablise()

            if background_task3.state() == STATE_RESULT_AVAILABLE:
                detected_rects = background_task3.result()
                background_task3.clear_result()

                if detected_rects is not None:
                    if len(detected_rects) > 0:
                        last_detected_time = now
                        last_detected_rects = detected_rects
                        #detected_time_list.append(now)
                        recent_detected_count += 1
                    else:
                        if recent_detected_count > 0:
                            recent_detected_count -= 1

            ret, frame = cap.read()
            if not ret:
                break

            frame_queue.push(frame)
            #print('{}x{}'.format(frame.frame.shape[0], frame.frame.shape[1]))
            

            if fps_counter.fps() % (FPS / 10) == 0 and background_task3.state() == STATE_IDLE:
                background_task3.submit_task(background_task3_task_worker.push, frame)

            #if len(list(filter(lambda x: x >= now - 1, detected_time_list))) > int(FPS * 0.1):
            if recent_detected_count > 0:
                if video_recoder is None:
                    print('motion triggered')
                    filename = '{}.mkv'.format(file_time(last_detected_time))
                    save_path = path.join(root, filename)
                    video_recoder = BufferedVideoWriter(fourcc, save_path, FPS, WIDTH, HEIGHT)
                    
            
            frame = frame_draw.draw_text(frame, '{}\n{}'.format('pipi', frame_time(frame.timestamp)), 1, 30, 30)
            if last_detected_rects is not None:
                for rect in last_detected_rects:
                    frame_draw.draw_rect(frame, rect)
            if video_recoder is not None:
                
                # consume all buffered frame
                for x, _ in frame_queue:
                    video_recoder.write(x)
                video_recoder.write(frame)
                pass

            cv2.imshow('frame', frame.frame)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()

        cap.release()
        if video_recoder is not None:
            video_recoder.release()
        
        background_task3.shutdown()

    avg_fps = round(statistics.mean(fps_counter.stat()), 2)
    #bg1_avg_fps = round(statistics.mean(background_task1_fps_counter.stat()), 2)
    #bg2_avg_fps = round(statistics.mean(background_task2_fps_counter.stat()), 2)
    bg3_avg_fps = round(statistics.mean(background_task3_fps_counter.stat()), 2)

    print('MAIN AVG FPS: {} {}'.format(avg_fps, 'PASS' if avg_fps >= (FPS - 5) else 'Not good'))
    #print('BG1 AVG FPS: {} {}'.format(bg1_avg_fps, 'PASS' if bg1_avg_fps >= FPS else 'FAIL'))
    #print('BG2 AVG FPS: {} {}'.format(bg2_avg_fps, 'PASS' if bg2_avg_fps >= FPS else 'FAIL'))
    print('BG3 AVG FPS: {} {}'.format(bg3_avg_fps, 'PASS' if bg3_avg_fps >= FPS else 'GOOD'))
