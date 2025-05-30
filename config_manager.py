import os
import json

class ConfigManager:
    """
    配置管理类，用于保存和加载应用程序配置，如选定区域的坐标
    """
    
    def __init__(self, config_file="app_config.json"):
        """
        初始化配置管理器
        
        参数:
            config_file: 配置文件名，默认为 app_config.json
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """
        从文件加载配置，如果文件不存在则创建默认配置
        
        返回:
            配置字典
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return self._default_config()
        else:
            return self._default_config()
    
    def _default_config(self):
        """
        返回默认配置
        
        返回:
            默认配置字典
        """
        return {
            "selected_area": {
                "x": 0,
                "y": 0,
                "width": 0,
                "height": 0
            },
            "mouse_track": {
                "start_x": 0,
                "start_y": 0,
                "end_x": 0,
                "end_y": 0
            }
        }
    
    def save_config(self):
        """
        保存配置到文件
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            print(f"配置已保存到 {self.config_file}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_selected_area(self):
        """
        获取已保存的选定区域坐标
        
        返回:
            包含 x, y, width, height 的字典
        """
        return self.config.get("selected_area", self._default_config()["selected_area"])
    
    def save_selected_area(self, x, y, width, height):
        """
        保存选定区域的坐标
        
        参数:
            x: 区域左上角 x 坐标
            y: 区域左上角 y 坐标
            width: 区域宽度
            height: 区域高度
        """
        self.config["selected_area"] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        self.save_config()
        
    def get_mouse_track(self):
        """
        获取已保存的鼠标轨迹坐标
        
        返回:
            包含 start_x, start_y, end_x, end_y 的字典
        """
        return self.config.get("mouse_track", self._default_config()["mouse_track"])
    
    def save_mouse_track(self, start_x, start_y, end_x, end_y):
        """
        保存鼠标轨迹的起始和结束坐标
        
        参数:
            start_x: 起始点 x 坐标
            start_y: 起始点 y 坐标
            end_x: 结束点 x 坐标
            end_y: 结束点 y 坐标
        """
        self.config["mouse_track"] = {
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y
        }
        self.save_config() 