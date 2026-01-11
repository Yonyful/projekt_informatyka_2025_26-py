import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath

class Rura:
    def __init__(self, punkty, grubosc=12, kolor=Qt.gray):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = kolor
        self.kolor_cieczy = QColor(0, 180, 255)
        self.czy_plynie = False
    def ustaw_przeplyw(self, plynie):
        self.czy_plynie = plynie
    def draw(self, painter):
        if len(self.punkty) < 2:
            return
        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)

        pen_rura = QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen_rura)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc - 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_ciecz)
            painter.drawPath(path)
        
class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0
    def dodaj_ciecz(self, ilosc):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
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

class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kaskada: Dol -> Gora")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #222;")
        self.z1 = Zbiornik(50, 50, nazwa = "Zbiornik1")
        self.z1.aktualna_ilosc = 100.0; self.z1.aktualizuj_poziom()

        self.z2 = Zbiornik(350, 200, nazwa ="Zbiornik2")
        self.z3 = Zbiornik(650, 350, nazwa = "Zbiornik3")
        self.zbiorniki = [self.z1, self.z2, self.z3]

        p_start = self.z1.punkt_dol_srodek()
        p_koniec = self.z2.punkt_gora_srodek()
        mid_y = (p_start[1] + p_koniec[1]) / 2

        self.rura1 = Rura([p_start, (p_start[0], mid_y), (p_koniec[0], mid_y), p_koniec])

        p_start2 = self.z2.punkt_dol_srodek()
        p_koniec2 = self.z3.punkt_gora_srodek()
        mid_y2 = (p_start2[1] + p_koniec2[1]) / 2
        self.rura2 = Rura([p_start2, (p_start2[0], mid_y2), (p_koniec2[0], mid_y2), p_koniec2])

        self.rury = [self.rura1, self.rura2]
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)



        self.btn = QPushButton("ON/OFF", self)
        self.btn.setGeometry(50, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.przelacz_symulacje)

        self.btn2 = QPushButton("Z1 FULL", self)
        self.btn2.setGeometry(50, 500, 100, 30)
        self.btn2.setStyleSheet("background-color: #444; color: white;")
        self.btn2.clicked.connect(self.z1.set_full)

    
        self.btn3 = QPushButton("Z1 EMPTY", self)
        self.btn3.setGeometry(160, 500, 100, 30)
        self.btn3.setStyleSheet("background-color: #444; color: white;")
        self.btn3.clicked.connect(self.z1.set_empty)
      

        self.btn4 = QPushButton("Z2 FULL", self)
        self.btn4.setGeometry(50, 460, 100, 30)
        self.btn4.setStyleSheet("background-color: #444; color: white;")
        self.btn4.clicked.connect(self.z2.set_full)


        self.btn5 = QPushButton("Z2 EMPTY", self)
        self.btn5.setGeometry(160, 460, 100, 30)
        self.btn5.setStyleSheet("background-color: #444; color: white;")
        self.btn5.clicked.connect(self.z2.set_empty)

        self.btn6 = QPushButton("Z3 FULL", self)
        self.btn6.setGeometry(50, 420, 100, 30)
        self.btn6.setStyleSheet("background-color: #444; color: white;")
        self.btn6.clicked.connect(self.z3.set_full)

        self.btn7 = QPushButton("Z3 EMPTY", self)
        self.btn7.setGeometry(160, 420, 100, 30)
        self.btn7.setStyleSheet("background-color: #444; color: white;")
        self.btn7.clicked.connect(self.z3.set_empty)





        self.running = False
        self.flow_speed = 0.8
    def przelacz_symulacje(self):
        if self.running: self.timer.stop()
        else: self.timer.start(20)
        self.running = not self.running
    def logika_przeplywu(self):
        plynie_1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            ilosc = self.z1.usun_ciecz(self.flow_speed)
            self.z2.dodaj_ciecz(ilosc)
            plynie_1 = True
        self.rura1.ustaw_przeplyw(plynie_1)
        plynie_2 = False
        if self.z2.aktualna_ilosc > 5.0 and not self.z3.czy_pelny():
            ilosc = self.z2.usun_ciecz(self.flow_speed)
            self.z3.dodaj_ciecz(ilosc)
            plynie_2 = True
        self.rura2.ustaw_przeplyw(plynie_2)
        self.update()
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for r in self. rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec_())




