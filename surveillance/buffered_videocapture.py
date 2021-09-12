import cv2
from threading import Thread
from queue import Queue
import time
import numpy as np

from .frame import Frame

class BufferedVideoCapture:
    def __init__(self, param, queue_size = 0) -> None:
        self._cap = cv2.VideoCapture(param)
        self._queue = Queue(queue_size)
        self._running = True
        self._thread = Thread(target=self._target)
        self._thread.isDaemon = True
    
    def start(self):
        self._thread.start()

    def set(self, prop, value):
        print('setting props {} = {}'.format(prop, value))
        self._cap.set(prop, value)

    def get(self, prop) -> any:
        return self._cap.get(prop)

    def isOpened(self) -> bool:
        return self._cap.isOpened()

    def read(self) -> Frame:
        return self._queue.get()

    def release(self):
        self._running = False
        self._thread.join()
        self._cap.release()
        pass

    def _target(self):
        ret, frame = None, None

        while self._running:
            if ret is None:
                ret, frame = self._cap.read()
            try:
                if self._queue.full():
                    time.sleep(0.0001)
                    continue
            except:
                pass
            
            self._queue.put((ret, Frame(frame=frame, timestamp=time.time())))
            ret, frame = None, None


