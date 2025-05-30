from PySide6.QtCore import Qt, Signal, QObject, QPoint, QTimer
from PySide6.QtGui import QScreen, QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import QApplication, QWidget

class MouseTrackerSignals(QObject):
    """信号类，用于发送鼠标轨迹数据"""
    trackCompleted = Signal(int, int, int, int)  # start_x, start_y, end_x, end_y
    trackerClosed = Signal()  # 新增：跟踪器关闭信号

class MouseTracker(QWidget):
    """鼠标轨迹跟踪器，捕获鼠标按下和释放的坐标"""
    
    def __init__(self):
        super().__init__()
        # 创建信号对象
        self.signals = MouseTrackerSignals()
        self.trackCompleted = self.signals.trackCompleted
        self.trackerClosed = self.signals.trackerClosed
        
        # 设置全屏无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        
        # 设置透明背景
        self.setStyleSheet("background-color: rgba(0, 0, 0, 50);")
        
        # 初始化轨迹坐标
        self.start_point = None
        self.current_point = None
        self.end_point = None
        
        # 获取屏幕截图作为背景
        screen = QApplication.primaryScreen()
        self.screenshot = screen.grabWindow(0)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 绘制背景截图
        painter.drawPixmap(0, 0, self.screenshot)
        
        # 绘制半透明黑色遮罩
        painter.fillRect(self.rect(), QColor(0, 0, 0, 50))
        
        # 如果有起点和当前点，绘制轨迹线
        if self.start_point and self.current_point:
            # 设置绘制轨迹的笔
            pen = QPen(QColor(255, 0, 0), 3)  # 红色，宽度为3
            painter.setPen(pen)
            painter.drawLine(self.start_point, self.current_point)
            
            # 绘制起点和当前点的圆圈标记
            painter.setBrush(QColor(0, 255, 0))  # 绿色填充
            painter.drawEllipse(self.start_point, 5, 5)  # 起点
            painter.setBrush(QColor(255, 0, 0))  # 红色填充
            painter.drawEllipse(self.current_point, 5, 5)  # 当前点/终点
            
            # 显示坐标信息
            painter.setPen(QColor(255, 255, 255))
            start_text = f"起点: ({self.start_point.x()}, {self.start_point.y()})"
            current_text = f"当前点: ({self.current_point.x()}, {self.current_point.y()})"
            
            # 在屏幕顶部显示坐标信息
            painter.drawText(10, 30, start_text)
            painter.drawText(10, 50, current_text)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 记录起点
            self.start_point = event.pos()
            self.current_point = event.pos()
            self.update()
        elif event.button() == Qt.RightButton:
            # 右键取消
            print("右键取消跟踪，发送关闭信号")
            self.signals.trackerClosed.emit()
            QTimer.singleShot(100, self.safeClose)
            
    def mouseMoveEvent(self, event):
        if self.start_point:
            # 更新当前点
            self.current_point = event.pos()
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_point:
            # 记录终点
            self.end_point = event.pos()
            
            # 发送信号
            start_x, start_y = self.start_point.x(), self.start_point.y()
            end_x, end_y = self.end_point.x(), self.end_point.y()
            
            print(f"鼠标轨迹: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})")
            self.signals.trackCompleted.emit(start_x, start_y, end_x, end_y)
            
            # 发送关闭信号
            print("发送轨迹完成信号，准备关闭跟踪器")
            self.signals.trackerClosed.emit()
            
            # 安全关闭跟踪器
            QTimer.singleShot(100, self.safeClose)
            
    def safeClose(self):
        print("安全关闭鼠标跟踪器...")
        try:
            # 在关闭前再次发送信号
            self.signals.trackerClosed.emit()
            # 仅销毁此窗口而不是退出程序
            self.deleteLater()
        except Exception as e:
            print(f"关闭鼠标跟踪器时出错: {str(e)}")
            
    def closeEvent(self, event):
        print("鼠标跟踪器正在关闭...")
        try:
            # 再次发送关闭信号，以防万一
            self.signals.trackerClosed.emit()
            # 接受关闭事件但不传播到整个应用程序
            event.accept()
            super().closeEvent(event)
        except Exception as e:
            print(f"处理关闭事件时出错: {str(e)}")
            # 确保事件被接受
            event.accept()
            
    def keyPressEvent(self, event):
        # 按ESC键取消
        if event.key() == Qt.Key_Escape:
            print("按ESC取消跟踪，发送关闭信号")
            self.signals.trackerClosed.emit()
            QTimer.singleShot(100, self.safeClose) 