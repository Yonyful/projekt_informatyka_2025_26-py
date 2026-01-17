from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QListWidget
from datetime import datetime

class Alarmy(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alarmy")
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: #222;")

        layout = QVBoxLayout()

        self.title = QLabel("Alarmy:")
        self.title.setStyleSheet("color: white;")
       

        self.list = QListWidget()
        self.list.setStyleSheet("color: white;")

        self.btn_log = QPushButton("Pokaz historie alarmow")
        self.btn_log.setStyleSheet("color: white;")
        self.btn_log.clicked.connect(self.pokaz_historie)

        self.btn_clear = QPushButton("Wyczysc historie")
        self.btn_clear.setStyleSheet("color: white;")
        self.btn_clear.clicked.connect(self.wyczysc)
        

        
        layout.addWidget(self.btn_log)
        layout.addWidget(self.title)
        layout.addWidget(self.list)
        layout.addWidget(self.btn_clear)
        self.setLayout(layout)


        self.log = []
        self.aktualne_alarmy = set()
        self.pokaz = False


    def wstaw_alarmy(self, alarmy: list[str]): #Dodawanie alarmow do listy
        nowe_alarmy = set(alarmy)

        for alarm in nowe_alarmy - self.aktualne_alarmy:
            czas = datetime.now().strftime("%H:%M:%S")
            self.log.append(f"{czas} {alarm}")
        self.aktualne_alarmy = nowe_alarmy

        if not self.pokaz:
            self.odswiez(self.aktualne_alarmy)

    def odswiez(self, alarmy): #Funkcja odswiezajaca
        self.list.clear()
        if alarmy:
            self.list.addItems(alarmy)
        else:
            self.list.addItem("Brak alarmow")
        
    def pokaz_historie(self): #Zmiana pomiedzy aktywnymi alarmami a historia alarmow
        self.pokaz = not self.pokaz

        if self.pokaz:
            self.title.setText("Historia alarmow:")
            self.btn_log.setText("Aktywne alarmy")
            self.odswiez(self.log)
        else:
            self.title.setText("Alarmy:")
            self.btn_log.setText("Pokaz historie alarmow")
            self.odswiez(self.aktualne_alarmy)

    def wyczysc(self): #Funkcja czyszczaca historie alarmow
        self.log.clear()

        if self.pokaz: #Jezeli aktualnie jest ona wyswietlana, to lista zostanie odswiezona 
            self.odswiez(self.log)
        

        



