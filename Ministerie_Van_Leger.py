import sys
import os
import random
import names
import pandas as pd
import world_bank_data as wb
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# Globale variabele om de Engelse landnaam op te slaan
global_translated_country_name = None


class MinisterieVanLegerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ministerie van Defensie')
        self.setGeometry(100, 100, 1000, 600)

        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Voer de naam van een land in")
        self.input_field.returnPressed.connect(self.update_data)
        left_layout.addWidget(self.input_field)

        self.country_label = QLabel("Gekozen land: ", self)
        self.country_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        left_layout.addWidget(self.country_label)

        self.table = QTableWidget(self)
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
        left_layout.addWidget(self.table)

        self.save_button = QPushButton("Opslaan", self)
        self.save_button.clicked.connect(self.manual_save_data)
        left_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Laad een saved file", self)
        self.load_button.clicked.connect(self.load_data_from_file)
        left_layout.addWidget(self.load_button)

        right_layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)
        self.image_label.setFrameShape(QFrame.Box)
        right_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        self.minister_label = QLabel("Dit is uw huidige minister van defensie", self)
        self.minister_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.minister_label)

        self.name_label = QLabel("", self)
        self.name_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.name_label)
        right_layout.setSpacing(2)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.load_random_image_and_name()
        self.minister_label.setStyleSheet("color: white;")
        self.name_label.setStyleSheet("color: white;")

    def manual_save_data(self):
        try:
            if self.table.rowCount() > 0:
                filename, _ = QFileDialog.getSaveFileName(
                    self, "Sla bestand op", "", "CSV Files (*.csv);;All Files (*)")
                if filename:
                    if not filename.endswith(".csv"):
                        filename += ".csv"
                    data = {
                        self.table.horizontalHeaderItem(0).text(): [
                            self.table.item(row, 0).text() for row in range(self.table.rowCount())
                        ],
                        self.table.horizontalHeaderItem(1).text(): [
                            self.table.item(row, 1).text() for row in range(self.table.rowCount())
                        ],
                    }
                    df = pd.DataFrame(data)
                    df['Land'] = self.country_label.text().replace("Gekozen land: ", "")
                    df.to_csv(filename, index=False)
                    print(f"Data opgeslagen in {filename}")
                else:
                    print("Opslaan geannuleerd.")
            else:
                print("Geen data beschikbaar om op te slaan.")
        except Exception as e:
            print(f"Er is een fout opgetreden tijdens het opslaan: {str(e)}")

    def load_data_from_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Kies een opgeslagen data bestand", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            loaded_data = pd.read_csv(filename)
            self.display_loaded_data(loaded_data)

    def display_loaded_data(self, data):
        country_name = data.iloc[0]['Land']
        self.country_label.setText(f"Gekozen land: {country_name}")
        data = data.drop(columns=['Land'])
        indicators = data.iloc[:, 0].tolist()
        values = data.iloc[:, 1].tolist()

        self.table.setColumnCount(2)
        self.table.setRowCount(len(indicators))
        self.table.setHorizontalHeaderLabels(['Indicator', 'Waarde'])

        for i, indicator in enumerate(indicators):
            indicator_item = QTableWidgetItem(indicator)
            indicator_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, indicator_item)
            value_item = QTableWidgetItem(values[i])
            value_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, value_item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setStretchLastSection(False)

    def update_data(self):
        global global_translated_country_name
        country_name = global_translated_country_name if global_translated_country_name else self.input_field.text()
        self.country_label.setText(f"Gekozen land: {country_name}")
        country_data = self.get_country_military_indicators(country_name)
        if country_data is not None:
            indicators = list(country_data.columns)[2:]
            values = [self.format_value(ind, country_data.iloc[0][ind]) for ind in indicators]
            self.table.setColumnCount(2)
            self.table.setRowCount(len(indicators))
            self.table.setHorizontalHeaderLabels(['Indicator', 'Waarde'])
            for i, indicator in enumerate(indicators):
                indicator_item = QTableWidgetItem(indicator)
                indicator_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 0, indicator_item)
                value_item = QTableWidgetItem(values[i])
                value_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 1, value_item)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            self.table.horizontalHeader().setStretchLastSection(False)
            self.table.verticalHeader().setStretchLastSection(False)
        else:
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            self.table.setHorizontalHeaderLabels([])
            self.table.clearContents()

    def load_random_image_and_name(self):
        image_folder = "gezichten"
        images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        if images:
            random_image = random.choice(images)
            pixmap = QPixmap(os.path.join(image_folder, random_image))
            if pixmap.isNull():
                self.image_label.setText("Afbeelding niet gevonden")
            else:
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
        else:
            self.image_label.setText("Geen afbeeldingen gevonden in de map")
        random_name = names.get_full_name()
        self.name_label.setText(f"Uw minister heet: {random_name}")

    def get_country_military_indicators(self, country_name):
        countries = wb.get_countries()
        indicators = {
            'Militaire Uitgaven (US$)': 'MS.MIL.XPND.CD',
            'Militaire Uitgaven (% van BBP)': 'MS.MIL.XPND.GD.ZS',
            'Personeel in de Strijdkrachten': 'MS.MIL.TOTL.P1',
        }
        data = {}
        for name, code in indicators.items():
            data[name] = wb.get_series(code, id_or_value='id', simplify_index=True, mrv=1)
        df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
        for name, series in data.items():
            df[name] = series
        country_data = df[df['country'].str.lower() == country_name.lower()]
        return country_data if not country_data.empty else None

    def format_value(self, indicator, value):
        if pd.isna(value):
            return "N/A"
        if indicator.endswith('(US$)'):
            return f"${value:,.2f}"
        elif '(%' in indicator:
            return f"{value:.2f}%"
        else:
            return f"{value:,.0f}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MinisterieVanLegerApp()
    main_app.show()
    sys.exit(app.exec_())
