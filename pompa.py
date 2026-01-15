from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath

class Pompa: 
    def __init__(self, x, y, zrodlo, cel, rura, wydajnosc, nazwa=""):
        self.x = x
        self.y = y
        self.r = 25

        self.wydajnosc = wydajnosc
        self.wlaczona = False
        self.nazwa = nazwa
        
        self.zrodlo = zrodlo
        self.cel = cel
        self.rura = rura

    def wlacz(self): #Przelaczenie dzialania pompy
        self.wlaczona = not self.wlaczona
    
    def pompuj(self): #Logika wypompowywania
        if not self.wlaczona:
            self.rura.ustaw_przeplyw(False)
            return
        if not self.zrodlo.czy_pusty() and not self.cel.czy_pelny():
            ilosc = self.zrodlo.usun_ciecz(self.wydajnosc)
            self.cel.dodaj_ciecz(ilosc, self.zrodlo.temperatura)
            self.rura.ustaw_przeplyw(True)
        else:
            self.rura.ustaw_przeplyw(False)
    

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


        painter.drawText(self.x - 25, self.y + self.r + 15, self.nazwa)