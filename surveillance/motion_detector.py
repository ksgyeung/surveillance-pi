import cv2

from .detect_frame import DetectFrame
from .frame import Frame
from .rect import Rect
from .timebase_fps_counter import TimeBaseFpsCounter

_RATIO = 3
_BLUR = 21

def make_detect_frame(frame: Frame, counter: TimeBaseFpsCounter) -> DetectFrame:
    with counter:
        width, height = frame.frame.shape[1], frame.frame.shape[0]

        process_frame = frame.frame
        process_frame = cv2.resize(process_frame, (int(width / _RATIO), int(height / _RATIO)))
        process_frame = cv2.cvtColor(process_frame, cv2.COLOR_BGR2GRAY)
        process_frame = cv2.GaussianBlur(process_frame, (_BLUR, _BLUR), 0)
        
        return DetectFrame(frame=process_frame, time=frame.timestamp)

def detect_motion(a: DetectFrame, b: DetectFrame, counter: TimeBaseFpsCounter):
    with counter:
        ret = list()

        if a is None or b is None:
            return ret

        diff_frame = cv2.absdiff(a.frame, b.frame)
        _, thresh_frame = cv2.threshold(diff_frame, 5, 255, cv2.THRESH_BINARY)
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
        contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 2500:
                continue

            (x, y, w, h) = cv2.boundingRect(contour)
            (x, y, w, h) = (x * _RATIO, y * _RATIO, w * _RATIO, h * _RATIO)
            ret.append(Rect(x, y, w, h))

        return ret