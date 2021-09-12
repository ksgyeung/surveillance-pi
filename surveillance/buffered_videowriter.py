import cv2
from queue import Queue
from threading import Thread

from .frame import Frame

class BufferedVideoWriter:
    def __init__(self, fourcc, filename, fps, width, height, queue_maxsize = 0) -> None:
        self._writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        self._queue = Queue(queue_maxsize)
        self._loop = True
        self._thread = Thread(target=self._target)
        self._thread.isDaemon = True
        self._thread.start()
        pass

    def set(self, prop, value):
        self._writer.set(prop, value)

    def write(self, frame: Frame):
        self._queue.put(frame)

    def release(self):
        self._loop = False
        self._thread.join()
        self._writer.release()
    
    def _target(self):
        while self._loop:
            while True:
                try:
                    frame = self._queue.get(timeout=1)
                    self._writer.write(frame.frame)
                except:
                    break

