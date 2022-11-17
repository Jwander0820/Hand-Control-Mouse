import os
from PIL import Image

"""儲存圖像時需要有特殊格式，才能確認該張圖當時計算的時間，否則若是等速播放的話會顯示不出處理速度的不同"""
# cv2.imwrite(f"./img/f{str(frame_num).zfill(5)}_s{process_time:0<6}.png", frame)
# 為了抓到固定的文件名稱，小數點後需要補0，才能對齊文件

folder_path = f"../img"  # 要處理的資料夾路徑
files = os.listdir(folder_path)  # 讀取資料夾內所有資料
gif_list = []
for file_name in files:
    img_path = os.path.join(folder_path, file_name)
    frame_sec = float(file_name[8:14])  # 提取出秒數，轉換成浮點數
    frame_time = round(frame_sec / 0.04)  # 計算需要重複的幀數，以每秒25幀做計算，一幀會佔據0.04秒
    img = Image.open(img_path).convert("RGB")  # 開啟圖片
    for i in range(frame_time):  # 按照需要重複的幀數，添加N張圖到清單中
        gif_list.append(img)
gif_list[0].save("../test.gif", save_all=True, append_images=gif_list[1:], loop=0, duration=40, disposal=0)
