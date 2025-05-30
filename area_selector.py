from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QObject, QTimer
from PySide6.QtGui import QScreen, QPixmap, QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QRubberBand

# 创建信号类
class AreaSelectorSignals(QObject):
    areaSelected = Signal(int, int, int, int)  # x, y, width, height
    selectorClosed = Signal()  # 新增：选择器关闭信号

# 屏幕区域选择器类
class ScreenAreaSelector(QWidget):
    def __init__(self):
        super().__init__()
        # 创建信号对象
        self.signals = AreaSelectorSignals()
        self.areaSelected = self.signals.areaSelected
        self.selectorClosed = self.signals.selectorClosed
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        
        # 背景变透明，而不是半透明黑色
        self.setStyleSheet("background-color: transparent;")
        
        # 创建橡皮筋选择框
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.rubberBand.setStyleSheet("QRubberBand { background-color: rgba(0, 174, 255, 50); border: 2px solid rgb(0, 174, 255); }")
        self.origin = QPoint()
        self.selection = QRect()
        
        # 获取屏幕截图
        screen = QApplication.primaryScreen()
        self.screenshot = screen.grabWindow(0)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 先绘制原始截图
        painter.drawPixmap(0, 0, self.screenshot)
        
        # 创建半透明黑色遮罩，覆盖整个屏幕
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))
        
        # 如果有选择区域，将该区域还原为原始图像
        if not self.selection.isNull():
            # 从原始截图中复制出选中区域
            selected_area = self.screenshot.copy(self.selection)
            
            # 在选中区域绘制原始图像
            painter.drawPixmap(self.selection, selected_area)
            
            # 绘制选中区域周围的边框
            pen = QPen(QColor(0, 174, 255), 2)
            painter.setPen(pen)
            painter.drawRect(self.selection)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
        elif event.button() == Qt.RightButton:
            # 右键点击取消
            print("右键取消选择，发送关闭信号")
            # 先发送信号，再安全关闭
            self.signals.selectorClosed.emit()
            # 使用延迟关闭，确保信号被处理
            QTimer.singleShot(100, self.safeClose)
            # 不直接调用 self.close() 避免意外关闭整个程序
    
    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.selection = QRect(self.origin, event.pos()).normalized()
            self.rubberBand.setGeometry(self.selection)
            self.update()  # 更新绘制
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.selection.isNull():
            # 隐藏橡皮筋，以便看到最终效果
            self.rubberBand.hide()
            
            # 完成选择后打印坐标并关闭
            x, y, width, height = self.selection.x(), self.selection.y(), self.selection.width(), self.selection.height()
            print(f"选择区域坐标: x={x}, y={y}, width={width}, height={height}")
            
            # 发出信号
            self.signals.areaSelected.emit(x, y, width, height)
            print("发送区域选择信号，准备关闭选择器")
            
            # 发送关闭信号
            self.signals.selectorClosed.emit()
            
            # 确保选择器被正确关闭但不会导致整个程序退出
            QTimer.singleShot(100, self.safeClose)
    
    def safeClose(self):
        print("安全关闭区域选择器...")
        try:
            # 在关闭前再次发送信号
            self.signals.selectorClosed.emit()
            # 仅销毁此窗口而不是退出程序
            self.deleteLater()
        except Exception as e:
            print(f"关闭区域选择器时出错: {str(e)}")
            
    def closeEvent(self, event):
        print("区域选择器正在关闭...")
        try:
            # 再次发送关闭信号，以防万一
            self.signals.selectorClosed.emit()
            # 接受关闭事件但不传播到整个应用程序
            event.accept()
            super().closeEvent(event)
        except Exception as e:
            print(f"处理关闭事件时出错: {str(e)}")
            # 确保事件被接受
            event.accept()

# 使用示例:
# selector = ScreenAreaSelector()
# selector.areaSelected.connect(lambda x, y, w, h: print(f"Selected: {x}, {y}, {w}, {h}"))
# selector.show() 