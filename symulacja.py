import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from grzalka import Grzalka
from rura import Rura
from pompa import Pompa 
from zbiornik import Zbiornik
from parametry import Parametry


    
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
        self.g1 = Grzalka(100, 120, self.z1, 150, nazwa="Grzalka1")
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




