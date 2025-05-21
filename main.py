import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QColor
from Country_Info import CountryInfoApp
from Sunplot_GDP import WereldGDPApp
from Sunplot_wereldpopulatie import WereldPopulatieApp
from Ministerie_Van_Economische_Zaken import MinisterieVanEconomischeZakenApp
from Ministerie_Van_Leger import MinisterieVanLegerApp
from Ministerie_Van_Landbouw import MinisterieVanLandbouwApp
from Ministerie_Van_Huisvesting import MinisterieVanHuisvestingApp
from Country_Ministries import CountryMinistries
from muziek import MuziekSpeler

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

        # Tab voor het kiezen van een land
        from Country_Selector import CountrySelector
        country_selector = CountrySelector()
        tab_widget.addTab(country_selector, "Kies Land")

        country_ministries = CountryMinistries()
        tab_widget.addTab(country_ministries, "Ministeries")

        ministerie_economische_zaken_app = MinisterieVanEconomischeZakenApp()
        tab_widget.addTab(ministerie_economische_zaken_app, "Economische Zaken")

        ministerie_leger_app = MinisterieVanLegerApp()
        tab_widget.addTab(ministerie_leger_app, "Leger")

        ministerie_landbouw_app = MinisterieVanLandbouwApp()
        tab_widget.addTab(ministerie_landbouw_app, "Landbouw")

        ministerie_huisvesting_app = MinisterieVanHuisvestingApp()
        tab_widget.addTab(ministerie_huisvesting_app, "Huisvesting")

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
