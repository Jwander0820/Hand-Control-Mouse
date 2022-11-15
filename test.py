import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector  # 手部檢測方法
import time
import autopy

# （1）導數視頻數據
wScr, hScr = autopy.screen.size()  # 返回電腦屏幕的寬和高(1920.0, 1080.0)
wCam, hCam = 1280, 720  # 視頻顯示窗口的寬和高
pt1, pt2 = (100, 100), (1100, 500)  # 虛擬鼠標的移動範圍，左上座標pt1，右下座標pt2

cap = cv2.VideoCapture(0)  # 0代表自己電腦的攝像頭
cap.set(3, wCam)  # 設置顯示框的寬度1280
cap.set(4, hCam)  # 設置顯示框的高度720

pTime = 0  # 設置第一幀開始處理的起始時間

pLocx, pLocy = 0, 0  # 上一幀時的鼠標所在位置

smooth = 4  # 自定義平滑係數，讓鼠標移動平緩一些

# （2）接收手部檢測方法
detector = HandDetector(mode=False,  # 視頻流圖像
                        maxHands=1,  # 最多檢測一隻手
                        detectionCon=0.8,  # 最小檢測置信度
                        minTrackCon=0.5)  # 最小跟蹤置信度

# （3）處理每一幀圖像
while True:

    # 圖片是否成功接收、img幀圖像
    success, img = cap.read()

    # 翻轉圖像，使自身和攝像頭中的自己呈鏡像關係
    img = cv2.flip(img, flipCode=1)  # 1代表水平翻轉，0代表豎直翻轉

    # 在圖像窗口上創建一個矩形框，在該區域內移動鼠標
    cv2.rectangle(img, pt1, pt2, (0, 255, 255), 5)

    # （4）手部關鍵點檢測
    # 傳入每幀圖像, 返回手部關鍵點的座標信息(字典)，繪製關鍵點後的圖像
    hands, img = detector.findHands(img, flipType=False)  # 上面反轉過了，這裏就不用再翻轉了
    # print(hands)

    # 如果能檢測到手那麼就進行下一步
    if hands:

        # 獲取手部信息hands中的21個關鍵點信息
        lmList = hands[0]['lmList']  # hands是由N個字典組成的列表，字典包每隻手的關鍵點信息

        # 獲取食指指尖座標，和中指指尖座標
        x1, y1, _ = lmList[8]  # 食指尖的關鍵點索引號爲8
        x2, y2, _ = lmList[12]  # 中指指尖索引12

        # （5）檢查哪個手指是朝上的
        fingers = detector.fingersUp(hands[0])  # 傳入
        # print(fingers) 返回 [0,1,1,0,0] 代表 只有食指和中指豎起

        # 如果食指豎起且中指彎下，就認爲是移動鼠標
        if fingers[1] == 1 and fingers[2] == 0:
            # 開始移動時，在食指指尖畫一個圓圈，看得更清晰一些
            cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)  # 顏色填充整個圓

            # （6）確定鼠標移動的範圍
            # 將食指的移動範圍從預製的窗口範圍，映射到電腦屏幕範圍
            x3 = np.interp(x1, (pt1[0], pt2[0]), (0, wScr))
            y3 = np.interp(y1, (pt1[1], pt2[1]), (0, hScr))

            # （7）平滑，使手指在移動鼠標時，鼠標箭頭不會一直晃動
            cLocx = pLocx + (x3 - pLocx) / smooth  # 當前的鼠標所在位置座標
            cLocy = pLocy + (y3 - pLocy) / smooth

            # （8）移動鼠標
            autopy.mouse.move(cLocx, cLocy)  # 給出鼠標移動位置座標

            # 更新前一幀的鼠標所在位置座標，將當前幀鼠標所在位置，變成下一幀的鼠標前一幀所在位置
            pLocx, pLocy = cLocx, cLocy

        # （9）如果食指和中指都豎起，指尖距離小於某個值認爲是點擊鼠標
        if fingers[1] == 1 and fingers[2] == 1:  # 食指和中指都豎起

            # 計算食指尖和中指尖之間的距離distance,繪製好了的圖像img,指尖連線的信息info
            distance, info, img = detector.findDistance((x1, y1), (x2, y2), img)
            # print(distance)

            # 當指間距離小於50（像素距離）就認爲是點擊鼠標
            if distance < 50:
                # 在食指尖畫個綠色的圓，表示點擊鼠標
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)

                # 點擊鼠標
                autopy.mouse.click()

    # （10）顯示圖像
    # 查看FPS
    cTime = time.time()  # 處理完一幀圖像的時間
    fps = 1 / (cTime - pTime)
    pTime = cTime  # 重置起始時間

    # 在視頻上顯示fps信息，先轉換成整數再變成字符串形式，文本顯示座標，文本字體，文本大小
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 顯示圖像，輸入窗口名及圖像數據
    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == 27:  # 每幀滯留20毫秒後消失，ESC鍵退出
        break

# 釋放視頻資源
cap.release()
cv2.destroyAllWindows()