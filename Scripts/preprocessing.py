import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

import cv2 as cv

from ROI_selection import detect_lines

import numpy as np

def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def get_binary(image):
    (thresh, blackAndWhiteImage) = cv.threshold(image, 100, 255, cv.THRESH_BINARY)
    return blackAndWhiteImage

def get_cropped_image(image, x, y, w, h):
    cropped_image = image[ y:y+h , x:x+w ]
    return cropped_image

def invert_area(image, x, y, w, h):
    ones = np.copy(image)
    ones = 255
    
    image[ y:y+h , x:x+w ] = ones - image[ y:y+h , x:x+w ] 
    cv.imshow("detect", image)
    #cv.imshow("ROI", cFrame)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    
def detect(bw_frame, x, y, cell_w, cell_h, index = 0, display=False, write_to_file=False):
    cropped_frame = get_cropped_image(bw_frame, x, y, cell_w, cell_h)
    
    cFrame = np.copy(bw_frame)

    text = pytesseract.image_to_string(cropped_frame, lang='eng', config='--psm 10')        
    cv.rectangle(cFrame, (x, y), (x+cell_w, y+cell_h), (255, 0, 0), 2)
    cv.putText(cFrame, "text: " + text, (50, 50), cv.FONT_HERSHEY_SIMPLEX,  
                       2, (0, 0, 0), 5, cv.LINE_AA)     
    if (display): 
        cv.imshow("detect", cropped_frame)
        #cv.imshow("ROI", cFrame)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    if (write_to_file):
        cv.imwrite("../Images/"+ str(index) + ".png", cFrame);
        
    return text

def detect_number(frame, x, y, cell_w, cell_h, index = 0, display=False, write_to_file=False):
    gray = get_grayscale(frame)
    bw = get_binary(gray)
    cropped_frame = get_cropped_image(bw, x, y, cell_w, cell_h)
    
    cFrame = np.copy(frame)

    text = pytesseract.image_to_string(cropped_frame, lang = 'eng', config ='-c tessedit_char_whitelist=0123456789 --psm 10 --oem 1')
    cv.rectangle(cFrame, (x, y), (x+cell_w, y+cell_h), (255, 0, 0), 2)
    cv.putText(cFrame, "text: " + text, (50, 50), cv.FONT_HERSHEY_SIMPLEX,  
                       2, (0, 0, 0), 5, cv.LINE_AA) 
    
    if (display): 
        cv.imshow("detect", cropped_frame)
        #cv.imshow("ROI", cFrame)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    if (write_to_file):
        cv.imwrite("../Images/"+ str(index) + ".png", cFrame);
        
    return text

def main():
    filename = '../Images/source7.png'
    
    src = cv.imread(cv.samples.findFile(filename))
    horizontal, vertical = detect_lines(src)
    
    offset = 4
    
    x1 = vertical[17][2] + offset
    y1 = horizontal[0][3] + offset
    x2 = vertical[20][2] - offset
    y2 = horizontal[-1][3] -offset
    
    w = x2 - x1
    h = y2 - y1
    
    gray = get_grayscale(src)
    bw = get_binary(gray)
    bw = invert_area(bw, x1, y1, w, h)
    
    keywords = ['no', 'kabupaten', 'kb_otg', 'kl_otg', 'sm_otg', 'ks_otg', 'not_cvd_otg',
            'kb_odp', 'kl_odp', 'sm_odp', 'ks_odp', 'not_cvd_odp',
            'kb_pdp', 'kl_pdp', 'sm_pdp', 'ks_pdp', 'not_cvd_pdp',
            'positif', 'sembuh', 'meninggal']
    
    dict_kabupaten = {}
    
    for keyword in keywords:
        dict_kabupaten[keyword] = []
    
    counter = 0
            
    #text = detect(src, x1, y1, w, h, counter, display=True)
    
    print(dict_kabupaten)
    return 0
    
if __name__ == "__main__":
    main()
