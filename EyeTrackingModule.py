import cv2
import numpy as np
import dlib


class EyeDetector():
    def __init__(self):
        # video setting and each definition
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.showSep = True
        self.showMidResult = True
        self.lastLeftOpen = 1
        self.curLeftOpen = 1
        self.lastRightOpen = 1
        self.curRightOpen = 1
        self.leftBlinkCount = 0
        self.rightBlinkCount = 0

    def eye_aspect_ratio(self, eye):
        # compute the distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        dv1 = pow(pow(eye[1].x - eye[5].x, 2) + pow(eye[1].y - eye[5].y, 2), 0.5)
        dv2 = pow(pow(eye[2].x - eye[4].x, 2) + pow(eye[2].y - eye[4].y, 2), 0.5)
        # compute the distance between the horizontal
        # eye landmark (x, y)-coordinates
        dl3 = pow(pow(eye[0].x - eye[3].x, 2) + pow(eye[0].y - eye[3].y, 2), 0.5)
        # compute and return the eye aspect ratio
        return (dv1 + dv2) / dl3

    def findEyePosition(self, img):
        # print("left", checkLeft, eyePredictor.leftBlinkCount, '\n')

        # 2. detect face
        dets = self.detector(img[:, :, ::-1])
        if len(dets) < 1:
            cv2.putText(img, "Please show more than half face", (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (61, 26, 237), 2, cv2.LINE_AA)
            # cv2.namedWindow("blink check", 0)
            # cv2.imshow("blink check", img)
            return [-1, -1], []

        parts = self.predictor(img, dets[0]).parts()
        # img = frame
        # if self.showSep:
        #     img = img * 0

        for i in parts:
            cv2.circle(img, (i.x, i.y), 3, (255, 0, 0), -1)

        # 3. find eye here
        # eye 1
        leftEye = [parts[36], parts[37], parts[38], parts[39], parts[40], parts[41]]
        for i in leftEye:
            cv2.circle(img, (i.x, i.y), 3, (0, 255, 0), -1)
        # eye 2
        rightEye = parts[42:48]
        for i in rightEye:
            cv2.circle(img, (i.x, i.y), 3, (0, 0, 255), -1)

        # if eyePredictor.showSep:
        #     cv2.namedWindow("detected", 1)
        #     cv2.imshow("detected", img)
        # else:
        #     cv2.destroyWindow("detected")

        closed = [0, 0]

        # 4. check blink
        checkLeft = self.eye_aspect_ratio(leftEye)
        lineColor = (25, 255, 90)

        if checkLeft < 0.3:
            self.curLeftOpen = 0
            lineColor = (61, 26, 237)
        else:
            self.curLeftOpen = 1
            lineColor = (25, 255, 90)

        if self.lastLeftOpen == 1 and self.curLeftOpen == 0:
            self.leftBlinkCount += 1
            closed[0] = 1
        self.lastLeftOpen = self.curLeftOpen

        for i in leftEye:
            cv2.circle(img, (i.x, i.y), 3, lineColor, -1)

        cv2.putText(img, "Left Blinks: {}".format(self.leftBlinkCount), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lineColor, 2, cv2.LINE_AA)
        # cv2.putText(img, "Eye ratio: {:.2f}".format(checkLeft), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lineColor, 2)

        # eye 2
        checkRight = self.eye_aspect_ratio(rightEye)

        lineColor = (25, 255, 90)
        if checkRight < 0.3:
            self.curRightOpen = 0
            lineColor = (61, 26, 237)
        else:
            self.curRightOpen = 1
            lineColor = (25, 255, 90)

        if self.curRightOpen == 0 and self.lastRightOpen == 1:
            self.rightBlinkCount += 1
            closed[1] = 1
        self.lastRightOpen = self.curRightOpen

        for i in rightEye:
            cv2.circle(img, (i.x, i.y), 3, lineColor, -1)

        if closed == [0, 1] and checkLeft < checkRight*1.2:
            closed = [1, 1]
        elif closed == [1, 0] and checkLeft*1.2 > checkRight:
            closed = [1, 1]

        # print("right", checkRight, eyePredictor.rightBlinkCount, '\n')

        cv2.putText(img, "Right Blinks: {}".format(self.rightBlinkCount), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lineColor, 2, cv2.LINE_AA)
        # cv2.putText(img, "Eye ratio: {:.2f}".format(checkRight), (300, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, lineColor, 2)

        return closed, img


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    eyePredictor = EyeDetector()

    while True:
        success, img = cap.read()

        # 1. Take each frame
        # ret, frame = cap.read()
        # cap.grab()
        # ret, frame = cap.retrieve()
        # if np.shape(frame) == ():
        #     continue

        # flip left and right if your camera need
        frame = cv2.flip(img, 1)

        ret, img = eyePredictor.findEyePosition(img)
        if ret == 0:
            continue

        # if eyePredictor.showSep:
        #     cv2.namedWindow("camera image", 0)
        #     cv2.imshow("camera image", frame)
        # else:
        #     cv2.destroyWindow("camera image")

        # 5. show out result
        cv2.namedWindow("blink check", 1)
        cv2.imshow("blink check", img)

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
