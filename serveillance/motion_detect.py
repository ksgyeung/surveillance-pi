import cv2
import time

def make_motion_detect_frame(frame, width, height):
    process_frame = frame
    process_frame = cv2.resize(process_frame, (int(width / 3), int(height / 3)))
    process_frame = cv2.cvtColor(process_frame, cv2.COLOR_BGR2GRAY)
    process_frame = cv2.GaussianBlur(process_frame, (11, 11), 0)
    #process_frame = cv2.blur(process_frame, (5, 5))
    #process_frame = cv2.resize(process_frame, (1280, 720), interpolation=cv2.INTER_NEAREST)
    return process_frame

def detect_motion(frame, motion_detect_frame_a, motion_detect_frame_b):
    if motion_detect_frame_a is None or motion_detect_frame_b is None:
        return 0

    detected = 0

    diff_frame = cv2.absdiff(motion_detect_frame_a, motion_detect_frame_b)
    _, thresh_frame = cv2.threshold(diff_frame, 5, 255, cv2.THRESH_BINARY)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 2500:
            continue

        detected = detected + 1
        #print('motion detected')
        #(x, y, w, h) = cv2.boundingRect(contour)
        #(x, y, w, h) = (x * 3, y * 3, w * 3, h * 3)
        # making green rectangle around the moving object
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    return detected

