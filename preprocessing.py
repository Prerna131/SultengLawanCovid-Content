import pytesseract
from pytesseract import Output
import cv2 as cv

from matplotlib import pyplot as plt

def detect(frame, x, y, cell_w, cell_h):
    cropped_frame = frame[ y:y+cell_h , x:x+cell_w]
    title = str(x) + ", " + str(y) + ".jpg"
    cv.imwrite("../Images/"+title, cropped_frame);
    text = pytesseract.image_to_string(cropped_frame, lang='eng', config='--psm 10')
    return text

def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def get_binary(image):
    (thresh, blackAndWhiteImage) = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)
    return blackAndWhiteImage

def get_rgb(image):
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)

def get_regions_ROI(image, x, y, w, h):
    cropped_image = image[ y:y+h , x:x+w ]
    cv.imshow("cropped_image", cropped_image)
    return cropped_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

image = cv.imread("../Images/source2.png")

nb_image = 1

images = []
for i in range (nb_image):
    title = "../Images/source" + str(i) + ".png"
    images.append(cv.imread(title))
    
offset_x = 25
offset_y = 5

keywords = ["Kabupaten/Kota", "Provinsi"]

box_keywords = {}

n_boxes = len(d['level'])
for i in range (nb_image):
    gray = get_grayscale(images[i])
    d = pytesseract.image_to_data(gray, output_type=Output.DICT, lang='eng')
    for j in range(n_boxes):
        text = d['text'][j]
        if(text in keywords):
            (x, y, w, h) = (d['left'][j], d['top'][j], d['width'][j], d['height'][j])
            x1 = x-offset_x
            x2 = x + w + offset_x
            y1 = y-offset_y
            y2 = y+h+offset_y
            box_keywords[text] = (x1, x2, y1, y2)
            cv.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.imshow('img'+str(i), gray)
            print(text + " || Loc: [" + str(x1) + ", " + str(x2) + "][" + str(y1) + ", " + str(y2) + "]")
            cv.waitKey(1)
            
print(box_keywords)

w = box_keywords['Kabupaten/Kota'][1] - box_keywords['Kabupaten/Kota'][0]
h = box_keywords['Provinsi'][3] - box_keywords['Kabupaten/Kota'][2]
x = box_keywords['Kabupaten/Kota'][0]
y = box_keywords['Kabupaten/Kota'][2]

#select the latest image
croppedImage = get_regions_ROI(images[i], x, y, w, h)

d = pytesseract.image_to_data(croppedImage, output_type=Output.DICT, lang='eng')
            
cv.waitKey(0)
cv.destroyAllWindows()