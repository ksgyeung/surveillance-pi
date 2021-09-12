import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import time

_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)
_FONT_SIZE = 48

def load_font(path):
    return ImageFont.truetype(path, _FONT_SIZE)


def draw_text(frame, width, height, font, text):
    return draw_text_cv(frame, width, height, font, text)

def draw_text_pil(frame, width, height, font, text):
    #p = time.time()

    image = Image.fromarray(frame)
    draw = ImageDraw.Draw(image)
    
    draw.text( 
        xy=(30, 30), 
        text=text, 
        font=font, 
        fill=_WHITE,
        stroke_width=1,
        stroke_fill=_BLACK
    )
    
    ret = np.array(image)
    #print(time.time() - p)

    return ret

def draw_text_cv(frame, width, height, font, text):
    ret = frame

    lines = text.split('\n')
    top=60

    for line in lines:
        #p = time.time()
        for x in range(-2, 2):
            for y in range(-2, 2):
                ret = cv2.putText(ret, line, (30 + x, top + y), cv2.FONT_HERSHEY_SIMPLEX, 1, _BLACK, 1, cv2.LINE_AA)
        
        ret = cv2.putText(ret, line, (30, top), cv2.FONT_HERSHEY_SIMPLEX, 1, _WHITE, 1, cv2.LINE_AA)
        top = top + _FONT_SIZE + 8
        #print(time.time() - p)
    return ret