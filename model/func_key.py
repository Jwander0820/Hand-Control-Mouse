import pyautogui  # 滑鼠控制


class FuncKey:
    @staticmethod
    def ctrl_c():
        """
        ctrl + c；複製
        :return:
        """
        pyautogui.keyDown('ctrl')
        pyautogui.press('c')
        pyautogui.keyUp('ctrl')

    @staticmethod
    def ctrl_v_enter():
        """
        ctrl+ v + enter；貼上 + Enter
        :return:
        """
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')
        pyautogui.press('enter')

    @staticmethod
    def ctrl_a():
        """
        ctrl + a；全選
        :return:
        """
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

    @staticmethod
    def alt_tab():
        """
        alt + tab；切換視窗
        :return:
        """
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.keyUp('alt')

    @staticmethod
    def ctrl_win_left():
        """
        ctrl + win + left；向左切換桌面
        :return:
        """
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('win')
        pyautogui.press('left')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('win')

    @staticmethod
    def ctrl_win_right():
        """
        ctrl + win + right；向右切換桌面
        :return:
        """
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('win')
        pyautogui.press('right')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('win')

    @staticmethod
    def right_click():
        """
        shift + f10；鍵盤模擬滑鼠點擊右鍵的選單功能
        :return:
        """
        pyautogui.keyDown('shift')
        pyautogui.press('f10')
        pyautogui.keyUp('shift')

    @staticmethod
    def enter():
        """
        enter；輸入使用
        :return:
        """
        pyautogui.press('enter')
