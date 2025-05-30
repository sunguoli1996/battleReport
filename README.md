# PyDracula - Modern GUI PySide6 / PyQt6
# 

> ## :gift: **//// DONATE ////**
> ## 🔗 Donate (Gumroad): https://gum.co/mHsRC
> This interface is free for any use, but if you are going to use it commercially, consider helping to maintain this project and others with a donation by Gumroado at the link above. This helps to keep this and other projects active.

> **Warning**: this project was created using PySide6 and Python 3.9, using previous versions can cause compatibility problems.

# YouTube - Presentation And Tutorial
Presentation and tutorial video with the main functions of the user interface.
> 🔗 https://youtu.be/9DnaHg4M_AM

# Multiple Themes
![PyDracula_Default_Dark](https://user-images.githubusercontent.com/60605512/112993874-0b647700-9140-11eb-8670-61322d70dbe3.png)
![PyDracula_Light](https://user-images.githubusercontent.com/60605512/112993918-18816600-9140-11eb-837c-e7a7c3d2b05e.png)

# High DPI
> Qt Widgets is an old technology and does not have a good support for high DPI settings, making these images look distorted when your system has DPI applied above 100%.
You can minimize this problem using a workaround by applying this code below in "main.py" just below the import of the Qt modules.
```python
# ADJUST QT FONT DPI FOR HIGHT SCALE
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96"
```

# Running
> Inside your preferred terminal run the commands below depending on your system, remembering before installing Python 3.9> and PySide6 "pip install PySide6".
> ## **Windows**:
```console
python main.py
```
> ## **MacOS and Linux**:
```console
python3 main.py
```
# Compiling
> ## **Windows**:
```console
python setup.py build
```

# Project Files And Folders
> **main.py**: application initialization file.

> **main.ui**: Qt Designer project.

> **resouces.qrc**: Qt Designer resoucers, add here your resources using Qt Designer. Use version 6 >

> **setup.py**: cx-Freeze setup to compile your application (configured for Windows).

> **themes/**: add here your themes (.qss).

> **modules/**: module for running PyDracula GUI.

> **modules/app_funtions.py**: add your application's functions here.
Up
> **modules/app_settings.py**: global variables to configure user interface.

> **modules/resources_rc.py**: "resource.qrc" file compiled for python using the command: ```pyside6-rcc resources.qrc -o resources_rc.py```.

> **modules/ui_functions.py**: add here only functions related to the user interface / GUI.

> **modules/ui_main.py**: file related to the user interface exported by Qt Designer. You can compile it manually using the command: ```pyside6-uic main.ui> ui_main.py ```.
After expoting in .py and change the line "import resources_rc" to "from. Resoucers_rc import *" to use as a module.

> **images/**: put all your images and icons here before converting to Python (resources_re.py) ```pyside6-rcc resources.qrc -o resources_rc.py```.

# Projects Created Using PyDracula
**See the projects that were created using PyDracula.**
> To participate create a "Issue" with the name beginning with "#pydracula_project", leaving the link of your project on Github, name of the creator and what is its functionality. Your project will be added and this list will be deleted from "Issue".
**Malicious programs will not be added**!

# 屏幕选择和鼠标自动化工具

这是一个基于PySide6的GUI应用程序，允许用户选择屏幕区域并记录鼠标操作轨迹，然后自动执行这些操作。

## 功能特性

1. **屏幕区域选择**：用户可以选择屏幕上的特定区域，并保存其坐标。
2. **鼠标轨迹记录**：记录从按下到释放的鼠标移动轨迹。
3. **自动化执行**：根据保存的轨迹自动执行鼠标操作。
4. **配置持久化**：在会话之间保存用户设置和操作。

## 安装说明

确保已安装以下依赖:
```
pip install PySide6 pyautogui
```

## 使用方法

1. 运行主程序：
```
python main.py
```

2. 界面功能：
   - 屏幕区域选择按钮：启动屏幕区域选择器
   - 鼠标轨迹记录按钮：启动鼠标轨迹记录
   - 鼠标操作执行按钮：执行已保存的鼠标轨迹

## 主要模块

- `main.py`: 主程序入口和UI控制
- `area_selector.py`: 屏幕区域选择功能
- `mouse_tracker.py`: 鼠标轨迹记录功能
- `mouse_action.py`: 鼠标操作执行功能
- `config_manager.py`: 配置管理和持久化

## 已知问题与解决方案

### 主窗口在弹出选择器后不再显示的问题

#### 问题描述：
当用户使用屏幕选择器或鼠标轨迹记录功能后，主窗口可能不会重新显示。

#### 解决方案：
1. 确保子窗口关闭时发送明确的信号：
```python
# 在 area_selector.py 和 mouse_tracker.py 中添加关闭信号
selectorClosed = Signal()  # 选择器关闭信号
trackerClosed = Signal()   # 跟踪器关闭信号

# 在相关事件处理中发送信号
self.signals.selectorClosed.emit()
```

2. 主窗口采用延迟恢复策略：
```python
def forceRestoreWindow(self):
    # 延迟恢复以确保子窗口已完全关闭
    QTimer.singleShot(100, self._delayedRestore)

def _delayedRestore(self):
    self.setVisible(True)
    self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    self.raise_()
    self.activateWindow()
    # 再次提升窗口以确保在前台
    QTimer.singleShot(50, self.raise_)
    QTimer.singleShot(100, self.activateWindow)
```

3. 使用 setVisible 而不是 hide/show：
```python
# 替代 self.hide()
self.setVisible(False)
QApplication.processEvents()
time.sleep(0.1)  # 短暂延迟确保窗口已隐藏

# 替代 self.show()
self.setVisible(True)
```

## 贡献指南

欢迎贡献代码或报告问题。请遵循以下步骤：
1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建合并请求

## 许可证

本项目基于 MIT 许可证发布 - 详情参见 LICENSE 文件。



