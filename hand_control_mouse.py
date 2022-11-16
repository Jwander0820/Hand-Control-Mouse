import time
import cv2
import numpy as np
import autopy  # 滑鼠控制
import pyautogui  # 滑鼠控制
from cvzone.HandTrackingModule import HandDetector  # 手部檢測方法
from model.func_key import FuncKey


class HandControlMouse:
    def __init__(self):
        # 1. 導入基本資料
        self.wScr, self.hScr = autopy.screen.size()  # 返回電腦螢幕的寬和高(1280.0 720.0)
        wCam, hCam = 1280, 720  # 影像顯示窗口的寬和高
        self.pt1, self.pt2 = (500, 300), (900, 500)  # 虛擬鼠標的移動範圍，左上座標pt1，右下座標pt2

        self.cap = cv2.VideoCapture(0)  # 0代表自己電腦的鏡頭
        self.cap.set(3, wCam)  # 設置顯示框的寬度1280
        self.cap.set(4, hCam)  # 設置顯示框的高度720

        self.pTime = 0  # 設置第一幀開始處理的起始時間
        self.p_loc_x, self.p_loc_y = 0, 0  # 紀錄上一幀時的鼠標所在位置
        self.smooth = 4  # 自定義平滑係數，讓鼠標移動平緩一些
        # 2. 建立手部檢測方法
        self.detector = HandDetector(mode=False,  # 視頻流圖像
                                     maxHands=1,  # 最多檢測一隻手
                                     detectionCon=0.8,  # 最小檢測置信度
                                     minTrackCon=0.5)  # 最小跟蹤置信度
        # 3. 計時器，用於計算間隔時間，避免快速重複執行同一操作
        self.click_last_time = 0  # 紀錄上一次點擊的時間，用於計算點擊的間隔時間
        self.horiz_left_last_time = 0  # 計算水平左移的間隔時間
        self.horiz_right_last_time = 0  # 計算水平右移的間隔時間
        self.vert_up_last_time = 0  # 垂直上移的間隔時間
        self.vert_down_last_time = 0  # 垂直下移的間隔時間
        self.sleep_last_time = 0  # 休眠機制的間隔時間
        self.sleep_switch = True  # 是否開啟

    def move_mouse(self, x, y):
        """
        移動鼠標的操作
        :param x: 選取移動點的 X座標
        :param y: 選取移動點的 Y座標
        :return:
        """
        # 確定鼠標移動的範圍
        # 將掌心移動範圍從預設的窗口範圍，映射到電腦螢幕範圍；(x3, y3)是映射的真實座標
        x3 = np.interp(x, (self.pt1[0], self.pt2[0]), (0, self.wScr))
        y3 = np.interp(y, (self.pt1[1], self.pt2[1]), (0, self.hScr))
        # 平滑化，使手指在移動鼠標時，鼠標箭頭不會一直晃動；原理為新的座標-舊的座標，計算出移動量後除上平滑係數，降低移動的幅度
        c_loc_x = self.p_loc_x + (x3 - self.p_loc_x) / self.smooth  # 當前的鼠標所在位置座標
        c_loc_y = self.p_loc_y + (y3 - self.p_loc_y) / self.smooth
        # 移動鼠標
        autopy.mouse.move(c_loc_x, c_loc_y)  # 給出鼠標移動位置座標
        # 更新前一幀的鼠標所在位置座標，將當前幀鼠標所在位置，變成下一幀的鼠標前一幀所在位置
        self.p_loc_x, self.p_loc_y = c_loc_x, c_loc_y

    def click_left_button(self, intervals=1.0):
        """
        點擊左鍵的操作
        :param intervals: 點擊的最小間隔時間，避免短時間連續重複點擊
        :return:
        """
        # 點擊鼠標
        click_start_time = time.time()  # 紀錄開始點擊的時間
        if click_start_time - self.click_last_time > intervals:  # 若上一次點擊時間和這次點擊時間相差大於1秒，才會執行點擊操作
            autopy.mouse.click()  # 點擊操作
            # pyautogui.click(clicks=1, interval=0.2, button='left')
        self.click_last_time = time.time()  # 完成操作後，紀錄本次點擊的結束時間

    def double_click_left_button(self, intervals=1.0):
        """
        快速點擊左鍵兩下的操作
        :param intervals: 點擊的最小間隔時間，避免短時間連續重複點擊
        :return:
        """
        click_start_time = time.time()  # 紀錄開始點擊的時間
        if click_start_time - self.click_last_time > intervals:  # 若上一次點擊時間和這次點擊時間相差大於1秒，才會執行點擊操作
            pyautogui.click(clicks=2, button='left')
        self.click_last_time = time.time()  # 完成操作後，紀錄本次點擊的結束時間

    def scroll_page(self, img, x, y, horizontal_control=True, intervals=5.0):
        """
        滾動操作；上下滾動分兩種段位，緩慢滾動與快速滾動，左右的操作則可以自定義，預設為向左複製，向右貼上+Enter
        # 當沒有上下的操作時才會出發左右的操作
        :param img:準備處理的圖片
        :param x:移動點的 X座標
        :param y:移動點的 Y座標
        :param horizontal_control: 是否啟用水平控制操作
        :param intervals: 點擊的最小間隔時間，避免短時間連續重複點擊
        :return:
        """
        # (x3, y3)是映射的新座標，用於計算與當前鼠標座標的相對關係
        x3 = np.interp(x, (self.pt1[0], self.pt2[0]), (0, self.wScr))
        y3 = np.interp(y, (self.pt1[1], self.pt2[1]), (0, self.hScr))
        if 350 > self.p_loc_y - y3 > 150:  # 映射座標的y小於當前鼠標座標(x3, y3) 代表新座標在鼠標座標上面
            pyautogui.scroll(50)
            cv2.putText(img, "slow scroll up", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        elif self.p_loc_y - y3 > 350:  # 第二段滾動方式
            pyautogui.scroll(200)
            cv2.putText(img, "quick scroll up", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        elif -350 < self.p_loc_y - y3 < -150:
            pyautogui.scroll(-50)
            cv2.putText(img, "slow scroll down", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        elif self.p_loc_y - y3 < -350:
            pyautogui.scroll(-200)
            cv2.putText(img, "quick scroll down", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        # 故意設計成當上下的控制都沒觸發時才會輪到左右的控制，避免短時間執行多項操作，導致錯誤操作
        elif self.p_loc_x - x3 > 250:
            if horizontal_control:  # 是否開啟水平控制操作
                horiz_left_start_time = time.time()  # 紀錄開始點擊的時間
                if horiz_left_start_time - self.horiz_left_last_time > intervals:
                    FuncKey.ctrl_c()  # 執行快捷鍵
                    cv2.putText(img, "ctrl + c", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    self.horiz_left_last_time = time.time()  # 完成操作後，紀錄本次執行的結束時間
        elif self.p_loc_x - x3 < -250:
            if horizontal_control:
                horiz_right_start_time = time.time()  # 紀錄開始點擊的時間
                if horiz_right_start_time - self.horiz_right_last_time > intervals:
                    FuncKey.ctrl_v_enter()
                    cv2.putText(img, "ctrl + v", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    self.horiz_right_last_time = time.time()  # 完成操作後，紀錄本次執行的結束時間

    def custom_control_func(self, img, x, y, vertical_control=True, horizontal_control=True, intervals=5.0):
        """
        自定義控制函數，提供四向控制
        :param img:準備處理的圖片
        :param x:移動點的 X座標
        :param y:移動點的 Y座標
        :param vertical_control: 是否啟用垂直控制操作
        :param horizontal_control: 是否啟用水平控制操作
        :param intervals: 點擊的最小間隔時間，避免短時間連續重複點擊
        :return:
        """
        # (x3, y3)是映射的新座標，用於計算與當前鼠標座標的相對關係
        x3 = np.interp(x, (self.pt1[0], self.pt2[0]), (0, self.wScr))
        y3 = np.interp(y, (self.pt1[1], self.pt2[1]), (0, self.hScr))

        if self.p_loc_y - y3 > 250:  # 朝上
            if vertical_control:  # 是否開啟水平控制操作
                vert_up_start_time = time.time()  # 紀錄開始點擊的時間
                if vert_up_start_time - self.vert_up_last_time > intervals:
                    # FuncKey.alt_tab()  # <-可以改成自定義的函數
                    cv2.putText(img, "vert up", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    self.vert_up_last_time = time.time()  # 完成操作後，紀錄本次執行的結束時間
        elif self.p_loc_y - y3 < -250:  # 朝下
            if vertical_control:
                vert_down_start_time = time.time()  # 紀錄開始點擊的時間
                if vert_down_start_time - self.vert_down_last_time > intervals:
                    # FuncKey.ctrl_a()
                    cv2.putText(img, "vert down", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    self.vert_down_last_time = time.time()  # 完成操作後，紀錄本次執行的結束時間
        elif self.p_loc_x - x3 > 250:  # 朝左
            if horizontal_control:  # 是否開啟水平控制操作
                horiz_left_start_time = time.time()  # 紀錄開始點擊的時間
                if horiz_left_start_time - self.horiz_left_last_time > intervals:
                    # FuncKey.ctrl_win_left()
                    cv2.putText(img, "horiz left", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    self.horiz_left_last_time = time.time()  # 完成操作後，紀錄本次執行的結束時間
        elif self.p_loc_x - x3 < -250:  # 朝右
            if horizontal_control:
                horiz_right_start_time = time.time()  # 紀錄開始點擊的時間
                if horiz_right_start_time - self.horiz_right_last_time > intervals:
                    # FuncKey.ctrl_win_right()
                    cv2.putText(img, "horiz right", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                    self.horiz_right_last_time = time.time()  # 完成操作後，紀錄本次執行的結束時間

    def cal_fps(self):
        cTime = time.time()  # 處理完一幀圖像的時間
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime  # 重置起始時間
        return fps

    def process_video_frame(self, sleep_mode=True):
        # 處理每一幀圖像
        while True:
            # 圖片是否成功接收、img幀圖像
            success, img = self.cap.read()
            # 翻轉圖像，使自身和攝像頭中的自己呈鏡像關係 # 1代表水平翻轉，0代表豎直翻轉
            img = cv2.flip(img, flipCode=1)
            # 在圖像窗口上創建一個矩形框，在該區域內移動鼠標
            cv2.rectangle(img, self.pt1, self.pt2, (0, 255, 255), 5)
            # 手部關鍵點檢測，傳入每幀圖像, 返回手部關鍵點的座標信息(字典)，繪製關鍵點後的圖像
            hands, img = self.detector.findHands(img, flipType=False)  # 上面反轉過了，這裏就不用再翻轉了

            # 睡眠機制；有檢測到手部且睡眠模式開啟才會進行判斷
            if hands and sleep_mode:
                fingers = self.detector.fingersUp(hands[0])
                # 數字六手勢，決定睡眠模式的開關，最小間隔時間3秒
                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    sleep_start_time = time.time()
                    if sleep_start_time - self.sleep_last_time > 3:
                        self.sleep_last_time = time.time()  # 更新本次執行的結束時間
                        if not self.sleep_switch:  # 若觸發時睡眠開關為False則切換為True，反之亦然
                            self.sleep_switch = True
                        else:
                            self.sleep_switch = False
            # 當睡眠模式開啟時，左上方顯示sleep
            if not self.sleep_switch:
                cv2.putText(img, "sleep", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # 有檢測到手部且睡眠開關為True時才會執行手勢判斷
            if self.sleep_switch and hands:
                # 獲取hands中的21個關鍵點訊息
                lmList = hands[0]['lmList']  # hands是由N個字典組成的列表，字典包每隻手的關鍵點信息
                x1, y1, _ = lmList[9]  # 掌心處的關鍵點索引號爲9
                # 檢測哪個手指是朝上的
                fingers = self.detector.fingersUp(hands[0])  # 傳入 # print(fingers) 返回 [0,1,1,0,0] 代表只有食指和中指豎起
                cv2.putText(img, f"{fingers}", (50, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)  # 顯示當前手指的狀態
                cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)  # 開始移動時，在掌心畫一個圓圈，看得更清晰一些
                """手勢操作區域"""
                # 手掌攤開抓取掌心點作為虛擬滑鼠移動
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    self.move_mouse(x1, y1)
                    cv2.putText(img, "move", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                # 握拳執行點擊操作；(握拳狀態下，僅有大拇指會立起)
                if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    self.click_left_button()
                    cv2.putText(img, "click", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                # 槍型手勢上下滾動操作、水平向執行複製貼上操作(可修改)
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    self.scroll_page(img, x1, y1)
                # 數字四手勢，可自定義四向操作
                if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    self.custom_control_func(img, x1, y1)
                    cv2.putText(img, "customize your function", (50, 80), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            # 計算影像處理的幀數
            fps = self.cal_fps()
            # 在影片上顯示fps信息，先轉換成整數再變成字符串形式，文本顯示座標，文本字體，文本大小
            cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            # 顯示圖像，輸入窗口名及圖像數據
            cv2.imshow('HandControlMouse Press Esc to exit the program', img)
            if cv2.waitKey(1) & 0xFF == 27:  # 每幀滯留20毫秒後消失，ESC鍵退出
                break

        # 釋放資源
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    HandControlMouse().process_video_frame()
