from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath



class Rura:
    def __init__(self, punkty=None, grubosc=12, kolor=Qt.gray):
        self.sciezki = []
        self.grubosc = grubosc
        self.kolor_rury = kolor
        self.kolor_cieczy = QColor(0, 180, 255)
        if punkty:
            self.dodaj_sciezke(punkty)
    
    def dodaj_sciezke(self, punkty): #Tworzenie rury na podstawie osobnych sciezek, w ktorej kazda moze sie osobno podswietlac, co daje mozliwosc tworzenia rozgalezien 
        sciezka = {
            "punkty": [QPointF(float(p[0]), float(p[1])) for p in punkty],
            "plynie": False
        }
        self.sciezki.append(sciezka)
    
       
    def ustaw_przeplyw(self, i, plynie):
        if 0 <= i < len(self.sciezki):
            self.sciezki[i]["plynie"] = plynie
    

    def draw(self, painter):
        pen_rura = QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        pen_ciecz = QPen(self.kolor_cieczy, self.grubosc - 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)

        for sciezka in self.sciezki: 
            punkty = sciezka["punkty"]
            if len(punkty) < 2:
                continue

            path = QPainterPath()
            path.moveTo(punkty[0])

            for p in punkty[1:]:
                path.lineTo(p)

            painter.setPen(pen_rura)
            painter.drawPath(path)

            if sciezka["plynie"]:
                painter.setPen(pen_ciecz)
                painter.drawPath(path)

  