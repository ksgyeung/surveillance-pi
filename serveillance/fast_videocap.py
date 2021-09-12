from queue import Queue
from threading import Thread
import time
import cv2

class FastVideoCap:
    def __init__(self, index):
        self._is_buffering = False
        self._queue = Queue(60)
        self._v = cv2.VideoCapture(index)
        self._t = None
        if not self._v.isOpened():
            raise Exception('camera ' + str(index) + ' cannot be opened')
    
    def set(self, prop, val):
        self._v.set(prop, val)

    def startBuffering(self):
        if self._is_buffering:
            return
        self._is_buffering = True
        t = Thread(target=self._buffering)
        t.start()
        self._t = t

    def stopBuffering(self):
        self._is_buffering = False
        self._t.join()
    
    def _buffering(self):
        while self._is_buffering:
            ret, frame = self._v.read()
            if ret:
                if not self._queue.empty():
                    try:
                        self._queue.get_nowait()
                    except Queue.Empty:
                        pass
                self._queue.put(frame)
                #print('{}'.format(time.time()))

    def read(self):
        return True, self._queue.get()

    def release(self):
        self.stopBuffering()
        self._v.release()


