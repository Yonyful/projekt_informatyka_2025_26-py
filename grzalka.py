from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath


class Grzalka:
    def __init__(self, x, y, zbiornik, moc, nazwa=""):
        self.x = x
        self.y = y
        self.zbiornik = zbiornik
        self.moc = moc
        self.nazwa = nazwa
        self.wlaczona = False

        #Uproszczone parametry fizyczne
        self.efektywnosc = 0.0005 #Ile stopnii celsjusza na jednostke mocy
        self.parowanie = 0.00005 #Ile objetosci wyparowuje na jednostke mocy

    def wlacz(self): #Funkcja wlaczajaca, do debugowania
        self.wlaczona = not self.wlaczona
    
    def grzej(self):
        if self.zbiornik.czy_pusty():
            self.wlaczona = False
            return
        delta_temperatury = self.moc * self.efektywnosc
        self.zbiornik.dodaj_temperature(delta_temperatury)
        delta_ciecz = self.moc * self.parowanie
        self.zbiornik.usun_ciecz(delta_ciecz)
            
    
    def draw(self, painter):
        if self.wlaczona:
            kolor = QColor(255, 100, 0)
        else:
            kolor = QColor(80, 80, 80)
        
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(kolor)
        painter.drawRect(self.x - 20, self.y - 10, 40, 20)
        #Tekst
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(self.x - 20, self.y + 25, self.nazwa)