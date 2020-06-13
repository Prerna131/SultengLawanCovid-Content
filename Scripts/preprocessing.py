try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import cv2 as cv

from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

image = cv.imread("../Images/source.png")

def detect(frame, x, y, cell_w, cell_h):
    cropped_frame = frame[ y:y+cell_h , x:x+cell_w]
    title = str(x) + ", " + str(y) + ".jpg"
    cv.imwrite("../Images/"+title, cropped_frame);
    text = pytesseract.image_to_string(cropped_frame, lang='eng', config='--psm 10')
    return text

im_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)

#cv.imwrite("../Images/bw.png", blackAndWhiteImage);

plt.imshow(blackAndWhiteImage, cmap='gray')

x = 650
y = 445
cell_height = 25
cell_width = 45

offset_x = [650, 720, 780, 850, 915, 985, 1040, 1110, 1180, 1248, 1320, 1400, 1480]

for offset in offset_x:
    text = detect(blackAndWhiteImage, offset, y, cell_width, cell_height)
    if(text=="G"):
        text = str(9)
    print(text)

#cv.waitKey(0)
#cv.destroyAllWindows()