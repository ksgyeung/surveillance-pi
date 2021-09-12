import time

class FpsStabliser:
    def __init__(self, fps) -> None:
        self._frame_ns = (1 / fps) * (10 ** 9)
        self._time = None

    def stablise(self):
        if self._time is not None:
            now = time.time_ns()
            delta = now - self._time
            if delta < self._frame_ns:
                sleep = (self._frame_ns - delta) / (10 ** 9); 
                #print('delta {}'.format(sleep))
                sleep = sleep * 0.95
                time.sleep(sleep)
        self._time = time.time_ns()
    