import cv2
import numpy as np
from matplotlib import pyplot as plt


def findCorners(bound):
    c1 = [bound[3][0],bound[0][1]]
    c2 = [bound[1][0],bound[0][1]]
    c3 = [bound[1][0],bound[2][1]]
    c4 = [bound[3][0],bound[2][1]]
    return [c1,c2,c3,c4]

# def fillImage(img):
#     h, w = img.shape[:2]
#     mask = np.zeros((h+2,w+2),np.uint8)
#     im_ff = img.copy()
#
#     #find the contours in the image
#     contours, heirar = cv2.findContours(th3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#
#     for num in range(0,len(contours)):
#         if(heirar[0][num][3] != -1):
#             #find centroid of contour
#             cnt = contours[num]
#             #find the boundries of the contour
#             left = tuple(cnt[cnt[:,:,0].argmin()][0])
#             right = tuple(cnt[cnt[:,:,0].argmax()][0])
#             top = tuple(cnt[cnt[:,:,1].argmin()][0])
#             bottom = tuple(cnt[cnt[:,:,1].argmax()][0])
#             #find centere coordinates of cavity --- we can do better
#             cx = left[0] + (right[0] - left[0])/2
#             cy = top[1] + (bottom[1] - top[1])/2
#             #perform flood fill on the center of the contour
#             cv2.floodFill(im_ff,mask,(cx,cy),255)
#     return img | im_ff

if __name__ == "__main__":
    bndingBx = []#holds bounding box of each countour
    corners = []

    img = cv2.imread('const.png',0) #read image

    #perform gaussian blur (5*5)
    blur = cv2.GaussianBlur(img,(5,5),0)
    #use Otsu method for global threshold
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    th3 = cv2.bitwise_not(th3)
    # ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #reassign contours to the filled in image
    contours, heirar = cv2.findContours(th3, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    #find the rectangle around each contour
    # for cnt in contours:
    for num in range(0,len(contours)):
        #if(heirar[0][num][3] == -1):
        left = tuple(contours[num][contours[num][:,:,0].argmin()][0])
        right = tuple(contours[num][contours[num][:,:,0].argmax()][0])
        top = tuple(contours[num][contours[num][:,:,1].argmin()][0])
        bottom = tuple(contours[num][contours[num][:,:,1].argmax()][0])
        bndingBx.append([top,right,bottom,left])

    #find the edges of each bounding box
    for bx in bndingBx:
        corners.append(findCorners(bx))

    #draw the countours on thresholded image
    # total = cv2.drawContours(img, contours[-2], -1, (0,255,0), 2)
    x,y,w,h = cv2.boundingRect(th3)
    # img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    imgplot = plt.imshow(img,'gray')
    #draw the box
    for bx in corners:
        plt.plot([bx[0][0],bx[1][0]],[bx[0][1],bx[1][1]],'g-',linewidth=2)
        plt.plot([bx[1][0],bx[2][0]],[bx[1][1],bx[2][1]],'g-',linewidth=2)
        plt.plot([bx[2][0],bx[3][0]],[bx[2][1],bx[3][1]],'g-',linewidth=2)
        plt.plot([bx[3][0],bx[0][0]],[bx[3][1],bx[0][1]],'g-',linewidth=2)
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()