from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
import time

class Pompa: 
    def __init__(self, x, y, wydajnosc, nazwa=""):
        self.x = x
        self.y = y
        self.r = 25

        self.wydajnosc = wydajnosc
        self.wlaczona = False
        self.nazwa = nazwa
        
        #Parametry czasowe, majace na celu zwiekszenie realizmu symulacji
        self.min_czas_pracy = 3.0
        self.min_czas_postoju = 2.0
        self.czas_ost_wl = 0
        self.czas_ost_wyl = 0

        #Ilosc pozostala do dopompowania (jedynie dla pompy zewnetrznej)
        self.pozostalo = 0.0

    #Ustawianie stanu wl/wyl zaleznie od spelnienia zadanego warunku
    def ustaw_stan(self, warunek: bool):
        czas = time.monotonic()
        if warunek and not self.wlaczona:
            if czas-self.czas_ost_wyl >= self.min_czas_postoju:
                self.wlaczona = True
                self.czas_ost_wl = czas
        elif not warunek and self.wlaczona:
            if czas-self.czas_ost_wl >= self.min_czas_pracy:
                self.wlaczona = False
                self.czas_ost_wyl = czas
    
    def draw(self, painter):
        #Rozne kolory pompy zaleznie od jej stanu
        if self.wlaczona:
            kolor = QColor(0, 200, 0)
        else:
            kolor = QColor(100, 100, 100)
        
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(kolor)
        painter.drawEllipse(self.x - self.r, self.y - self.r, self.r*2, self.r*2)

        #Litera M w srodku kola
        painter.setPen(Qt.white)
        font = painter.font()
        font.setPointSize(18)
        painter.setFont(font)
        painter.drawText(self.x - 10, self.y + 7, "M")


        painter.drawText(self.x - 30, self.y + self.r + 15, self.nazwa)