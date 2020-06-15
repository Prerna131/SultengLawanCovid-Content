import pytesseract
from pytesseract import Output
import cv2 as cv

from matplotlib import pyplot as plt

def detect(frame, x, y, cell_w, cell_h):
    gray = get_grayscale(frame)
    bw = get_binary(gray)
    cropped_frame = bw[ y:y+cell_h , x:x+cell_w]
    
    #title = str(x) + ", " + str(y) + ".jpg"
    #cv.imwrite("../Images/"+title, cropped_frame);
    #cv.imshow("detect", cropped_frame)
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
    #cv.imshow("cropped_image", cropped_image)
    return cropped_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

image = cv.imread("../Images/source2.png")

images = []
image_index = 2
title = "../Images/source" + str(image_index) + ".png"
image = cv.imread(title)
    
keywords = ["Kabupaten/Kota", "Provinsi"]
box_keywords = {}

n_boxes = len(d['level'])
gray = get_grayscale(image)
d = pytesseract.image_to_data(gray, output_type=Output.DICT, lang='eng')
for j in range(n_boxes):
    text = d['text'][j]
    if(text in keywords):
        (x, y, w, h) = (d['left'][j], d['top'][j], d['width'][j], d['height'][j])
        offset_x = int(0.135*w)
        offset_y = int(0.135*h)
        x1 = x-offset_x
        x2 = x + w + offset_x
        y1 = y-offset_y
        y2 = y+h+offset_y
        box_keywords[text] = (x1, x2, y1, y2)
            
#print(box_keywords)

datum_w = box_keywords['Kabupaten/Kota'][1] - box_keywords['Kabupaten/Kota'][0]
datum_h = box_keywords['Provinsi'][3] - box_keywords['Kabupaten/Kota'][2]
datum_x = box_keywords['Kabupaten/Kota'][0]
datum_y = box_keywords['Kabupaten/Kota'][2]

#select the latest image
croppedImage = get_regions_ROI(image, datum_x, datum_y, datum_w, datum_h)
d = pytesseract.image_to_data(croppedImage, output_type=Output.DICT, lang='eng')

#print(d)
n_boxes = len(d['level'])
region_name = ""
kabupaten = {'data':[]}
index = 0

for j in range(n_boxes):
    text = d['text'][j]
    word_num = d['word_num'][j]
    if(word_num>0 and len(text)>2):
        (x, y, w, h) = (d['left'][j], d['top'][j], d['width'][j], d['height'][j])
        x1 = x + datum_x
        x2 = x + datum_x + w
        y1 = y + datum_y
        y2 = y + datum_y + h
            
        
        if ( d['word_num'][j] == 1):
            region_dict = {}                    
            region_name = text
            region_dict["no"] = index
            region_dict["name"] = region_name
            region_dict["box"] = [x1, y1, x2, y2]
            if(index>0):
                kabupaten['data'].append(region_dict)
            index += 1
            
        else:
            if(index>0):
                region_name += " " + text
                region_dict["name"] = region_name
                region_dict["box"][2] = x2
                region_dict["box"][3] = y2

for region in kabupaten['data']:
    cv.rectangle(image, (region["box"][0], region["box"][1]), (region["box"][2], region["box"][3]), (0, 255, 0), 2)
    

cv.imshow('img'+str(image_index), image)

index = 10
h_ori = kabupaten['data'][index]['box'][3] - kabupaten['data'][index]['box'][1]
offset_y = int(0.15*h_ori)
x = kabupaten['data'][index]['box'][0]
y = kabupaten['data'][index]['box'][1] - offset_y
h = int(h_ori *1.2)
w = image.shape[1] - x - 245
    
croppedImage = get_regions_ROI(image, x, y, w, h)
cv.imshow("cropped_image"+ str(index), croppedImage)
    
#plt.show(croppedImage)
detected = detect(image, x, y, w, h)
print(detected)

            
cv.waitKey(0)
cv.destroyAllWindows()