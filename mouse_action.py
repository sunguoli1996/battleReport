import time
import threading
from PySide6.QtCore import QObject, Signal
import pyautogui

# 确保鼠标操作安全，防止意外移动到屏幕边缘
pyautogui.FAILSAFE = True

class MouseActionSignals(QObject):
    """信号类，用于发送鼠标操作结果"""
    actionCompleted = Signal(bool, str)  # 成功/失败，消息

class MouseActionExecutor:
    """
    鼠标操作执行器，用于根据保存的坐标执行鼠标操作
    """
    
    def __init__(self):
        """初始化鼠标操作执行器"""
        self.signals = MouseActionSignals()
        self.actionCompleted = self.signals.actionCompleted
        self.is_running = False
    
    def execute_mouse_track(self, start_x, start_y, end_x, end_y, duration=0.5):
        """
        执行鼠标轨迹操作
        
        参数:
            start_x: 起始点 x 坐标
            start_y: 起始点 y 坐标
            end_x: 结束点 x 坐标
            end_y: 结束点 y 坐标
            duration: 鼠标移动持续时间（秒）
        """
        if self.is_running:
            self.signals.actionCompleted.emit(False, "操作正在执行中，请等待完成")
            return
            
        # 使用线程执行鼠标操作，避免阻塞UI
        thread = threading.Thread(
            target=self._execute_mouse_track_thread,
            args=(start_x, start_y, end_x, end_y, duration)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_mouse_track_thread(self, start_x, start_y, end_x, end_y, duration):
        """
        在线程中执行鼠标轨迹操作
        
        参数:
            start_x: 起始点 x 坐标
            start_y: 起始点 y 坐标
            end_x: 结束点 x 坐标
            end_y: 结束点 y 坐标
            duration: 鼠标移动持续时间（秒）
        """
        try:
            self.is_running = True
            
            # 获取当前鼠标位置（可选，用于操作后恢复）
            # original_position = pyautogui.position()
            
            # 执行前暂停一下，给主窗口最小化时间
            time.sleep(0.5)
            
            # 移动鼠标到起始位置
            print(f"移动鼠标到起始位置: ({start_x}, {start_y})")
            pyautogui.moveTo(start_x, start_y, duration=0.2)
            
            # 鼠标左键按下
            print("鼠标左键按下")
            pyautogui.mouseDown()
            
            # 移动到结束位置
            print(f"拖动到结束位置: ({end_x}, {end_y})")
            pyautogui.moveTo(end_x, end_y, duration=duration)
            
            # 鼠标左键释放
            print("鼠标左键释放")
            pyautogui.mouseUp()
            
            # 操作完成后短暂延迟，确保操作完成
            time.sleep(0.5)
            
            # 操作完成
            print("鼠标轨迹操作完成")
            self.signals.actionCompleted.emit(True, "鼠标轨迹操作完成")
            
            # 移动回原位置（可选）
            # pyautogui.moveTo(original_position.x, original_position.y, duration=0.2)
            
        except Exception as e:
            error_message = f"执行鼠标操作时出错: {str(e)}"
            print(error_message)
            self.signals.actionCompleted.emit(False, error_message)
        finally:
            self.is_running = False


# 单次点击操作
def click_at_position(x, y, button='left'):
    """
    在指定位置执行单次点击
    
    参数:
        x: 点击位置的 x 坐标
        y: 点击位置的 y 坐标
        button: 使用的鼠标按钮，默认为'left'（左键）
    """
    try:
        # 移动鼠标到指定位置
        pyautogui.moveTo(x, y, duration=0.2)
        # 执行点击
        pyautogui.click(button=button)
        return True, "点击操作完成"
    except Exception as e:
        return False, f"点击操作失败: {str(e)}" 