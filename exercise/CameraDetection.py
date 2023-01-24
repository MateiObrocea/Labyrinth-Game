import cv2
import numpy as np
import math


class CameraDetection:
    """
        Clas which dictates the movement of the player
        Computes an angle between 2 objects of specific different colors
        Code inspired by botforge
        """

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
        Determines the approximated outline and position of the first color
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_lowerbound = np.array([40, 40, 40])
        hsv_upperbound = np.array([80, 255, 255])  # green color bounds
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
        Determines the approximated outline and position of the first color
        """
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_lowerbound = np.array([90, 60, 80])
        hsv_upperbound = np.array([125, 255, 255])  # blue color bounds
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
        # saves a copy of the frame, since the image is changing
        copy_frame = orig_frame.copy()
        (color1_x, color1_y), found_color1 = self.find_color1(copy_frame)
        (color2_x, color2_y), found_color2 = self.find_color2(copy_frame)


        if found_color2 and found_color1:
            # calculates the angle between the 2 colors, using trigonometry
            hypotenuse = self.distance(color1_x, color1_x, color2_x, color2_y)
            horizontal = self.distance(color1_x, color1_y, color2_x, color1_y)
            vertical = self.distance(color2_x, color2_y, color2_x, color1_y)
            if hypotenuse != 0: # avoid division by 0
                if -1 < vertical / hypotenuse < 1: # constrain the arg of the arcsine
                    angle = np.arcsin(vertical / hypotenuse) * 180.0 / math.pi

                    # draw all 3 lines - display and debugging
                    cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 2)
                    cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color1_y), (0, 0, 255), 2)
                    cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 2)

                    angle_final = 0

                    if isinstance(angle, float) and angle < 360:
                        if color2_y < color1_y and color2_x > color1_x:
                            angle_final = int(angle)
                        elif color2_y < color1_y and color2_x < color1_x:
                            angle_final = int(180 - angle)
                        elif color2_y > color1_y and color2_x < color1_x:
                            angle_final = int(180 + angle)
                        elif color2_y > color1_y and color2_x > color1_x:
                            angle_final = int(360 - angle)

                    if 45 < angle_final < 135:
                        self.direction = 0
                    elif 135 < angle_final < 225:
                        self.direction = 1
                    elif 225 < angle_final < 315:
                        self.direction = 2
                    else:
                        self.direction = 3
        else:
            self.direction = 10
        cv2.waitKey(5)

