"""
USES OPENCV 4.10, PROBABLY WILL WORK FOR OPENCV 2.70 and up
REMEMBER TO CALCULATE THE HSV BOUNDS FOR color1 & color2, use the trackbar:
https://gist.github.com/botforge/c6559abd3c48bceb78c2664dcb53cef6
to get these values
"""
import cv2
import numpy as np
import math


class CameraDetection:

    def __init__(self):
        self.direction = 10  # random nr outside the direction

    def distance(self, x1, y1, x2, y2):
        """
        Calculate distance between two points
        """
        dist = math.sqrt(math.fabs(x2 - x1) ** 2 + math.fabs(y2 - y1) ** 2)
        return dist

    def find_color1(self, frame):
        """
        Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
        """
        """
        red color
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_lowerbound = np.array([0, 120, 120])  # replace THIS LINE w/ your hsv lowerb
        hsv_upperbound = np.array([40, 255, 255])  # replace THIS LINE w/ your hsv upperb
        mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
        res = cv2.bitwise_and(frame, frame, mask=mask)  # filter inplace
        cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            maxcontour = max(cnts, key=cv2.contourArea)

            # Find center of the contour
            M = cv2.moments(maxcontour)
            if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return (cx, cy), True
            else:
                # pass
                return (1700, 1700), False  # faraway point
        else:
            # return False
            return (1700, 1700), False  # faraway point

    def find_color2(self, frame):
        """
        Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
        """

        """
        blue color
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_lowerbound = np.array([90, 80, 120])  # replace THIS LINE w/ your hsv lowerb
        hsv_upperbound = np.array([125, 255, 255])  # replace THIS LINE w/ your hsv upperb
        mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            maxcontour = max(cnts, key=cv2.contourArea)

            # Find center of the contour
            M = cv2.moments(maxcontour)
            if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                return (cx, cy), True  # True
            else:
                # pass
                return (1700, 1700), False  # faraway point
        else:
            return (1700, 1700), False  # faraway point

    cap = cv2.VideoCapture(0)

    def perform(self):
        _, orig_frame = self.cap.read()
        # we'll be inplace modifying frames, so save a copy
        copy_frame = orig_frame.copy()
        (color1_x, color1_y), found_color1 = self.find_color1(copy_frame)
        (color2_x, color2_y), found_color2 = self.find_color2(copy_frame)

        # draw circles around these objects
        cv2.circle(copy_frame, (color1_x, color1_y), 20, (255, 0, 0), -1)
        cv2.circle(copy_frame, (color2_x, color2_y), 20, (0, 128, 255), -1)

        if found_color2 and found_color1:
            # trig stuff to get the line
            hypotenuse = self.distance(color1_x, color1_x, color2_x, color2_y)
            horizontal = self.distance(color1_x, color1_y, color2_x, color1_y)
            vertical = self.distance(color2_x, color2_y, color2_x, color1_y)
            if hypotenuse != 0:
                if -1 < vertical / hypotenuse < 1:
                    angle = np.arcsin(vertical / hypotenuse) * 180.0 / math.pi
                    # print("angle is float")

                    # draw all 3 lines
                    cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 2)
                    cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color1_y), (0, 0, 255), 2)
                    cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 2)

                    # put angle text (allow for calculations upto 180 degrees)
                    angle_text = ""
                    angle_final = 0

                    if isinstance(angle, float) and angle < 360:
                        if color2_y < color1_y and color2_x > color1_x:
                            angle_final = int(angle)
                            angle_text = str(int(angle))
                        elif color2_y < color1_y and color2_x < color1_x:
                            angle_final = int(180 - angle)
                            angle_text = str(int(180 - angle))
                        elif color2_y > color1_y and color2_x < color1_x:
                            angle_final = int(180 + angle)
                            angle_text = str(int(180 + angle))
                        elif color2_y > color1_y and color2_x > color1_x:
                            angle_final = int(360 - angle)
                            angle_text = str(int(360 - angle))
                        # except:
                        #     print("conversion error"
                    if 45 < angle_final < 135:
                        print("North")
                        self.direction = 0
                    elif 135 < angle_final < 225:
                        print("East")
                        self.direction = 1
                    elif 225 < angle_final < 315:
                        print("South")
                        self.direction = 2
                    else:
                        print("West")
                        self.direction = 3

                    # print(self.direction)

                    # CHANGE FONT HERE
                    cv2.putText(copy_frame, angle_text, (color1_x - 30, color1_y), cv2.FONT_HERSHEY_COMPLEX, 1,
                                (0, 128, 229), 2)
        else:
            self.direction = 10

        # cv2.imshow('mat', copy_frame)
        cv2.waitKey(5)

        # while (1):
        #     self.perform()

    # cap.release()
    # cv2.destroyAllWindows()
