import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
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

        self.temperatura = 20.0
        self.max_temperatura = 80.0
        self.temperatura_otoczenia = 20.0
        self.wspolczynnik_chlodzenia = self.temperatura_otoczenia / 1000.0

    def dodaj_ciecz(self, ilosc, temperatura_cieczy):
        wolne = self.pojemnosc - self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        
        if self.aktualna_ilosc + dodano > 0:
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

#Okno do zmiany parametrow ukladu
class Parametry(QDialog):
    def __init__(self, symulacja):
        super().__init__()
        self.symulacja = symulacja
        self.setWindowTitle("Parametry ukladu")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        #Suwak predkosci przeplywu rur
        self.label_flow = QLabel(f"Predkosc przeplywu rur: {symulacja.flow_speed}")
        self.slider_flow = QSlider(Qt.Horizontal)
        self.slider_flow.setMinimum(1)
        self.slider_flow.setMaximum(300)
        self.slider_flow.setValue(int(symulacja.flow_speed*100))
        self.slider_flow.valueChanged.connect(self.zmien_flow)

        #Suwak wydajnosci pompy
        self.label_pompa = QLabel(f"Wydajnosc pompy: {symulacja.p1.wydajnosc}")
        self.slider_pompa = QSlider(Qt.Horizontal)
        self.slider_pompa.setMinimum(1)
        self.slider_pompa.setMaximum(300)
        self.slider_pompa.setValue(int(symulacja.p1.wydajnosc*100))
        self.slider_pompa.valueChanged.connect(self.zmien_wydajnosc)

        #Dodanie do layoutu
        layout.addWidget(self.label_flow)
        layout.addWidget(self.slider_flow)
        layout.addSpacing(10)
        layout.addWidget(self.label_pompa)
        layout.addWidget(self.slider_pompa)
        self.setLayout(layout)

    
    def zmien_flow(self, value):
        self.symulacja.flow_speed = value / 100
        self.label_flow.setText(f"Predkosc przeplywu rur: {self.symulacja.flow_speed}")

    def zmien_wydajnosc(self, value):
        self.symulacja.p1.wydajnosc = value / 100
        self.label_pompa.setText(f"Wydajnosc pompy: {self.symulacja.p1.wydajnosc}")

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

    def wlacz(self):
        self.wlaczona = not self.wlaczona
    
    def grzej(self):
        if self.zbiornik.czy_pusty():
            self.wlaczona = False
            return
        if self.zbiornik.temperatura <= self.zbiornik.max_temperatura:
            self.wlaczona = True
            delta_temperatury = self.moc * self.efektywnosc
            self.zbiornik.dodaj_temperature(delta_temperatury)
        
        if self.wlaczona:
            delta_ciecz = self.moc* self.parowanie
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






    
 

    

        






class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()

        self.running = False
        self.flow_speed = 0.8

        self.setWindowTitle("Kaskada: Dol -> Gora")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #222;")

        #Inicializacja zbiornikow
        self.z1 = Zbiornik(50, 50, nazwa = "Zbiornik1")
        self.z1.aktualna_ilosc = 100.0; self.z1.aktualizuj_poziom()
        self.z2 = Zbiornik(400, 50, nazwa ="Zbiornik2")
        self.z3 = Zbiornik(600, 350, nazwa = "Zbiornik3")
        self.z4 = Zbiornik(300, 350, nazwa = "Zbiornik4")
        self.zbiorniki = [self.z1, self.z2, self.z3, self.z4]

    
        #Punkty przylaczen rury 1 (Zbiornik 1-2)
        p_start = self.z1.punkt_gora_srodek()
        p_koniec = self.z2.punkt_gora_srodek()
        mid_y = (p_start[1] + p_koniec[1]) / 2
        self.rura1 = Rura([p_start, (p_start[0], mid_y), (p_koniec[0], mid_y), p_koniec])

        #Punkty przylaczen rury 2 (Zbiornik 2-3)
        p_start2 = self.z2.punkt_dol_srodek()
        p_koniec2 = self.z3.punkt_gora_srodek()
        mid_y2 = (p_start2[1] + p_koniec2[1]) / 2
        self.rura2 = Rura([p_start2, (p_start2[0], mid_y2), (p_koniec2[0], mid_y2), p_koniec2])


        #Punkty przylaczen rury 3 (Zbiornik 3-4)
        p_start3 = self.z3.punkt_dol_srodek()
        p_koniec3 = self.z4.punkt_dol_srodek()
        mid_y3 = (p_start3[1] + p_koniec3[1]) / 2
        self.rura3 = Rura([p_start3, (p_start3[0], mid_y3), (p_koniec3[0], mid_y3), p_koniec3])

        #Punkty przylaczen rury 4 (Zbiornik 4-1, zamkniecie obiegu)
        p_start4 = self.z4.punkt_gora_srodek()
        p_koniec4 = self.z1.punkt_dol_srodek()
        mid_y4 = (p_start4[1] + p_koniec[1]) / 2
        self.rura4 = Rura([p_start4, (p_start4[0], mid_y4), (p_koniec4[0], mid_y4), p_koniec4])

        self.rury = [self.rura1, self.rura2, self.rura3, self.rura4]


        #Pompy
        self.p1 = Pompa(230, 270, self.z4, self.z1, self.rura4, 0.9, nazwa="Pompa1")
        self.pompy = [self.p1]

        #Grzalki
        self.g1 = Grzalka(100, 120, self.z1, 1500, nazwa="Grzalka1")
        self.grzalki = [self.g1]



        #Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)


        #Przycisk ON/OFF     
        self.btn = QPushButton("ON/OFF", self) 
        self.btn.setGeometry(50, 500, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.przelacz_symulacje)

        #Przycisk ON/OFF pompy 1
        self.btn2 = QPushButton("POMPA1 ON/OFF", self)
        self.btn2.setGeometry(50, 550, 100, 30)
        self.btn2.setStyleSheet("background-color: #444; color: white;")
        self.btn2.clicked.connect(lambda: (self.p1.wlacz(), self.update()))

        #Wejscie do ustawien 
        self.btn3 = QPushButton("Parametry", self)
        self.btn3.setGeometry(750, 550, 100, 30)
        self.btn3.setStyleSheet("background-color: #444; color: white;")
        self.btn3.clicked.connect(self.zmien_parametry)
        self.parametry = Parametry(self)

        self.btn4 = QPushButton("GRZ Z1 ON/OFF", self)
        self.btn4.setGeometry(50, 450, 100, 30)
        self.btn4.setStyleSheet("background-color: #444; color: white;")
        self.btn4.clicked.connect(self.g1.wlacz)
      





    def przelacz_symulacje(self): #Przelaczenie symulacji ON/OFF
        if self.running: self.timer.stop()
        else: self.timer.start(20)
        self.running = not self.running

    def logika_przeplywu(self):
        self.p1.pompuj()
        self.g1.grzej()
        for z in self.zbiorniki: z.chlodz()

        plynie_1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            ilosc = self.z1.usun_ciecz(self.flow_speed)
            self.z2.dodaj_ciecz(ilosc, self.z1.temperatura)
            plynie_1 = True
        self.rura1.ustaw_przeplyw(plynie_1)
    
        plynie_2 = False
        if self.z2.aktualna_ilosc > 5.0 and not self.z3.czy_pelny():
            ilosc = self.z2.usun_ciecz(self.flow_speed)
            self.z3.dodaj_ciecz(ilosc, self.z2.temperatura)
            plynie_2 = True
        self.rura2.ustaw_przeplyw(plynie_2)
        self.update()

        plynie_3 = False
        if self.z3.aktualna_ilosc > 5.0 and not self.z4.czy_pelny():
            ilosc = self.z3.usun_ciecz(self.flow_speed)
            self.z4.dodaj_ciecz(ilosc, self.z3.temperatura)
            plynie_3 = True
        self.rura3.ustaw_przeplyw(plynie_3)
        self.update()
            

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for r in self. rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)
        for x in self.pompy: x.draw(p)
        for g in self.grzalki: g.draw(p)
    
    def zmien_parametry(self):
        self.parametry.show()
        

if __name__ == '__main__': #Glowne okno
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec_())




