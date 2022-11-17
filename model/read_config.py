import os
import configparser


class ReadConfig:
    @staticmethod
    def get_config(config_path, section):
        """
        取得設定檔相關資料
        :param config_path:設定檔路徑
        :param section: 提取的區塊
        :return:
        """
        # 開發使用，使用絕對路徑指向設定檔，避免相對路徑下，revital外的資料夾在呼叫內部程式時，因為工作路徑不同無法引用設定檔。
        # config_path = r"E:\JasperWork\Revital\revital\revital_config.ini"
        config = configparser.ConfigParser()
        config.read(config_path, encoding='UTF-8')
        config_section = config[section]  # 儲存section下的config設定
        return config_section

    @staticmethod
    def get_data(key, value):
        config_path = r"../config.ini"
        if os.path.exists(config_path) is True:
            config = configparser.ConfigParser()
            config.read(config_path, encoding='UTF-8')
            return config.get(key, value)

        else:
            print("file is not exist")

    @staticmethod
    def ini2json(ini_path):
        d = {}
        config = configparser.ConfigParser()
        config.read(ini_path, encoding='UTF-8')
        for s in config.sections():
            # print(s)
            # print(cfg.items(s))  # 指定section,返回二元组
            d[s] = dict(config.items(s))
        return d


if __name__ == '__main__':
    sleep_mode = ReadConfig().get_data("basic", "sleep_mode")
    print(sleep_mode)

    _config_path = "../config.ini"
    main_config = ReadConfig.get_config(_config_path, "basic")
    print(main_config)  # 原始狀態下 會顯示 <Section: main>；type為<class 'configparser.SectionProxy'>
    bool_test = main_config.getboolean("sleep_mode")  # 正確從設定檔中轉bool的方法
    print(bool_test)
    print(type(bool_test))
