import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QColor
from Country_Info import CountryInfoApp  # Zorg ervoor dat je deze klasse hebt gedefinieerd
from Sunplot_GDP import WereldGDPApp  # Zorg ervoor dat je deze klasse hebt gedefinieerd
from Sunplot_wereldpopulatie import WereldPopulatieApp  # Importeer de WereldPopulatieApp klasse
from Ministerie_Van_Economische_Zaken import MinisterieVanEconomischeZakenApp  # Zorg ervoor dat je deze klasse hebt gedefinieerd
from muziek import MuziekSpeler  # Zorg ervoor dat je deze klasse hebt gedefinieerd

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Epic Game!")

        # Pas de achtergrond aan met een houttextuur
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("Backgrounds/20.jpg")))
        self.setPalette(palette)

        # Hoofdwidget en lay-out
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Tab-widget om de verschillende apps in tabs te plaatsen
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Voeg de verschillende applicaties toe als tabbladen
        country_info_app = CountryInfoApp()
        tab_widget.addTab(country_info_app, "Country Info")

        ministerie_economische_zaken_app = MinisterieVanEconomischeZakenApp()
        tab_widget.addTab(ministerie_economische_zaken_app, "Economische Zaken")

        wereld_gdp_app = WereldGDPApp()
        tab_widget.addTab(wereld_gdp_app, "Wereld GDP")

        wereld_populatie_app = WereldPopulatieApp()
        tab_widget.addTab(wereld_populatie_app, "Wereld Populatie")

        # Voeg de MuziekSpeler toe als een tab
        muziek_speler = MuziekSpeler()

        # Verwijder de afbeelding en stel een effen zwarte achtergrond in voor MuziekSpeler
        muziek_speler_palette = QPalette()
        muziek_speler_palette.setColor(QPalette.Window, QColor("black"))
        muziek_speler.setPalette(muziek_speler_palette)
        muziek_speler.setAutoFillBackground(True)

        tab_widget.addTab(muziek_speler, "Muziek Speler")

        # Pas de stijl van de tabs aan
        self.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid lightgray; 
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #f9f9f9; /* Zachte lichte kleur */
                color: black;
                padding: 10px;
                border: 1px solid lightgray;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:selected { 
                background: #ccff00; /* Fluorescerend geel voor geselecteerde tab */
                color: black;
            }
            QTabBar::tab:hover {
                background: #cccccc; /* Donkere grijs voor hover */
            }
        """)

        self.resize(800, 600)  # Pas de grootte van het venster aan

def main():
    app = QApplication(sys.argv)

    # Start de MainApp
    main_app = MainApp()
    main_app.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()