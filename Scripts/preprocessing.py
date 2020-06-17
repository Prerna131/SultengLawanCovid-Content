import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

import cv2 as cv

from matplotlib import pyplot as plt

from ROI_selection import detect_lines

def detect(frame, x, y, cell_w, cell_h, display=False):
    gray = get_grayscale(frame)
    bw = get_binary(gray)
    cropped_frame = bw[ y:y+cell_h , x:x+cell_w]

    if (display): 
        cv.imshow("detect", cropped_frame)
        cv.rectangle(frame, (x, y), (x+cell_w, y+cell_h), (255, 0, 0), 2)
        cv.imshow("ROI", frame)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    text = pytesseract.image_to_string(cropped_frame, lang='eng', config='--psm 10')
    return text

def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def get_binary(image):
    (thresh, blackAndWhiteImage) = cv.threshold(image, 100, 255, cv.THRESH_BINARY)
    return blackAndWhiteImage

def get_rgb(image):
    return cv.cvtColor(image, cv.COLOR_BGR2RGB)

def get_regions_ROI(image, x, y, w, h):
    cropped_image = image[ y:y+h , x:x+w ]
    #cv.imshow("cropped_image", cropped_image)
    return cropped_image

def main():
    filename = '../Images/source6.png'
    
    src = cv.imread(cv.samples.findFile(filename))
    
    # Loads an image
    horizontal, vertical = detect_lines(src, display=True)
    
    print(vertical[0], vertical[1], horizontal[0], horizontal[1])
    
    offset = 2
    
    for i in range(1,15):
        x1 = vertical[1][2] + offset
        y1 = horizontal[i][3] + offset
        x2 = vertical[2][2] - offset
        y2 = horizontal[i+1][3] -offset
        
        w = x2 - x1
        h = y2 - y1
    
        text = detect(src, x1, y1, w, h)
        print(text)
    
    return 0
    
if __name__ == "__main__":
    main()
