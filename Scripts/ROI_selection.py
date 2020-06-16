# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:48:11 2020

@author: My Laptop
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:19:57 2020

@author: My Laptop
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:48:51 2020

@author: My Laptop
"""

"""
@file hough_lines.py
@brief This program demonstrates line finding with the Hough transform
"""
import sys
import math
import cv2 as cv
import numpy as np

def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]

def func1(x):
    return x[0]
    
def func2(x):
    return x[1]
    
def main(argv):
    
    default_file = '../Images/source0.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename))
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # Check if image is loaded fine
    if gray is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    dst = cv.Canny(gray, 50, 150, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    
    linesP = cv.HoughLinesP(dst, 1 , np.pi / 180, 50, None, 250, 6)
    
    horizontal_lines = []
    vertical_lines = []
    
    if linesP is not None:
        #for i in range(40, nb_lines):
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)
                
            elif (is_horizontal(l)):
                horizontal_lines.append(l)
    
    
        vertical_lines = sorted(vertical_lines, key=func1)
        horizontal_lines = sorted(horizontal_lines, key=func2)
    
        for i in range(len(vertical_lines)):
            l_curr = vertical_lines[i]
            if(i>0):
                l_prev = vertical_lines[i-1]
                if ( (l_curr[0] - l_prev[0]) > 5):
                    cv.line(cdstP, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,0,255), 3, cv.LINE_AA)
                    cv.line(src, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,0,255), 3, cv.LINE_AA)
                    
            else:
                cv.line(cdstP, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,0,255), 3, cv.LINE_AA)
                cv.line(src, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,0,255), 3, cv.LINE_AA)
                
        for i in range(len(horizontal_lines)):
            l_curr = horizontal_lines[i]
            if(i>0):
                l_prev = horizontal_lines[i-1]
                if ( (l_curr[3] - l_prev[3]) > 5):
                    cv.line(cdstP, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,255,0), 3, cv.LINE_AA)
                    cv.line(src, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,255,0), 3, cv.LINE_AA)
                    #cv.putText(src, str(l_curr[3]), (l_curr[0], l_curr[1]), font,  
                    #       fontScale, (0, 0, 0), thickness, cv.LINE_AA) 
            else:
                cv.line(cdstP, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,255,0), 3, cv.LINE_AA)
                cv.line(src, (l_curr[0], l_curr[1]), (l_curr[2], l_curr[3]), (0,255,0), 3, cv.LINE_AA)
                #cv.putText(src, str(l_curr[3]), (l_curr[0], l_curr[1]), font,  
                #       fontScale, (0, 0, 0), thickness, cv.LINE_AA) 
            
    cv.imshow("Source", src)
    cv.imshow("Canny", cdstP)
    cv.waitKey()
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])