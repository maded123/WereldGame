from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from Country_names import CountryMap
import global_state

class CountrySelector(QWidget):
    def __init__(self):
        super().__init__()
        self.country_map = CountryMap()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kies een land')
        layout = QVBoxLayout(self)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText('Voer een landnaam in...')
        layout.addWidget(self.input_field)

        self.save_button = QPushButton('Opslaan', self)
        self.save_button.clicked.connect(self.save_country)
        layout.addWidget(self.save_button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

    def save_country(self):
        country_dutch = self.input_field.text()
        english = self.country_map.get_country_name(country_dutch)
        global_state.translated_country_name = english
        self.status_label.setText(f'Geselecteerd land: {english}')
