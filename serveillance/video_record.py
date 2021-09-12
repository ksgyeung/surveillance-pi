import cv2
from os import path
import time
from threading import Thread
from queue import Queue

from . import globalvar

_ENABLE_THREAD = True

def _unix():
    return int(time.time())

class VideoRecord:
    def __init__(self, fourcc, fps, width, height):
        self.__fourcc = fourcc
        self.__video_writer = None
        self.__unixtimestamp = None
        self.__fps = fps
        self.__width = width
        self.__height = height
        self._thread_flag = False
        self._thread = None
        self._queue = Queue()

    def is_recording(self):
        return self.__video_writer != None

    def start(self, name):
        if not self.is_recording():
            video_path = path.join(globalvar.ROOT, '{}.mkv'.format(name))
            self.__video_writer = cv2.VideoWriter(video_path, self.__fourcc, self.__fps, (self.__width, self.__height))
            if _ENABLE_THREAD:
                self._thread_flag = True
                self._thread = Thread(target=self._buffering)
                self._thread.start()
        self.__unixtimestamp = _unix()
    
    def write(self, frame):
        if self.is_recording():
            if _ENABLE_THREAD:
                if self._queue.full():
                    print('queue is full')
                    self._queue.get_nowait()
                self._queue.put(frame)
            else:
                self.__video_writer.write(frame)

    def stop(self):
        if self.is_recording():
            if _ENABLE_THREAD:
                self._thread_flag = False
                self._thread.join()
                self._thread = None
                self._queue = Queue()

            self.__video_writer.release()
            self.__video_writer = None
            self.__unixtimestamp = None

    def tick(self, second):
        if self.is_recording():
            now = _unix()
            if now > self.__unixtimestamp + second:
                self.stop()

    def _buffering(self):
        while self._thread_flag:
            try:
                frame = self._queue.get(timeout=1)
                self.__video_writer.write(frame)
            except:
                pass



