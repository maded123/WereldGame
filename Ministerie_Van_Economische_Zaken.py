import sys
import os
import random
import names
import pandas as pd
import world_bank_data as wb
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QTableWidget, \
    QTableWidgetItem, QHeaderView, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import uuid
from PyQt5.QtWidgets import QPushButton, QFileDialog
import global_state


class MinisterieVanEconomischeZakenApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ministerie van Economische Zaken')
        self.setGeometry(100, 100, 1000, 600)

        # Hoofd Layout
        main_layout = QHBoxLayout(self)

        # Layout voor de linkerkant (land informatie)
        left_layout = QVBoxLayout()

        # Input veld voor land
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Voer de naam van een land in")
        self.input_field.returnPressed.connect(self.update_data)
        left_layout.addWidget(self.input_field)

        # Label voor gekozen land
        self.country_label = QLabel("Gekozen land: ", self)
        self.country_label.setStyleSheet("font-weight: bold; font-size: 11pt;")  # Maak de tekst dik en 2 maten groter
        left_layout.addWidget(self.country_label)

        # Tabel om de data weer te geven
        self.table = QTableWidget(self)
        self.table.setColumnCount(0)
        self.table.setRowCount(0)

        # Instellingen voor het aanpassen van rijen en kolommen
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        left_layout.addWidget(self.table)

        # Knop om data op te slaan
        self.save_button = QPushButton("Opslaan", self)
        self.save_button.clicked.connect(self.manual_save_data)
        left_layout.addWidget(self.save_button)

        # Knop om eerder opgeslagen data te laden
        self.load_button = QPushButton("Laad een saved file", self)
        self.load_button.clicked.connect(self.load_data_from_file)
        left_layout.addWidget(self.load_button)

        # Layout voor de rechterkant (minister afbeelding)
        right_layout = QVBoxLayout()

        # Afbeeldingslabel
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)  # Stel grootte van afbeelding in
        self.image_label.setFrameShape(QFrame.Box)  # Voeg een kader rond de afbeelding toe
        right_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Label voor tekst onder afbeelding
        self.minister_label = QLabel("Dit is uw huidige minister van financiën", self)
        self.minister_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.minister_label)

        # Label voor de willekeurige naam
        self.name_label = QLabel("", self)
        self.name_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.name_label)

        # Verklein de afstand tussen de labels
        right_layout.setSpacing(2)

        # Voeg layouts toe aan de hoofd layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Zet de layout op het hoofdvenster
        self.setLayout(main_layout)

        # Laad de afbeelding en naam bij het opstarten
        self.load_random_image_and_name()

        # Pas de stijl aan voor de tekstkleur
        self.minister_label.setStyleSheet("color: white;")
        self.name_label.setStyleSheet("color: white;")

    def manual_save_data(self):
        try:
            if self.table.rowCount() > 0:
                # Open een dialoogvenster om een bestandsnaam in te voeren
                filename, _ = QFileDialog.getSaveFileName(self, "Sla bestand op", "",
                                                          "CSV Files (*.csv);;All Files (*)")

                if filename:
                    if not filename.endswith(".csv"):
                        filename += ".csv"

                    # Maak een DataFrame van de huidige data in de tabel
                    data = {
                        self.table.horizontalHeaderItem(0).text(): [self.table.item(row, 0).text() for row in
                                                                    range(self.table.rowCount())],
                        self.table.horizontalHeaderItem(1).text(): [self.table.item(row, 1).text() for row in
                                                                    range(self.table.rowCount())],
                    }
                    df = pd.DataFrame(data)

                    # Voeg de landnaam als een extra kolom toe
                    df['Land'] = self.country_label.text().replace("Gekozen land: ", "")

                    # Sla de data op in het bestand met de door de gebruiker ingevoerde naam
                    df.to_csv(filename, index=False)

                    print(f"Data opgeslagen in {filename}")
                else:
                    print("Opslaan geannuleerd.")
            else:
                print("Geen data beschikbaar om op te slaan.")
        except Exception as e:
            print(f"Er is een fout opgetreden tijdens het opslaan: {str(e)}")

    def load_data_from_file(self):
        # Open een dialoogvenster om een bestand te kiezen
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Kies een opgeslagen data bestand", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)

        if filename:
            # Lees de data van het CSV-bestand
            loaded_data = pd.read_csv(filename)

            # Update de tabel met de geladen data
            self.display_loaded_data(loaded_data)

    def display_loaded_data(self, data):
        # Haal de landnaam op uit de laatste kolom
        country_name = data.iloc[0]['Land']
        self.country_label.setText(f"Gekozen land: {country_name}")

        # Verwijder de landnaam kolom voordat je de rest van de data in de tabel zet
        data = data.drop(columns=['Land'])

        indicators = data.iloc[:, 0].tolist()  # Eerste kolom
        values = data.iloc[:, 1].tolist()  # Tweede kolom

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
        # Gebruik de gekozen naam uit het keuzetabblad indien beschikbaar
        country_name = global_state.translated_country_name if global_state.translated_country_name else self.input_field.text()
        self.country_label.setText(f"Gekozen land: {country_name}")

        country_data = self.get_country_economic_indicators(country_name)

        if country_data is not None:
            # In plaats van kolommen, maken we nu één kolom voor de indicatoren en één voor de waarden
            indicators = list(country_data.columns)[2:]  # Sla de eerste twee kolommen over ('region', 'country')
            values = [self.format_value(indicator, country_data.iloc[0][indicator]) for indicator in indicators]

            display_pairs = [(ind, val) for ind, val in zip(indicators, values) if val != "N/A"]

            self.table.setColumnCount(2)
            self.table.setRowCount(len(display_pairs))

            self.table.setHorizontalHeaderLabels(['Indicator', 'Waarde'])

            for i, (indicator, value) in enumerate(display_pairs):
                indicator_item = QTableWidgetItem(indicator)
                indicator_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 0, indicator_item)

                value_item = QTableWidgetItem(value)
                value_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 1, value_item)

            # Zorg ervoor dat de cellen zich aanpassen aan de inhoud
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

            # De tabel headers kunnen nog steeds handmatig worden aangepast
            self.table.horizontalHeader().setStretchLastSection(False)
            self.table.verticalHeader().setStretchLastSection(False)
        else:
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            self.table.setHorizontalHeaderLabels([])
            self.table.clearContents()

    def load_random_image_and_name(self):
        # Kies een willekeurige afbeelding uit de map "Gezichten"
        image_folder = os.path.join(os.path.dirname(__file__), 'Gezichten')
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

        # Genereer een willekeurige naam en zet de tekst met de naam direct onder de minister_label
        random_name = names.get_full_name()
        self.name_label.setText(f"Uw minister heet: {random_name}")

    def get_country_economic_indicators(self, country_name):
        # Data ophalen van de Wereldbank
        countries = wb.get_countries()

        indicators = {
            'BBP (totaal)': 'NY.GDP.MKTP.CD',
            'Bevolking': 'SP.POP.TOTL',
            'BBP per Hoofd van de Bevolking': 'NY.GDP.PCAP.CD',
            'Inflatie (CPI)': 'FP.CPI.TOTL',
            'Werkloosheid': 'SL.UEM.TOTL.ZS',
            'Levensverwachting': 'SP.DYN.LE00.IN',
            'Stedelijke Bevolking (%)': 'SP.URB.TOTL.IN.ZS',
            'Handelsbalans (% van BBP)': 'NE.TRD.GNFS.ZS',
            'High-tech Export (% van Totale Export)': 'TX.VAL.TECH.MF.ZS',
            'Netto Migratie': 'SM.POP.NETM',
            'Werkgelegenheid in Landbouw (% van Totale Werkgelegenheid)': 'SL.AGR.EMPL.ZS',
            'Werkgelegenheid in Industrie (% van Totale Werkgelegenheid)': 'SL.IND.EMPL.ZS',
            'Werkgelegenheid in Diensten (% van Totale Werkgelegenheid)': 'SL.SRV.EMPL.ZS',
            'Buitenlandse Directe Investeringen (% van BBP)': 'BX.KLT.DINV.WD.GD.ZS',
            'Totale Reserves (inclusief Goud, Huidige US$)': 'FI.RES.TOTL.CD',
            'CO2 Uitstoot (ton per capita)': 'EN.ATM.CO2E.PC',
            'Oppervlakte (km²)': 'AG.SRF.TOTL.K2',
            'Moedersterfte (per 100.000 geboorten)': 'SH.STA.MMRT',
            'Kindersterfte <5 (per 1000)': 'SH.DTH.MORT',
            'Bevolkingsgroei (%)': 'SP.POP.GROW',
            'Bruto Nationaal Inkomen per Hoofd': 'NY.GNP.PCAP.CD',
            'BBP Groei (%)': 'NY.GDP.MKTP.KD.ZG',
            'Export van Goederen en Diensten (% van BBP)': 'NE.EXP.GNFS.ZS',
            'Import van Goederen en Diensten (% van BBP)': 'NE.IMP.GNFS.ZS',
            'BBP Deflator Inflatie (%)': 'NY.GDP.DEFL.KD.ZG',
        }

        data = {}
        for name, code in indicators.items():
            data[name] = wb.get_series(code, id_or_value='id', simplify_index=True, mrv=1)

        df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']

        for name, series in data.items():
            df[name] = series

        country_data = df[df['country'].str.lower() == country_name.lower()]

        if not country_data.empty:
            return country_data
        else:
            return None

    def format_value(self, indicator, value):
        if pd.isna(value):
            return "N/A"

        if indicator in ['BBP (totaal)', 'BBP per Hoofd van de Bevolking']:
            return f"€{value:,.2f}"
        elif indicator in ['Bevolking']:
            return f"{value:,.0f}"
        elif indicator in ['Inflatie (CPI)',
                           'Werkloosheid',
                           'Overheidsuitgaven aan Onderwijs (% van BBP)',
                           'Stedelijke Bevolking (%)',
                           'Handelsbalans (% van BBP)',
                           'High-tech Export (% van Totale Export)',
                           'Werkgelegenheid in Landbouw (% van Totale Werkgelegenheid)',
                           'Werkgelegenheid in Industrie (% van Totale Werkgelegenheid)',
                           'Werkgelegenheid in Diensten (% van Totale Werkgelegenheid)',
                           'Buitenlandse Directe Investeringen (% van BBP)']:
            return f"{value:.2f}%"
        elif indicator == 'Levensverwachting':
            return f"{value:.2f} jaar"
        else:
            return str(value)


class MinisterieVanDefensieApp(QWidget):
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
        main_layout.addLayout(left_layout)
        self.setLayout(main_layout)

    def update_data(self):
        country_name = self.input_field.text()
        self.country_label.setText(f"Gekozen land: {country_name}")
        indicators = [
            ("Militaire Uitgaven (% van BBP)", "MS.MIL.XPND.GD.ZS"),
            ("Aantal Militairen (per 1000 inwoners)", "MS.MIL.TOTL.P1"),
            ("Wapens Import (miljoen US$)", "MS.MIL.MPRT.KD"),
        ]
        data = self.get_defense_data(country_name, indicators)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(indicators))
        self.table.setHorizontalHeaderLabels(['Indicator', 'Waarde'])
        for i, (label, _) in enumerate(indicators):
            indicator_item = QTableWidgetItem(label)
            indicator_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, indicator_item)
            value_item = QTableWidgetItem(data.get(label, "N/A"))
            value_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, value_item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setStretchLastSection(False)

    def get_defense_data(self, country_name, indicators):
        try:
            import world_bank_data as wb
            countries = wb.get_countries()
            df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
            data = {}
            for label, code in indicators:
                series = wb.get_series(code, id_or_value='id', simplify_index=True, mrv=1)
                df[label] = series
            country_data = df[df['country'].str.lower() == country_name.lower()]
            for label, _ in indicators:
                if not country_data.empty:
                    value = country_data.iloc[0][label]
                    data[label] = f"{value:.2f}" if not pd.isna(value) else "N/A"
                else:
                    data[label] = "N/A"
            return data
        except Exception:
            return {label: "N/A" for label, _ in indicators}


class MinisterieVanLandbouwApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ministerie van Landbouw')
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
        main_layout.addLayout(left_layout)
        self.setLayout(main_layout)

    def update_data(self):
        country_name = self.input_field.text()
        self.country_label.setText(f"Gekozen land: {country_name}")
        indicators = [
            ("Landbouw Productie Index", "AG.PRD.FOOD.XD"),
            ("Landbouw (% van BBP)", "NV.AGR.TOTL.ZS"),
            ("Werkgelegenheid in Landbouw (% van Totale Werkgelegenheid)", "SL.AGR.EMPL.ZS"),
        ]
        data = self.get_agriculture_data(country_name, indicators)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(indicators))
        self.table.setHorizontalHeaderLabels(['Indicator', 'Waarde'])
        for i, (label, _) in enumerate(indicators):
            indicator_item = QTableWidgetItem(label)
            indicator_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, indicator_item)
            value_item = QTableWidgetItem(data.get(label, "N/A"))
            value_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, value_item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setStretchLastSection(False)

    def get_agriculture_data(self, country_name, indicators):
        try:
            import world_bank_data as wb
            countries = wb.get_countries()
            df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
            data = {}
            for label, code in indicators:
                series = wb.get_series(code, id_or_value='id', simplify_index=True, mrv=1)
                df[label] = series
            country_data = df[df['country'].str.lower() == country_name.lower()]
            for label, _ in indicators:
                if not country_data.empty:
                    value = country_data.iloc[0][label]
                    data[label] = f"{value:.2f}" if not pd.isna(value) else "N/A"
                else:
                    data[label] = "N/A"
            return data
        except Exception:
            return {label: "N/A" for label, _ in indicators}


class MinisterieVanHuisvestingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ministerie van Huisvesting')
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
        main_layout.addLayout(left_layout)
        self.setLayout(main_layout)

    def update_data(self):
        country_name = self.input_field.text()
        self.country_label.setText(f"Gekozen land: {country_name}")
        indicators = [
            ("Stedelijke Bevolking (% van Totale Bevolking)", "SP.URB.TOTL.IN.ZS"),
            ("Aantal Woningen per 1000 inwoners", None),
            ("Gemiddelde Huishoudgrootte", None),
        ]
        data = self.get_housing_data(country_name, indicators)
        self.table.setColumnCount(2)
        self.table.setRowCount(len(indicators))
        self.table.setHorizontalHeaderLabels(['Indicator', 'Waarde'])
        for i, (label, _) in enumerate(indicators):
            indicator_item = QTableWidgetItem(label)
            indicator_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, indicator_item)
            value_item = QTableWidgetItem(data.get(label, "N/A"))
            value_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, value_item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setStretchLastSection(False)

    def get_housing_data(self, country_name, indicators):
        try:
            import world_bank_data as wb
            countries = wb.get_countries()
            df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
            data = {}
            for label, code in indicators:
                if code:
                    series = wb.get_series(code, id_or_value='id', simplify_index=True, mrv=1)
                    df[label] = series
            country_data = df[df['country'].str.lower() == country_name.lower()]
            for label, code in indicators:
                if code and not country_data.empty:
                    value = country_data.iloc[0][label]
                    data[label] = f"{value:.2f}" if not pd.isna(value) else "N/A"
                elif not code:
                    data[label] = "N/A"  # Placeholder for unavailable data
                else:
                    data[label] = "N/A"
            return data
        except Exception:
            return {label: "N/A" for label, _ in indicators}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MinisterieVanEconomischeZakenApp()
    main_app.show()
    sys.exit(app.exec_())