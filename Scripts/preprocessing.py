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

def detect(frame, x, y, cell_w, cell_h, index = 0, display=False, write_to_file=False):
    gray = get_grayscale(frame)
    bw = get_binary(gray)
    cropped_frame = get_cropped_image(bw, x, y, cell_w, cell_h)
    
    cFrame = np.copy(frame)

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

    text = pytesseract.image_to_string(cropped_frame, lang = 'eng', config ='-c tessedit_char_whitelist=0123456789 --psm 10 --oem 2')
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
    filename = '../Images/source1.png'
    
    src = cv.imread(cv.samples.findFile(filename))
    
    # Loads an image
    horizontal, vertical = detect_lines(src)
    
    offset = 4
    
    keywords = ['no', 'kabupaten', 'kb_otg', 'kl_otg', 'sm_otg', 'ks_otg', 'not_cvd_otg',
            'kb_odp', 'kl_odp', 'sm_odp', 'ks_odp', 'not_cvd_odp',
            'kb_pdp', 'kl_pdp', 'sm_pdp', 'ks_pdp', 'not_cvd_pdp',
            'positif', 'sembuh', 'meninggal']
    
    dict_kabupaten = {}
    
    for keyword in keywords:
        dict_kabupaten[keyword] = []
    
    counter = 0
    
    for i in range(1,14):
        for j, keyword in enumerate(keywords):
            counter += 1
            x1 = vertical[j][2] + offset
            y1 = horizontal[i][3] + offset
            x2 = vertical[j+1][2] - offset
            y2 = horizontal[i+1][3] -offset
            
            w = x2 - x1
            h = y2 - y1
            
            if (keyword=='kabupaten'):
                text = detect(src, x1, y1, w, h, counter, write_to_file=True)
                print("Not number, " + "Keyword: " + keyword + ", row: ", str(i), "text: ", text)
            else:
                text = detect_number(src, x1, y1, w, h, counter, write_to_file=True)
                print("Is number, " + "Keyword: " + keyword + ", row: ", str(i), "text: ", text)
                
            dict_kabupaten[keyword].append(text)
            
            
    print(dict_kabupaten)
    return 0
    
if __name__ == "__main__":
    main()
