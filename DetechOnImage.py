from ultralytics import YOLO
import cv2
import cvzone
import math
import os
from werkzeug.utils import secure_filename
classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()


class DetectOnImage:
    def __init__(self):
        pass

    def detect(self, img):
        model = YOLO('yolov8n.pt')
        results = model(img)
        for info in results:
            parameters = info.boxes
            for box in parameters:
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = box.conf[0]
                class_detect = box.cls[0]
                class_detect = int(class_detect)
                class_detect = classnames[class_detect]
                conf = math.ceil(confidence * 100)

                if conf > 60:
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w, h = x2-x1, y2-y1
                    cvzone.cornerRect(img, (x1, y1, w, h), rt=9)
                    cvzone.putTextRect(img, f'{class_detect}', [x1 + 8, y1 + 30],
                                       scale=3, thickness=3,)

                    cv2.imwrite(os.path.join(
                        'static', 'detected.jpg'), img)


# image = '4.jpeg'
# DetectOnImage().detect(image)
