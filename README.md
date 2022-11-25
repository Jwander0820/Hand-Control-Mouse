## 簡介

透過鏡頭辨識手勢，實現手勢操控滑鼠執行輕度操作

## 環境相關

**建議 Python 3.8 版本 (以下)**

建立環境可以參考requirements.txt

主要套件: numpy、opencv-python、cvzone、mediapipe、
pyautogui 、autopy

Python版本限制 3.8 以下主要是因autopy只支援到Python 3.8 的版本


## 執行

直接執行 hand_control_mouse.py 即可

## 基礎手勢說明
1. 數字手勢 - 五
- 執行滑鼠的移動，透過關鍵點的移動映射到顯示器對應位置上
<div><img width="156" height="200"  src=pyinstaller_spec/body_hand_tenohira_five.png></div>

2. 數字手勢 - 零
- 執行左鍵點擊，設定觸發時間間距1秒，避免連續點擊
<div><img width="156" height="156"  src=pyinstaller_spec/body_hand_tenohira_zero.png></div>

3. 數字手勢 - 七
- 四向操作，向左複製、向右貼上、上下控制滑鼠滾輪的滾動
- 左右的操作觸發時間間距5秒
- 上下的滾輪操作有兩段操作，根據位移距離決定觸發的操作，第一段滾動較慢，第二段滾動較快
<div><img width="156" height="200"  src=pyinstaller_spec/body_hand_tenohira_seven.png></div>

4. 數字手勢 - 六
- 控制休眠機制，休眠時不會觸發其他操作，觸發時間間距3秒
<div><img width="156" height="156"  src=pyinstaller_spec/body_hand_tenohira_six.png></div>

5. 數字手勢 - 四
- 四向操作，可自行定義要執行的動作，亦可以從func_key.py中選擇調用常用的功能鍵，觸發時間間距5秒
<div><img width="156" height="200"  src=pyinstaller_spec/body_hand_tenohira_four.png></div>


## 設定檔說明(預設值)
1. sleep_mode = True
   - 設定睡眠機制的開關，由手勢六觸發
2. anti_shake_factor = 20
   - 防抖動係數，當滑鼠移動的位移量大於該值(pixel)時才會觸發移動
   - 主要用於解決手懸空固定時，些微的晃動造成滑鼠跟著抖動的問題
3. frame_resize_factor = 0.25
   - 觀察用的實時處理視窗大小，預設分辨率為1280x720
4. save_video_frame = False
   - 儲存實時處理完的圖像結果，建議不要開啟，開啟後會讓處理速度大幅降低(約50%)
5. gesture_seven = True
   - 設定手勢七的開關
6. gesture_four = True
   - 設定手勢四的開關
7. gesture_four_exe_threshold = 500
   - 設定手勢四，四向位移觸發功能的最短距離

---
### 待優化問題
1. 欲觸發指定操作時，應該先維持手勢一段時間後才會觸發該功能，避免手一揮過鏡頭意外觸發操作，
主要是有碰到手在隨意揮動的情況下，可能會意外觸發某些操作，可能只是一閃而過的畫面，但不是我們想要執行的操作
；解決方向，觸發功能前添加計時器，當維持手勢一段時間後才會觸發功能，代表使用者確定要執行該功能
