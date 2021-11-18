import PySimpleGUI as sg
import cv2
import numpy as np
import pyautogui as pg
import os
import sys
import HandTrackingModule as htm
import EyeTrackingModule as etm
import time
from collections import deque


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def display_main():

    layout = [[sg.Text('リアルタイム映像', size=(40, 1),  font='メイリオ 22', justification='center', key='-status-')],
              [sg.Text('カメラ番号: ', size=(8, 1)), sg.InputText(default_text='0', size=(4, 1), key='-camera_num-'), sg.Button('ジェスチャー認識 ON/OFF', key='-gesture-')],
              [sg.Image(filename='', key='-image-')],
              [sg.Text('', key='-description-')],
              [sg.Button('開始', key='-start-'), sg.Button('停止', key='-stop-'), sg.Button('ホーム', key='-home-')]
              ]

    recording = False
    gesture = False

    window = sg.Window('Blicky ―Hand&Eye Tracking Virtual Mouse―', layout=layout,  font='メイリオ', icon=resource_path('Blicky.ico'))
    
    previous_gesture = deque([])       # store gesture_id
    cool_time = 30      # cool time(frames) for gesture recognition
    gesture_accuracy = 0.8      # do action if the proportion of current gesture_id is higher than this value
    
    while True:
        event, values = window.read(timeout=0)
        if event == '-gesture-':
            gesture = not gesture
            
        if event in (None, '終了'):
            break

        elif event == '-start-':
            window['-status-'].update('Live')
            window['-description-'].update('※ 表示されているピンク色の枠がパソコンのフレームです')
            ##########################
            wCam, hCam = 640, 480
            frameR = 100  # Frame Reduction
            smoothening = 7
            #########################

            pTime = 0
            plocX, plocY = 0, 0
            clocX, clocY = 0, 0

            camera_number = int(values['-camera_num-'])
            cap = cv2.VideoCapture(camera_number, cv2.CAP_DSHOW)
            # cap = cv2.VideoCapture(camera_number)
            cap.set(3, wCam)
            cap.set(4, hCam)
            detector = htm.handDetector(detectionCon=0.5, trackCon=0.5)
            eyeDetector = etm.EyeDetector()
            wScr, hScr = pg.size()
            # print(wScr, hScr)
            recording = True

        elif event == '-stop-':
            window['-status-'].update("Stop")
            window['-description-'].update('')
            recording = False
            # 幅、高さ　戻り値Float
            W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # print(H,W)
            img = np.full((H, W), 0)
            # ndarry to bytes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['-image-'].update(data=imgbytes)
            cap.release()
            cv2.destroyAllWindows()

        elif event == '-home-':
            window.close()
            return True

        if recording:
            ret, img = cap.read()
            if ret is True:
                img = cv2.flip(img, 1)
                img = detector.findHands(img)
                lmList, point_history, bbox, gesture_id = detector.findPosition(img, gesture=gesture)

                # 2. Get the tip of the index and middle fingers
                if len(lmList) != 0:
                    # print(lmList)
                    x1, y1 = lmList[8][1:]
                    x2, y2 = lmList[12][1:]
                    # print(x1, y1, x2, y2)

                # 3. Check which fingers are up
                if len(lmList) != 0:
                    fingers = detector.fingersUp()

                    # print(fingers)
                    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
                    # 4. Only Index Finger : Moving Mode
                    if fingers[1] == 1 and fingers[2] == 0:
                        # 5. Convert Coordinates
                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                        # 6. Smoothen Values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening

                        # 7. Move Mouse
                        # pg.moveTo(wScr - clocX, clocY)
                        pg.moveTo(clocX, clocY)
                        cv2.circle(img, (x1, y1), 16, (255, 0, 255), cv2.FILLED)
                        for index, point in enumerate(point_history):
                            if point[0] != 0 and point[1] != 0:
                                cv2.circle(img, (point[0], point[1]), index, (255/16*index, 0, 255/16*index), 2)
                        plocX, plocY = clocX, clocY

                    # 8. Both Index and middle fingers are up : Clicking Mode
                    if fingers[1] == fingers[2]:
                        # 9. Find distance between fingers
                        length, img, lineInfo = detector.findDistance(8, 12, img)

                        # 10. Click mouse if distance short
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        if fingers[1] == 0:
                            length *= -1
                        try:
                            pg.scroll(int(5*length))
                        except Exception as e:
                            print(e)
                    
                    if gesture_id != -1:
                        previous_gesture.append(gesture_id)
                        if len(previous_gesture) >= cool_time:
                            previous_gesture.popleft()
                            # print(gesture_delay)
                            if previous_gesture.count(gesture_id)/len(previous_gesture) >= gesture_accuracy:
                                if gesture_id == 0:     # Heart
                                    pg.write('I love JPHACKS2021.')
                                elif gesture_id == 1:       # Triangle
                                    screenshot = pg.screenshot()
                                    screenshot.save('./screenshot.png')
                                previous_gesture = deque([])

                            
                # 9. Either left or right eye are closed : Clicking Mode
                ret, img2 = eyeDetector.findEyePosition(img)
                if ret == [-1, -1]:
                    img2 = img
                # 10. Left-click mouse if left eye are closed and Right-click mouse if right eye are closed
                elif ret == [1, 0]:
                    pg.leftClick()
                elif ret == [0, 1]:
                    pg.rightClick()

                # 11. Frame Rate
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img2, f'{int(fps)} FPS', (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (228, 223, 175), 2, cv2.LINE_AA)

                imgbytes = cv2.imencode('.png', img2)[1].tobytes()
                window['-image-'].update(data=imgbytes)

    window.close()


sg.theme('DarkAmber')

# ウィンドウの部品とレイアウト
layout = [
    [sg.Text('バーチャルマウスの基本操作方法', font=('Arial', 22), justification='center')],
    [sg.Text('▼ カーソル移動：人差し指を上げて動かす')],
    [sg.Image(filename=resource_path('move.png'), size=(330, 100), key='-img1-')],
    [sg.Text('▼ 左（右）クリック：左（右）目だけを閉じる')],
    [sg.Image(filename=resource_path('click.png'), size=(330, 100), key='-img2-')],
    [sg.Text('▼ 上（下）スクロール：ピースサイン上向き（下向き）')],
    [sg.Image(filename=resource_path('scroll.png'), size=(330, 100), key='-img3-')],
    [sg.Text('▼ 開発中①｜I love JPHACKS2021. と入力する：ハート💛を指で描く')],
    [sg.Text('▼ 開発中②｜スクリーンショットをとる：三角形🔺を指で描く')],
    [sg.Button('はじめる', key='-start-')],
]

# ウィンドウの生成
window = sg.Window('Blicky ―Hand&Eye Tracking Virtual Mouse', layout=layout, font='メイリオ', icon=resource_path('Blicky.ico'))


# イベントループ
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == "-start-":
        window.Hide()  # 説明画面を隠す
        # メイン画面を表示する
        main_return = display_main()
        # もしNoneが返ってきたら説明画面も終了させる
        if main_return is None:
            break
        elif main_return == True:
            window.UnHide()  # 説明画面を再表示する

window.close()
