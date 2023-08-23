import cv2
from pyzbar import pyzbar as bar

# image = cv2.imread('codes.png')


class Decode:
    def __init__(self):
        pass

    def barcode(image):
        OUTPUT = None
        result = bar.decode(image)
        for data in result:
            OUTPUT = data.data
            OUTPUT = OUTPUT.decode('utf-8')
        return OUTPUT


# text = Decode.barcode(image)
# print(text)
