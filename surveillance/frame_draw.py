import cv2

from .frame import Frame
from .rect import Rect

_WHITE = (255,255,255)
_BLACK = (0,0,0)
_GREEN = (0,255,0)

def draw_text(frame: Frame, text: str, font_size: int, x: int, y: int) -> Frame:
    lines = text.split('\n')

    f = frame.frame
    line_offset = y

    for line in lines:
        text_size, base_line = cv2.getTextSize(
            text=line,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=font_size,
            thickness=1
        )

        if line_offset == y:
            line_offset += text_size[1] + base_line

        for x_offset in range(-2, 2):
            for y_offset in range(-2, 2):
                f = cv2.putText(
                    img=f, 
                    text=line, 
                    org=(x + x_offset, line_offset + y_offset), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=font_size, 
                    color=_WHITE, 
                    lineType=cv2.LINE_AA
                )

        f = cv2.putText(
            img=f, 
            text=line, 
            org=(x, line_offset), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=font_size, 
            color=_BLACK, 
            lineType=cv2.LINE_AA
        )

        line_offset += int(round(text_size[1] * 1.5))


    return Frame(frame=f, timestamp=frame.timestamp)
    

def draw_rect(frame: Frame, rect: Rect) -> Frame:
    #print(rect)
    cv2.rectangle(frame.frame, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), _GREEN, 1)
    return frame
    