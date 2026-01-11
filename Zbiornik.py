import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath

class Zbiornik(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 400)
        self.top_trapez_h = 60
        self.rect_h = 200
        self.bot_trapez_h = 60

        self.width_top = 200
        self.width_mid = 140
        self.width_bot = 40

        self.total_tank_height = self.top_trapez_h + self.rect_h + self.bot_trapez_h

        self._poziom = 0.5
        
        self.draw_x = 50
        self.draw_y = 50

    def setPoziom(self, poziom):
        self._poziom = max(0.0, min(1.0, poziom))
        self.update()
    
    def setPolozenie(self, x, y):
        self.draw_x = x
        self.draw_y = self.update()

    def getPoziom(self):
        return self._poziom
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.draw_x + (self.width_top / 2)
        start_y = self.draw_y

        path = QPainterPath()

        p1_tl = QPointF(cx - self.width_top/2, start_y)
        p1_tr = QPointF(cx + self.width_top/2, start_y)
        p2_ml = QPointF(cx - self.width_mid/2, start_y + self.top_trapez_h)
        p2_mr = QPointF(cx + self.width_mid/2, start_y + self.top_trapez_h)
        p3_bl = QPointF(cx - self.width_mid/2, start_y + self.top_trapez_h + self.rect_h)
        p3_br = QPointF(cx + self.width_mid/2, start_y + self.top_trapez_h + self.rect_h)
        p4_bl = QPointF(cx - self.width_bot/2, start_y + self.total_tank_height)
        p4_br = QPointF(cx + self.width_bot/2, start_y + self.total_tank_height)


        path.moveTo(p1_tl)
        path.lineTo(p1_tr); path.lineTo(p2_mr); path.lineTo(p3_br)
        path.lineTo(p4_br); path.lineTo(p4_bl); path.lineTo(p3_bl)
        path.lineTo(p2_ml); path.lineTo(p1_tl)
        path.closeSubpath()

        painter.save()
        painter.setClipPath(path)

        liquid_height_px = self.total_tank_height * self._poziom
        rect_liquid = QRectF(cx - self.width_top/2, start_y + self.total_tank_height - liquid_height_px, self.width_top, liquid_height_px)

        painter.fillRect(rect_liquid, QColor(0,120,255,180))
        pen = QPen(Qt.gray, 4)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zbiornik PyQt")
        self.resize(500, 600)


        container = QHBoxLayout()
        layout = QVBoxLayout()
        layout2= QVBoxLayout()
        container.addLayout(layout)
        container.addLayout(layout2)
        self.setLayout(container)

        self.zbiornik1 = Zbiornik()
        self.zbiornik1.setStyleSheet("background-color: #222;")
        self.zbiornik2 = Zbiornik()
        self.zbiornik2.setStyleSheet("background-color: #222;")
        layout.addWidget(self.zbiornik1)
        layout2.addWidget(self.zbiornik2)

        self.slider_zbiornik1 = QSlider(Qt.Horizontal)
        self.slider_zbiornik1.setRange(0,100)
        self.slider_zbiornik1.setValue(50)
        self.slider_zbiornik1.valueChanged.connect(self.zmien_poziom)
        layout.addWidget(self.slider_zbiornik1)

        self.slider_zbiornik2 = QSlider(Qt.Horizontal)
        self.slider_zbiornik2.setRange(0,100)
        self.slider_zbiornik2.setValue(50)
        self.slider_zbiornik2.valueChanged.connect(self.zmien_poziom2)
        layout2.addWidget(self.slider_zbiornik2)



        self.label_slider_zbiornik1 = QLabel("Poziom: 50%")
        self.label_slider_zbiornik1.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_slider_zbiornik1)

        self.label_slider_zbiornik2 = QLabel("Poziom: 50%")
        self.label_slider_zbiornik2.setAlignment(Qt.AlignCenter)
        layout2.addWidget(self.label_slider_zbiornik2)

    def zmien_poziom(self, value):
        poziom_float = value / 100.0
        self.zbiornik1.setPoziom(poziom_float)
        self.label_slider_zbiornik1.setText(f"Poziom: {value}%")

    def zmien_poziom2(self, value):
        poziom_float = value / 100.0
        self.zbiornik2.setPoziom(poziom_float)
        self.label_slider_zbiornik2.setText(f"Poziom: {value}%")    
            



if __name__ == '__main__':
    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())





    



