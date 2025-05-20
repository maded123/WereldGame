
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDial, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pygame

# Initialiseer pygame mixer
pygame.mixer.init()

# De map waarin de muziekbestanden staan
muziek_map = os.path.join(os.path.dirname(__file__), "Muziek")

# Een lijst maken van alle muziekbestanden in de opgegeven map
if os.path.isdir(muziek_map):
    muziek_bestanden = [
        os.path.join(muziek_map, bestand)
        for bestand in os.listdir(muziek_map)
        if bestand.lower().endswith((".mp3", ".wav"))
    ]
else:
    muziek_bestanden = []

# Controleer of er muziekbestanden zijn gevonden
if not muziek_bestanden:
    raise Exception("Geen muziekbestanden gevonden in de map!")

class MuziekSpeler(QWidget):
    def __init__(self):
        super().__init__()
        self.huidige_index = 0
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout()

        # Label voor scrollende tekst
        self.scroll_label = QLabel("")
        self.scroll_label.setFont(QFont('Helvetica', 12))
        self.scroll_label.setStyleSheet("color: yellow; background-color: rgba(0, 0, 0, 0);")
        self.scroll_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.layout.addWidget(self.scroll_label)

        # Timer voor het scrollen van de tekst
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_text)
        self.timer.start(50)

        # Layout voor knoppen
        self.button_layout = QHBoxLayout()

        # Knoppen voor bediening
        self.speel_knop = QPushButton('Speel', self)
        self.speel_knop.setStyleSheet("background-color: rgba(0, 75, 0, 0.8); color: white;")
        self.speel_knop.clicked.connect(self.speel_muziek)
        self.button_layout.addWidget(self.speel_knop)

        self.stop_knop = QPushButton('Stop', self)
        self.stop_knop.setStyleSheet("background-color: rgba(0, 75, 0, 0.8); color: white;")
        self.stop_knop.clicked.connect(self.stop_muziek)
        self.button_layout.addWidget(self.stop_knop)

        self.volgende_knop = QPushButton('Volgende', self)
        self.volgende_knop.setStyleSheet("background-color: rgba(0, 75, 0, 0.8); color: white;")
        self.volgende_knop.clicked.connect(self.volgende_nummer)
        self.button_layout.addWidget(self.volgende_knop)

        self.vorige_knop = QPushButton('Vorige', self)
        self.vorige_knop.setStyleSheet("background-color: rgba(0, 75, 0, 0.8); color: white;")
        self.vorige_knop.clicked.connect(self.vorige_nummer)
        self.button_layout.addWidget(self.vorige_knop)

        # Volume Dial
        self.volume_dial = QDial(self)
        self.volume_dial.setRange(0, 100)
        self.volume_dial.setValue(50)
        self.volume_dial.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: white;")
        self.volume_dial.valueChanged.connect(self.aanpassen_volume)
        self.button_layout.addWidget(self.volume_dial)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.speel_muziek()

    def speel_muziek(self):
        if 0 <= self.huidige_index < len(muziek_bestanden):
            pygame.mixer.music.load(muziek_bestanden[self.huidige_index])
            pygame.mixer.music.play()
            self.update_scroll_text(f"Nu wordt afgespeeld: {os.path.basename(muziek_bestanden[self.huidige_index])}")
        else:
            QMessageBox.critical(self, "Fout", "Ongeldige index! Kies een ander nummer.")

    def stop_muziek(self):
        pygame.mixer.music.stop()
        self.update_scroll_text("Muziek gestopt.")

    def volgende_nummer(self):
        self.huidige_index = (self.huidige_index + 1) % len(muziek_bestanden)
        self.speel_muziek()

    def vorige_nummer(self):
        self.huidige_index = (self.huidige_index - 1) % len(muziek_bestanden)
        self.speel_muziek()

    def aanpassen_volume(self, waarde):
        pygame.mixer.music.set_volume(waarde / 100.0)

    def update_scroll_text(self, text):
        self.scroll_label.setText(text)
        self.scroll_label.move(self.width(), self.scroll_label.y())
        self.animate_text()

    def animate_text(self):
        x = self.scroll_label.x() - 2
        if x + self.scroll_label.width() < 0:
            x = self.width()
        self.scroll_label.move(x, self.scroll_label.y())

if __name__ == '__main__':
    app = QApplication([])
    speler = MuziekSpeler()
    speler.show()
    app.exec_()
