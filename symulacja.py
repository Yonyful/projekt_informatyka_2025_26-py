import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from grzalka import Grzalka
from rura import Rura
from pompa import Pompa 
from zbiornik import Zbiornik
from parametry import Parametry
from Alarmy import Alarmy 


    
class SymulacjaKaskady(QWidget):
    def __init__(self):
        super().__init__()

        self.running = False
        self.flow_speed = 0.3

        self.okno_alramy = Alarmy()
        self.plynie_3 = False

        self.setWindowTitle("Kaskada: Dol -> Gora")
        self.setFixedSize(900, 600)
        self.setStyleSheet("background-color: #222;")

        #Inicializacja zbiornikow
        self.z1 = Zbiornik(50, 50, nazwa = "Zbiornik1")
        self.z1.aktualna_ilosc = 100.0; self.z1.aktualizuj_poziom()
        self.z2 = Zbiornik(400, 50, nazwa ="Zbiornik2")
        self.z2.aktualna_ilosc = 50.0; self.z2.aktualizuj_poziom()
        self.z3 = Zbiornik(600, 350, nazwa = "Zbiornik3")
        self.z4 = Zbiornik(300, 350, nazwa = "Zbiornik4")
        self.zbiorniki = [self.z1, self.z2, self.z3, self.z4]

        #Minimalna calkowita ilosc cieczy we wszystkich zbiornikach
        self.minimalna_calkowita_ilosc = 50.0


        #Punkty przylaczen rury 1 (Zbiornik 1-2)
        p_start = self.z1.punkt_gora_srodek()
        p_koniec = self.z2.punkt_gora_srodek()
        mid_y = (p_start[1] + p_koniec[1]) / 2
        self.rura1 = Rura([p_start, (p_start[0], mid_y), (p_koniec[0], mid_y), p_koniec])

        #Punkty przylaczen rury 2 (Zbiornik 2-3)
        p_start2 = self.z2.punkt_dol_srodek()
        p_koniec2 = self.z3.punkt_gora_srodek()
        mid_y2 = (p_start2[1] + p_koniec2[1]) / 2
        rozgalezienie_r2 = (p_start2[0], p_start2[1] + 90)
        self.rura2 = Rura()
        #Pionowo w dol
        self.rura2.dodaj_sciezke([p_start2, rozgalezienie_r2])
        #Galaz do Z3
        self.rura2.dodaj_sciezke([rozgalezienie_r2, (rozgalezienie_r2[0], mid_y2), (p_koniec2[0], mid_y2), p_koniec2])
        #Galaz do Z4
        p_koniec5 = self.z4.punkt_dol_srodek()
        przesuniecie_5 = self.z4.y + 140
        self.rura2.dodaj_sciezke([rozgalezienie_r2, (rozgalezienie_r2[0], przesuniecie_5), (p_koniec5[0], przesuniecie_5), p_koniec5])


        #Punkty przylaczen rury 3 (Zbiornik 3-4)
        p_start3 = self.z3.punkt_dol_srodek()
        p_koniec3 = self.z4.punkt_dol_srodek()
        mid_y3 = (p_start3[1] + p_koniec3[1]) / 2
        self.rura3 = Rura([p_start3, (p_start3[0], mid_y3 + 30), (p_koniec3[0], mid_y3 + 30), p_koniec3])

        #Punkty przylaczen rury 4 (Zbiornik 4-1)
        p_start4 = self.z4.punkt_gora_srodek()
        p_koniec4 = self.z1.punkt_dol_srodek()
        mid_y4 = (p_start4[1] + p_koniec[1]) / 2
        self.rura4 = Rura([p_start4, (p_start4[0], mid_y4), (p_koniec4[0], mid_y4), p_koniec4])


        self.rury = [self.rura1, self.rura2, self.rura3, self.rura4]


        #Pompy
        self.p1 = Pompa(230, 270, 0.9, nazwa="Pompa1")
        self.pzew = Pompa(800, 100, 0.3, nazwa="PompaZew")
        self.pompy = [self.p1, self.pzew]

        #Grzalki
        self.g1 = Grzalka(350, 420, self.z4, 150, nazwa="Grzalka1")
        self.grzalki = [self.g1]



        #Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)


        #Przycisk ON/OFF     
        self.btn = QPushButton("ON/OFF", self) 
        self.btn.setGeometry(50, 500, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.przelacz_symulacje)

        #Wejscie do ustawien 
        self.btn2 = QPushButton("Parametry", self)
        self.btn2.setGeometry(750, 550, 100, 30)
        self.btn2.setStyleSheet("background-color: #444; color: white;")
        self.btn2.clicked.connect(self.zmien_parametry)
        self.parametry = Parametry(self)

        #Wejscie do alarmow
        self.btn3 = QPushButton("Alarmy", self)
        self.btn3.setGeometry(750, 500, 100, 30)
        self.btn3.setStyleSheet("background-color: #444; color: white;")
        self.btn3.clicked.connect(self.otworz_alarmy)



        
    def przelacz_symulacje(self): #Przelaczenie symulacji ON/OFF
        if self.running: self.timer.stop()
        else: self.timer.start(20)
        self.running = not self.running
    
    def calkowita_ilosc(self): #Funkcja zliczajaca calkowita ilosc wody w zbiornikach 
        return sum(z.aktualna_ilosc for z in self.zbiorniki)
    
    def sprawdz_alarmy(self):
        alarmy = []
        for z in self.zbiorniki:
            #Alarm zbyt wysokiej temperatury
            if z.temperatura >= z.max_temperatura + 3:
                alarmy.append(f"{z.nazwa}: Wysoka temperatura cieczy {z.temperatura:.1f} °C")
            #Alarm przepelnienia zbiornika
            if z.czy_pelny():
                alarmy.append(f"{z.nazwa} jest pelny")
            #Alarm niskiej ilosci cieczy w zbiorniku
            if z.aktualna_ilosc < 5.0:
                alarmy.append(f"{z.nazwa}: niski poziom cieczy")
        
        if self.calkowita_ilosc() < self.minimalna_calkowita_ilosc:
            alarmy.append("Zbyt niski calkowity poziom cieczy w ukladzie")

        self.okno_alramy.wstaw_alarmy(alarmy)

    
   


    def logika_przeplywu(self):

        #Logika pompy zewnetrznej, ktora dopompowuje wode gdy za duzo jej odparuje
        calkowita = self.calkowita_ilosc()
        
        #Jezeli spadlo ponizej minimum, zlecane jest dopompowanie konkretnej ilosci wody
        if calkowita < self.minimalna_calkowita_ilosc and self.pzew.pozostalo <= 0:
            self.pzew.pozostalo = 10 * self.pzew.wydajnosc
        #Pompa zewnetrzna bedzie pracowac jedynie gdy ma cos do dopompowania
        warunek_pzew = self.pzew.pozostalo > 0
        self.pzew.ustaw_stan(warunek_pzew)
        if self.pzew.wlaczona:
            ilosc = min(self.pzew.wydajnosc, self.pzew.pozostalo)
            self.z1.dodaj_ciecz(ilosc, 20.0)
            self.pzew.pozostalo -= ilosc
        
        

        #Logika grzalki 1
        if not self.g1.wlaczona and self.z4.temperatura <= self.z4.max_temperatura - 2:
            self.g1.wlaczona = True
        elif self.g1.wlaczona and self.z4.temperatura >= self.z4.max_temperatura + 2:
            self.g1.wlaczona = False
        if self.g1.wlaczona:
            self.g1.grzej()
       
        #Logika pompy 1 i rury4
        warunek_p1 = (not self.z4.czy_pusty() and not self.z1.czy_pelny() and self.z4.temperatura >= self.z4.max_temperatura)
        self.p1.ustaw_stan(warunek_p1)
        if self.p1.wlaczona:
            ilosc = self.z4.usun_ciecz(self.p1.wydajnosc)
            self.z1.dodaj_ciecz(ilosc, self.z4.temperatura)
            self.rura4.ustaw_przeplyw(0, True)
        else:
            self.rura4.ustaw_przeplyw(0, False)
           

        #Wszystkie zbiorniki "samoczynnie" sie chlodza
        for z in self.zbiorniki: z.chlodz()

        #Logika przelywu rury 1 Z1-Z2
        plynie_1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            ilosc = self.z1.usun_ciecz(self.flow_speed)
            self.z2.dodaj_ciecz(ilosc, self.z1.temperatura)
            plynie_1 = True
        self.rura1.ustaw_przeplyw(0, plynie_1)
        
        #Logika przeplywu rury 2 Z2-Z3
        plynie_2 = False
        if self.z2.aktualna_ilosc > 5.0 and not self.z3.czy_pelny():
            ilosc = self.z2.usun_ciecz(self.flow_speed/2)
            self.z3.dodaj_ciecz(ilosc, self.z2.temperatura)
            plynie_2 = True
        self.rura2.ustaw_przeplyw(1, plynie_2)

        #Logika przeplywu rury 3 Z3-Z4
        if not self.plynie_3:
            if self.z3.aktualna_ilosc > 22.0 and self.z4.aktualna_ilosc <= 90.0 and self.z3.temperatura <= self.z3.temperatura_otoczenia + 2:
                self.plynie_3 = True
        else:
            if self.z3.aktualna_ilosc < 18.0 or self.z4.czy_pelny() or self.z3.temperatura >= self.z3.temperatura_otoczenia + 3:
                self.plynie_3 = False
        if self.plynie_3:
            ilosc = self.z3.usun_ciecz(self.flow_speed)
            self.z4.dodaj_ciecz(ilosc, self.z3.temperatura)
        self.rura3.ustaw_przeplyw(0, self.plynie_3)


        #Logika przeplywu rury 5
        plynie_5 = False
        if self.z2.aktualna_ilosc > 5.0 and self.z4.aktualna_ilosc <= 90.0:
            ilosc = self.z2.usun_ciecz(self.flow_speed/2)
            self.z4.dodaj_ciecz(ilosc, self.z2.temperatura)
            plynie_5 = True
        self.rura2.ustaw_przeplyw(0, plynie_5 or plynie_2)
        self.rura2.ustaw_przeplyw(2, plynie_5)


        self.sprawdz_alarmy()
        self.update()
            
    def paintEvent(self, event): #Procedury rysujace elementy 
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for r in self. rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)
        for x in self.pompy: x.draw(p)
        for g in self.grzalki: g.draw(p)
    
    def zmien_parametry(self): #Wejscie do okna ustawien 
        self.parametry.show()
    
    def otworz_alarmy(self):
        self.okno_alramy.show()
        

if __name__ == '__main__': #Glowne okno
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec_())




