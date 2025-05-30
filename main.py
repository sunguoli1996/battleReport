# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import time

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from PySide6.QtCore import Qt, QTimer, QEventLoop
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QMessageBox
from area_selector import ScreenAreaSelector
from config_manager import ConfigManager
from mouse_tracker import MouseTracker
from mouse_action import MouseActionExecutor

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        # 保存应用程序引用，用于正确恢复窗口
        self.app = QApplication.instance()

        # 初始化配置管理器
        self.config_manager = ConfigManager()
        
        # 初始化鼠标操作执行器
        self.mouse_executor = MouseActionExecutor()
        
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "PyDracula - Modern GUI"
        description = "PyDracula APP - Theme with colors based on Dracula for Python."
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_home_New.clicked.connect(self.buttonClick)
        
        # 绑定屏幕区域选择功能到按钮
        if hasattr(widgets, 'pushButton_2'):
            widgets.pushButton_2.clicked.connect(self.selectScreenArea)
            
            # 在启动后显示上次选择的区域坐标
            self.showLastSelectedArea()
            
        # 绑定鼠标轨迹跟踪功能到按钮
        if hasattr(widgets, 'pushButton_3'):
            widgets.pushButton_3.clicked.connect(self.trackMouseMovement)
            
            # 在启动后显示上次记录的鼠标轨迹
            self.showLastMouseTrack()
            
        # 绑定鼠标操作执行功能到按钮
        if hasattr(widgets, 'pushButton_4'):
            widgets.pushButton_4.clicked.connect(self.executeMouseAction)
            
            # 连接操作完成信号
            self.mouse_executor.actionCompleted.connect(self.onMouseActionCompleted)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()
        # 确保窗口置于最前
        self.activateWindow()
        self.raise_()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
        
    # 显示上次选择的区域坐标
    def showLastSelectedArea(self):
        if hasattr(widgets, 'lineEdit_2'):
            area = self.config_manager.get_selected_area()
            if area["width"] > 0 and area["height"] > 0:
                widgets.lineEdit_2.setText(
                    f"上次选择区域: x={area['x']}, y={area['y']}, "
                    f"width={area['width']}, height={area['height']}"
                )
            else:
                widgets.lineEdit_2.setText("尚未选择区域")
                
    # 显示上次记录的鼠标轨迹
    def showLastMouseTrack(self):
        if hasattr(widgets, 'lineEdit_2'):
            track = self.config_manager.get_mouse_track()
            if track["end_x"] > 0 or track["end_y"] > 0:  # 检查是否有有效数据
                message = (
                    f"上次鼠标轨迹: 从 ({track['start_x']}, {track['start_y']}) "
                    f"到 ({track['end_x']}, {track['end_y']})"
                )
                if widgets.lineEdit_2.text().startswith("上次选择区域"):
                    # 如果已经显示了区域信息，则添加到后面
                    widgets.lineEdit_2.setText(widgets.lineEdit_2.text() + " | " + message)
                else:
                    widgets.lineEdit_2.setText(message)
    
    # 执行保存的鼠标轨迹操作
    def executeMouseAction(self):
        print("执行保存的鼠标轨迹操作...")
        
        # 获取保存的鼠标轨迹
        track = self.config_manager.get_mouse_track()
        
        # 检查是否有有效的轨迹数据
        if track["start_x"] == 0 and track["start_y"] == 0 and track["end_x"] == 0 and track["end_y"] == 0:
            QMessageBox.warning(self, "警告", "没有可用的鼠标轨迹数据，请先使用轨迹记录功能")
            return
            
        # 显示确认对话框
        reply = QMessageBox.question(
            self, 
            "确认执行",
            f"即将执行鼠标从 ({track['start_x']}, {track['start_y']}) 到 ({track['end_x']}, {track['end_y']}) 的操作。\n\n"
            "注意：即将自动控制您的鼠标，请确保这是您想要的操作。\n"
            "程序将最小化，执行完成后会自动恢复。\n\n"
            "确定要执行吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 给用户3秒时间切换到目标窗口
            if hasattr(widgets, 'lineEdit_2'):
                widgets.lineEdit_2.setText("准备执行鼠标操作，3秒后开始...")
            
            # 执行倒计时
            QTimer.singleShot(1000, lambda: self.updateCountdown(2))
            QTimer.singleShot(2000, lambda: self.updateCountdown(1))
            QTimer.singleShot(3000, lambda: self.performMouseAction(track))
    
    def updateCountdown(self, seconds):
        if hasattr(widgets, 'lineEdit_2'):
            widgets.lineEdit_2.setText(f"准备执行鼠标操作，{seconds}秒后开始...")
    
    def performMouseAction(self, track):
        if hasattr(widgets, 'lineEdit_2'):
            widgets.lineEdit_2.setText("正在执行鼠标操作...")
        
        # 最小化窗口
        print("最小化窗口以执行鼠标操作...", flush=True)
        self.showMinimized()
        # 确保窗口状态更新
        QApplication.processEvents()
        
        # 执行鼠标轨迹操作
        self.mouse_executor.execute_mouse_track(
            track["start_x"], 
            track["start_y"],
            track["end_x"],
            track["end_y"],
            duration=0.5  # 可以调整拖动速度
        )
    
    def onMouseActionCompleted(self, success, message):
        print(f"鼠标操作结果: {'成功' if success else '失败'}, {message}")
        # 操作完成后恢复窗口
        QTimer.singleShot(500, self.forceRestoreWindow)
        
        if hasattr(widgets, 'lineEdit_2'):
            widgets.lineEdit_2.setText(message)
    
    # 屏幕区域选择方法
    def selectScreenArea(self):
        print("开始选择屏幕区域...", flush=True)
        # 隐藏窗口而不是最小化，避免闪烁
        self.setVisible(False)
        # 让窗口立即隐藏，确保处理完成
        QApplication.processEvents()
        time.sleep(0.1)  # 短暂延迟确保窗口已隐藏
        # 立即显示区域选择器
        self.showAreaSelector()
        
    def showAreaSelector(self):
        print("显示区域选择器...", flush=True)
        try:
            self.selector = ScreenAreaSelector()
            # 连接信号
            self.selector.areaSelected.connect(self.onAreaSelected)
            # 连接关闭信号
            self.selector.selectorClosed.connect(self.forceRestoreWindow)
            
            # 设置属性以防止选择器关闭导致整个应用程序关闭
            self.selector.setAttribute(Qt.WA_QuitOnClose, False)
            
            # 显示选择器
            self.selector.show()
            
            # 确保在选择器销毁时恢复主窗口
            self.selector.destroyed.connect(self.forceRestoreWindow)
        except Exception as e:
            print(f"显示区域选择器时出错: {str(e)}", flush=True)
            # 出错时也要确保主窗口恢复
            self.forceRestoreWindow()
    
    def onAreaSelected(self, x, y, width, height):
        print(f"主窗口接收到选择区域: x={x}, y={y}, width={width}, height={height}")
        # 保存选择的区域坐标到配置文件
        self.config_manager.save_selected_area(x, y, width, height)
        # 更新界面显示
        if hasattr(widgets, 'lineEdit_2'):
            widgets.lineEdit_2.setText(f"选择区域: x={x}, y={y}, width={width}, height={height}")
    
    # 鼠标轨迹跟踪方法
    def trackMouseMovement(self):
        print("开始跟踪鼠标轨迹...")
        # 隐藏窗口
        self.setVisible(False)
        # 让窗口立即隐藏，确保处理完成
        QApplication.processEvents()
        time.sleep(0.1)  # 短暂延迟确保窗口已隐藏
        # 立即显示跟踪器
        self.showMouseTracker()
        
    def showMouseTracker(self):
        print("显示鼠标跟踪器...", flush=True)
        try:
            self.tracker = MouseTracker()
            # 连接信号
            self.tracker.trackCompleted.connect(self.onTrackCompleted)
            # 连接关闭信号
            self.tracker.trackerClosed.connect(self.forceRestoreWindow)
            
            # 设置属性以防止跟踪器关闭导致整个应用程序关闭
            self.tracker.setAttribute(Qt.WA_QuitOnClose, False)
            
            # 显示跟踪器
            self.tracker.show()
            
            # 确保在跟踪器销毁时恢复主窗口
            self.tracker.destroyed.connect(self.forceRestoreWindow)
        except Exception as e:
            print(f"显示鼠标跟踪器时出错: {str(e)}", flush=True)
            # 出错时也要确保主窗口恢复
            self.forceRestoreWindow()
    
    def forceRestoreWindow(self):
        print("强制恢复主窗口...", flush=True)
        # 确保程序没有被销毁
        if not QApplication.instance():
            print("错误：应用程序实例不存在！", flush=True)
            return
            
        # 确保窗口可见且活跃
        QTimer.singleShot(100, self._delayedRestore)
    
    def _delayedRestore(self):
        print("执行延迟恢复...", flush=True)
        
        # 将窗口标记为有效
        if not self.isVisible():
            print("窗口不可见，正在恢复...", flush=True)
        
        # 如果窗口处于最小化状态，需要先恢复
        if self.isMinimized():
            print("恢复最小化窗口...", flush=True)
            self.showNormal()
            QApplication.processEvents()
            
        # 确保窗口的正确状态
        self.setVisible(True)
        
        # 取消最小化并激活窗口
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.raise_()
        self.activateWindow()
        
        # 更新界面
        QApplication.processEvents()
        
        # 再次提升窗口以确保在前台
        QTimer.singleShot(100, lambda: self._finalRestore())
        
    def _finalRestore(self):
        print("执行最终恢复...", flush=True)
        # 确保窗口位于最前方
        self.raise_()
        self.activateWindow()
        self.show()  # 确保窗口显示
        print("主窗口已恢复", flush=True)
        
    def onTrackCompleted(self, start_x, start_y, end_x, end_y):
        print(f"主窗口接收到鼠标轨迹: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
        # 保存轨迹坐标到配置文件
        self.config_manager.save_mouse_track(start_x, start_y, end_x, end_y)
        # 更新界面显示
        if hasattr(widgets, 'lineEdit_2'):
            message = f"鼠标轨迹: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})"
            if widgets.lineEdit_2.text().startswith("选择区域"):
                # 如果已经显示了区域信息，则添加到后面
                widgets.lineEdit_2.setText(widgets.lineEdit_2.text() + " | " + message)
            else:
                widgets.lineEdit_2.setText(message)
                
    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW HOME_NEW PAGE
        if btnName == "btn_home_New":
            widgets.stackedWidget.setCurrentWidget(widgets.home_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    try:
        # 设置应用程序属性
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("icon.ico"))
        
        # 创建主窗口并显示
        window = MainWindow()
        
        # 防止应用程序意外关闭的安全机制
        def handle_exception(exc_type, exc_value, exc_tb):
            print(f"捕获到未处理的异常: {exc_type.__name__}: {exc_value}")
            # 记录到日志或显示给用户
            return False  # 让系统默认的异常处理程序继续处理
        
        # 设置异常钩子
        sys.excepthook = handle_exception
        
        # 防止子窗口关闭导致应用程序退出
        def custom_quit_handler():
            print("拦截到退出请求！")
            # 不执行退出操作，而是确保主窗口可见
            if hasattr(window, '_delayedRestore'):
                window._delayedRestore()
            return
            
        # 替换应用程序的退出函数
        original_quit = app.quit
        app.quit = custom_quit_handler
        
        # 运行应用程序事件循环
        exit_code = app.exec_()
        print(f"应用程序正常退出，退出码: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        print(f"应用程序启动时发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
