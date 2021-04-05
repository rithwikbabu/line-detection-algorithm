import cv2
import numpy as np

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

    # define range of red color in HSV
    lower_red = np.array([0, 70, 50])
    # lower_red = np.array([0, 150, 75])
    upper_red = np.array([5, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('mask', mask)
    coord = cv2.findNonZero(mask)

    cv2.imshow('res', res)

    start_point = (0, 0)
    end_point = (0, 0)

    # if coord is not None:
    #     if (i//3 == i/3):
    #         start_point = ()
    #         l1 = list(start_point)
    #         for x in coord[0][0]:
    #             l1.append(x)
    #         start_point = tuple(l1)
    #         cv2.line(frame, start_point, (0, 0), (255, 0, 0), 2)
    #         cv2.line(frame, start_point, (640, 0), (255, 0, 0), 2)
    #         cv2.line(frame, start_point, (640, 480), (255, 0, 0), 2)
    #         cv2.line(frame, start_point, (0, 480), (255, 0, 0), 2)
    #
    # marked_points.append(start_point)
    #
    # for val in marked_points:
    #     cv2.circle(frame, val, 1,(0,0,255))

    points_list = list()
    if coord is not None:
        for ind in range(int(coord.size / 2 - 1)):
            points = list()
            for x in coord[ind][0]:
                points.append(x)
            points_list.append(tuple(points))

    val1 = (0, 0)
    val2 = (0, 0)

    if coord is not None:
        j = 0
        for val in points_list:
            j += 1
            if j // 2 == j / 2:
                val1 = val
            else:
                val2 = val
            print(val1, val2)
            if(j > 3):
                cv2.line(frame, val1, val2, (255, 0, 0), 2)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
