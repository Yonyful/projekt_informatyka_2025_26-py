from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QLabel, QSlider, QVBoxLayout, QDoubleSpinBox
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath


#Okno do zmiany parametrow ukladu
class Parametry(QDialog):
    def __init__(self, symulacja):
        super().__init__()
        self.symulacja = symulacja
        self.setWindowTitle("Parametry ukladu")
        self.setFixedSize(800, 800)
        self.setStyleSheet("background-color: #222;")

        layout = QVBoxLayout()
        layout.addSpacing(10)

        #Suwak predkosci przeplywu rur
        self.label_flow = QLabel(f"Predkosc przeplywu rur: {symulacja.flow_speed}")
        self.label_flow.setStyleSheet("color: white;")
        self.slider_flow = QSlider(Qt.Horizontal)
        self.slider_flow.setMinimum(1)
        self.slider_flow.setMaximum(100)
        self.slider_flow.setValue(int(symulacja.flow_speed*100))
        self.slider_flow.valueChanged.connect(self.zmien_flow)



        #Zmiana wydajnosci pomp
        for i, pompa in enumerate(self.symulacja.pompy, start = 1):
            label = QLabel(f"Wydajnosc pompy {pompa.nazwa}: {pompa.wydajnosc}")
            label.setStyleSheet("color: white;")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(300)
            slider.setValue(int(pompa.wydajnosc*100))
            slider.valueChanged.connect(lambda value, p = pompa, l=label: self.zmien_wydajnosc(p, l, value))

            layout.addWidget(label)
            layout.addWidget(slider)

        #Zmiana mocy grzalki
        for i, grzalka in enumerate(self.symulacja.grzalki, start=1):
            label = QLabel(f"Moc grzalki {grzalka.nazwa}: {grzalka.moc} W")
            label.setStyleSheet("color: white;")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(10000)
            slider.setValue(int(grzalka.moc*10))
            slider.valueChanged.connect(lambda value, g = grzalka, l = label: self.zmien_moc(g, l, value))
            layout.addWidget(label)
            layout.addWidget(slider)

        #Zmiana maksymalnej temperatury cieczy zbiornikow
        for i, zbiornik in enumerate(self.symulacja.zbiorniki, start=1):
            label = QLabel(f"Maksymalna temperatura {zbiornik.nazwa}: {zbiornik.max_temperatura} °C")
            label.setStyleSheet("color: white;")
            box = QDoubleSpinBox()
            box.setStyleSheet("color: white;")
            box.setMinimum(0.0)
            box.setMaximum(200.0)
            box.setDecimals(1)
            box.setValue(zbiornik.max_temperatura)
            box.setSuffix(" °C")

            box.valueChanged.connect(lambda value, z=zbiornik, l=label: self.zmien_max_temp(z, l, value))
            layout.addWidget(label)
            layout.addWidget(box)

     
        #Dodanie do layoutu
        layout.addWidget(self.label_flow)
        layout.addWidget(self.slider_flow)
        self.setLayout(layout)

    
    def zmien_flow(self, value):
        self.symulacja.flow_speed = value / 100
        self.label_flow.setText(f"Predkosc przeplywu rur: {self.symulacja.flow_speed}")

    def zmien_wydajnosc(self, pompa, label, value,):
        pompa.wydajnosc = value / 100
        label.setText(f"Wydajnosc pompy {pompa.nazwa}: {pompa.wydajnosc}")
    
    def zmien_moc(self, grzalka, label, value):
        grzalka.moc = value / 10
        label.setText(f"Moc grzalki {grzalka.nazwa}: {grzalka.moc} W")
    
    def zmien_max_temp(self, zbiornik, label, value):
        zbiornik.max_temperatura = value
        label.setText(f"Maksymalna temperatura {zbiornik.nazwa}: {value} °C")

