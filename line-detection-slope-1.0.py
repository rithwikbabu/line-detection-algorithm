import cv2
import numpy as np
import math
from statistics import median

def getSlope(val1, val2):
    if math.isclose(val1[0], val2[0], abs_tol=10) is False:
        slope = (val2[1] - val1[1]) / (val2[0] - val1[0])
    else:
        slope = 999
    return slope


def coord_sort(cords_input):
    coord_sorted = list()
    coord_unsorted = list(cords_input)
    curr_coord = ()
    tempcurr_cord = ()
    hypot = 99999

    for val in coord_unsorted:
        valhypot = math.sqrt(val[0] * val[1])
        hypot = min(valhypot, hypot)

        if hypot == valhypot:
            curr_coord = val

    if len(coord_unsorted) != 0:
        coord_unsorted.remove(curr_coord)
        coord_sorted.append(curr_coord)

    for x in range(9999):
        if len(coord_unsorted) == 0:
            break

        tempcurr_cord = coord_unsorted[0]
        hypot = 9999
        minval = 9999
        for val in coord_unsorted:
            valhypot = math.sqrt(abs((curr_coord[0] - val[0]) * (curr_coord[1] - val[1])))
            hypot = min(valhypot, hypot)

            if hypot == valhypot:
                if tempcurr_cord[0] == val[0]:
                    minval = min(minval, abs(curr_coord[1] - val[1]))
                    if abs(curr_coord[1] - val[1]) == minval:
                        tempcurr_cord = val

                elif tempcurr_cord[1] == val[1]:
                    minval = min(minval, abs(curr_coord[0] - val[0]))
                    if abs(curr_coord[0] - val[0]) == minval:
                        tempcurr_cord = val

                else:
                    tempcurr_cord = val

        curr_coord = tempcurr_cord
        coord_unsorted.remove(curr_coord)
        coord_sorted.append(curr_coord)

        if len(coord_unsorted) < 0:
            break

    slopes_list = list()
    for x in range(len(coord_sorted) - 1):
        slope = getSlope(coord_sorted[x], coord_sorted[x + 1])
        slopes_list.append(slope)

    k = 1
    if len(coord_sorted) > 0:
        for slopenum in range(len(slopes_list)):
            if math.isclose(slopes_list[slopenum], median(slopes_list), abs_tol=10) is False:
                k -= 1
                coord_sorted.pop(slopenum + k)

    return coord_sorted


cv2.namedWindow("preview")
cap = cv2.VideoCapture(0)

i = 0
marked_points = list()
while 1:
    i += 1
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    # lower_blue = np.array([0, 70, 50])
    lower_blue = np.array([0, 150, 75])
    upper_blue = np.array([5, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('mask', mask)
    coord = cv2.findNonZero(mask)

    # cv2.imshow('res', res)

    start_point = (0, 0)
    end_point = (0, 0)

    points_list = list()
    if coord is not None:
        for ind in range(int(coord.size / 2 - 1)):
            points = list()
            for x in coord[ind][0]:
                points.append(x)
            points_list.append(tuple(points))

    val1 = (0, 0)
    val2 = (0, 0)

    points_list_us = points_list
    points_list = coord_sort(points_list)
    if coord is not None:
        j = 0
        for val in points_list:
            j += 1
            if j // 2 == j / 2:
                val1 = val
            else:
                val2 = val
            if j > 3:
                cv2.line(frame, val1, val2, (255, 0, 0), 2)

    # if coord is not None:
    #     j = 0
    #     for val in points_list_us:
    #         j += 1
    #         if j // 2 == j / 2:
    #             val1 = val
    #         else:
    #             val2 = val
    #         if j > 3:
    #             cv2.line(frame, val1, val2, (0, 0, 255), 2)
    cv2.imshow('framesorted', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        print(points_list)
        break

cv2.destroyAllWindows()

