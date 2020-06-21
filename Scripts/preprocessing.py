import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

import cv2 as cv

from ROI_selection import detect_lines, get_ROI

import numpy as np

def get_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def get_binary(image):
    (thresh, blackAndWhiteImage) = cv.threshold(image, 100, 255, cv.THRESH_BINARY)
    return blackAndWhiteImage

def get_cropped_image(image, x, y, w, h):
    cropped_image = image[ y:y+h , x:x+w ]
    return cropped_image

def invert_area(image, x, y, w, h, display=False):
    ones = np.copy(image)
    ones = 1
    
    image[ y:y+h , x:x+w ] = ones*255 - image[ y:y+h , x:x+w ] 
    if (display): 
        cv.imshow("inverted", image)
        cv.waitKey(0)
        cv.destroyAllWindows()
    return image
    
def detect(bw, x, y, cell_w, cell_h, index = 0, is_number = False,
           display=False, write_to_file=False):
    cropped_frame = get_cropped_image(bw, x, y, cell_w, cell_h)
    
    cFrame = np.copy(bw)

    if (is_number):
        text = pytesseract.image_to_string(cropped_frame, lang = 'eng',
                                           config ='-c tessedit_char_whitelist=0123456789 --psm 10 --oem 1')
    else:
        text = pytesseract.image_to_string(cropped_frame, lang='eng', config='--psm 10')        
    
    if (display or write_to_file):
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
    
    ## invert area
    left_line_index = 17
    right_line_index = 20
    top_line_index = 0
    bottom_line_index = -1
    
    x, y, w, h = get_ROI(horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)
    
    gray = get_grayscale(src)
    bw = get_binary(gray)
    cv.imshow("bw", bw)
    bw = invert_area(bw, x, y, w, h, display=True)
    
    ## set keywords
    keywords = ['no', 'kabupaten', 'kb_otg', 'kl_otg', 'sm_otg', 'ks_otg', 'not_cvd_otg',
            'kb_odp', 'kl_odp', 'sm_odp', 'ks_odp', 'not_cvd_odp',
            'kb_pdp', 'kl_pdp', 'sm_pdp', 'ks_pdp', 'not_cvd_pdp',
            'positif', 'sembuh', 'meninggal']
    
    dict_kabupaten = {}
    for keyword in keywords:
        dict_kabupaten[keyword] = []
        
    ## set counter for image indexing
    counter = 0
    
    ## set line index
    first_line_index = 1
    last_line_index = 14
    
    ## read text
    for i in range(first_line_index, last_line_index):
        for j, keyword in enumerate(keywords):
            counter += 1
            
            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1
            
            x, y, w, h = get_ROI(horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)
            
            if (keywords[j]=='kabupaten'):
                text = detect(bw, x, y, w, h, index=counter)
                print("Not number, " + "Keyword: " + keyword + ", row: ", str(i), "text: ", text)
            else:
                text = detect(bw, x, y, w, h, index=counter, is_number=True)
                print("Is number, " + "Keyword: " + keyword + ", row: ", str(i), "text: ", text)
                
            ## add to dictionary
            dict_kabupaten[keyword].append(text)
    
    print(dict_kabupaten)
    return 0
    
if __name__ == "__main__":
    main()
