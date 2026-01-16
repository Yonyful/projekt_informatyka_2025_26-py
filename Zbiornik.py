from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath

class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0

        self.temperatura = 20.0
        self.max_temperatura = 40.0
        self.temperatura_otoczenia = 20.0
        self.wspolczynnik_chlodzenia = self.temperatura_otoczenia / 1000.0

    def dodaj_ciecz(self, ilosc, temperatura_cieczy):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        
        if self.aktualna_ilosc + dodano > 0: #Przekazywana jest rowniez temperatura cieczy pomiedzy zbiornikami 
            nowa_temp = (self.aktualna_ilosc * self.temperatura + dodano * temperatura_cieczy) / (self.aktualna_ilosc + dodano)
            self.temperatura = nowa_temp
        
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano
    

    def usun_ciecz(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc -= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def set_empty(self):
        self.aktualna_ilosc = 0.0
        self.aktualizuj_poziom()

    def set_full(self):
        self.aktualna_ilosc = 100.0
        self.aktualizuj_poziom() 

    def dodaj_temperature(self, ilosc): 
        self.temperatura += ilosc
        self.temperatura = max(0, self.temperatura)
    
    def chlodz(self):
        ilosc = self.temperatura - self.temperatura_otoczenia
        self.temperatura -= ilosc * self.wspolczynnik_chlodzenia

    def czy_pusty(self): return self.aktualna_ilosc <= 0.1
    def czy_pelny(self): return self.aktualna_ilosc >= self.pojemnosc - 0.1

    def punkt_gora_srodek(self): return (self.x + self.width/2, self.y)
    def punkt_dol_srodek(self): return (self.x + self.width/2, self.y + self.height)

    def draw(self, painter):
        if self.poziom > 0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height - h_cieczy
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0,120,255,200))
            painter.drawRect(int(self.x+3), int(y_start), int(self.width - 6),int(h_cieczy - 2))

        pen = QPen(Qt.white, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        painter.setPen(Qt.white)
        painter.drawText(int(self.x), int(self.y - 10), self.nazwa)
        painter.drawText(int(self.x), int(self.y + self.height + 15), f"{self.temperatura:.1f} °C")