import os
import webbrowser
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from countryinfo import CountryInfo
from geopy.geocoders import Nominatim
import folium
from Country_names import CountryMap  # Importeer de nieuwe CountryMap class

class CountryInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.country_map = CountryMap()  # Instantieer de CountryMap class
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Landeninformatie')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.flagLabel = QLabel(self)
        layout.addWidget(self.flagLabel)

        self.countryInput = QLineEdit(self)
        self.countryInput.setPlaceholderText('Voer een landnaam in...')
        layout.addWidget(self.countryInput)

        self.getInfoButton = QPushButton('Haal informatie over het land op', self)
        self.getInfoButton.clicked.connect(self.getCountryInfo)
        layout.addWidget(self.getInfoButton)

        self.infoDisplay = QTextEdit(self)
        self.infoDisplay.setReadOnly(True)
        layout.addWidget(self.infoDisplay)

    def getCountryInfo(self):
        try:
            # Haal de Engelse landnaam op via de nieuwe methode
            countryName = self.get_translated_country_name()
            country = CountryInfo(countryName)

            data = {
                'Officiële Naam': self.get_data(country, 'alt_spellings', index=1),
                'Hoofdstad': self.get_data(country, 'capital'),
                'Regio': self.get_data(country, 'region'),
                'Subregio': self.get_data(country, 'subregion'),
                'Provincies': self.get_data(country, 'provinces', is_list=True),
                'Grenzen': self.get_borders(country),
                'Bevolking': self.get_data(country, 'population'),
                'Oppervlakte (km²)': self.get_data(country, 'area'),
                'Valuta': self.get_data(country, 'currencies', is_list=True),
                'Tijdzones': self.get_data(country, 'timezones', is_list=True),
                'Wikipedia Link': self.get_data(country, 'wiki'),
                'Landnummers': self.get_data(country, 'calling_codes', is_list=True),
                'Internet Top Level Domein': self.get_data(country, 'tld', is_list=True),
                'Inheemse Naam': self.get_data(country, 'native_name'),
                'Demonym': self.get_data(country, 'demonym'),
            }

            available_data = {k: v for k, v in data.items() if v != 'N/A'}
            unavailable_data = {k: v for k, v in data.items() if v == 'N/A'}

            self.infoDisplay.clear()
            for key, value in available_data.items():
                self.infoDisplay.append(f"{key}: {value}")

            if unavailable_data:
                self.infoDisplay.append("\nNiet Beschikbare Informatie:")
                for key, value in unavailable_data.items():
                    self.infoDisplay.append(f"{key}: {value}")

            # Toon de vlag
            self.showFlag(countryName)

            # Kaart genereren
            self.showMap(countryName)

        except Exception as e:
            countryNameDutch = self.countryInput.text()
            self.infoDisplay.setText(f"Fout bij het ophalen van informatie voor {countryNameDutch}: {str(e)}")

    def get_translated_country_name(self):
        countryNameDutch = self.countryInput.text()
        return self.country_map.get_country_name(countryNameDutch)

    def get_data(self, country, attribute, is_list=False, index=None):
        try:
            result = getattr(country, attribute)()
            if is_list and result:
                return ', '.join(result)
            if index is not None and result and len(result) > index:
                return result[index]
            return result if result else 'N/A'
        except:
            return 'N/A'

    def get_borders(self, country):
        try:
            borders = country.borders()
            if borders:
                return ', '.join([self.fullCountryName(border) for border in borders])
            return 'N/A'
        except:
            return 'N/A'

    def get_languages(self, country):
        try:
            languages = country.languages()
            if languages:
                return ', '.join(languages.values())
            return 'N/A'
        except:
            return 'N/A'

    def fullCountryName(self, code):
        country_codes = {
            'AFG': 'Afghanistan', 'BGD': 'Bangladesh', 'BTN': 'Bhutan', 'MMR': 'Myanmar (Burma)',
            'CHN': 'China', 'NPL': 'Nepal', 'PAK': 'Pakistan', 'LKA': 'Sri Lanka', 'INR': 'Indian Rupee',
            # Voeg meer codes en namen toe zoals nodig
        }
        return country_codes.get(code, code)

    def showFlag(self, country_name):
        try:
            response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
            if response.status_code == 200:
                country_data = response.json()[0]
                flag_url = country_data['flags']['png']

                # Toon de vlag
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(flag_url).content)
                self.flagLabel.setPixmap(pixmap)
                self.flagLabel.setAlignment(Qt.AlignCenter)
            else:
                self.flagLabel.setText("Vlag niet gevonden.")
        except Exception as e:
            self.flagLabel.setText(f"Fout bij het ophalen van de vlag: {str(e)}")

    def showMap(self, country_name):
        try:
            # Maak de map "mappen" aan als deze niet bestaat
            if not os.path.exists("mappen"):
                os.makedirs("mappen")

            # Stel de bestandsnaam in voor de kaart binnen de "mappen"-submap
            map_file = os.path.join("mappen", f"{country_name}_kaart.html")

            # Controleer of het bestand al bestaat
            if os.path.exists(map_file):
                # Als het bestand bestaat, open het in de webbrowser
                self.infoDisplay.append(f"Kaart bestaat al, openen {map_file}.")
                webbrowser.open(f"file://{os.path.realpath(map_file)}")
            else:
                # Als het bestand niet bestaat, genereer de kaart
                geolocator = Nominatim(user_agent="countryinfo_app")
                location = geolocator.geocode(country_name)

                if location:
                    # Maak een folium kaart
                    country_map = folium.Map(location=[location.latitude, location.longitude], zoom_start=6)
                    folium.Marker([location.latitude, location.longitude], popup=country_name).add_to(country_map)

                    # Sla de kaart op als HTML-bestand
                    country_map.save(map_file)

                    # Open de kaart in een webbrowser
                    self.infoDisplay.append(f"Kaart gegenereerd en opgeslagen als {map_file}.")
                    webbrowser.open(f"file://{os.path.realpath(map_file)}")
                else:
                    self.infoDisplay.append(f"\nKon locatie voor {country_name} niet vinden.")
        except Exception as e:
            self.infoDisplay.append(f"\nFout bij het weergeven van de kaart: {str(e)}")

