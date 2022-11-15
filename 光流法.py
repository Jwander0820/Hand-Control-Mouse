# -*- coding:utf-8 -*-
__author__ = 'Microcosm'

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# 設定 ShiTomasi 角點檢測的引數
feature_params = dict( maxCorners=100,
                       qualityLevel=0.3,
                       minDistance=7,
                       blockSize=7 )

# 設定 lucas kanade 光流場的引數
# maxLevel 為使用影象金字塔的層數
lk_params = dict( winSize=(15,15),
                  maxLevel=2,
                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# 產生隨機的顏色值
color = np.random.randint(0,255,(100,3))

# 獲取第一幀，並尋找其中的角點
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# 建立一個掩膜為了後面繪製角點的光流軌跡
mask = np.zeros_like(old_frame)

while(1):
    ret, frame = cap.read()
    if ret:
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 計算能夠獲取到的角點的新位置
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # 選取好的角點，並篩選出舊的角點對應的新的角點
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # 繪製角點的軌跡
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()  # 需要轉換為int形式
            c,d = old.ravel()
            a = int(a)
            b = int(b)
            c = int(c)
            d = int(d)
            cv2.line(mask, (a,b), (c,d), color[i].tolist(), 2)
            cv2.circle(frame, (a,b), 5, color[i].tolist(), -1)

        img = cv2.add(frame, mask)

        cv2.imshow("frame", img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # 更新當前幀和當前角點的位置
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)

    else:
        break

cv2.destroyAllWindows()
cap.release()
