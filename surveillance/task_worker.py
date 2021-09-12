from . import motion_detector
from .frame import Frame
from .timebase_fps_counter import TimeBaseFpsCounter

class TaskWorker:
    def __init__(self, counter:TimeBaseFpsCounter) -> None:
        self._frame = None
        self._counter = counter
        self._dummy = TimeBaseFpsCounter()

    def push(self, frame: Frame):
        with self._counter:
            if self._frame is None:
                self._frame = motion_detector.make_detect_frame(frame, self._dummy)
                return None

            frame = motion_detector.make_detect_frame(frame, self._dummy)
            return self.compute(self._frame, frame)
    
    def compute(self, frame1, frame2):
        rects = motion_detector.detect_motion(frame1, frame2, self._dummy)
        self._frame = None
        return rects
