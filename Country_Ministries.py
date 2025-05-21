from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget
from Country_names import CountryMap
import global_state
from Ministerie_Van_Leger import MinisterieVanLegerApp
from Ministerie_Van_Huisvesting import MinisterieVanHuisvestingApp
from Ministerie_Van_Landbouw import MinisterieVanLandbouwApp
from Ministerie_Van_Economische_Zaken import MinisterieVanEconomischeZakenApp

class CountryMinistries(QWidget):
    def __init__(self):
        super().__init__()
        self.country_map = CountryMap()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText('Voer een landnaam in')
        input_layout.addWidget(self.input_field)
        self.load_button = QPushButton('Laad Data', self)
        self.load_button.clicked.connect(self.load_country)
        input_layout.addWidget(self.load_button)
        layout.addLayout(input_layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.military_tab = MinisterieVanLegerApp()
        self.social_tab = MinisterieVanHuisvestingApp()
        self.housing_tab = MinisterieVanHuisvestingApp()
        self.agri_tab = MinisterieVanLandbouwApp()
        self.trade_tab = MinisterieVanEconomischeZakenApp()

        self.tabs.addTab(self.military_tab, 'Military')
        self.tabs.addTab(self.social_tab, 'Social Security')
        self.tabs.addTab(self.housing_tab, 'Housing')
        self.tabs.addTab(self.agri_tab, 'Agriculture')
        self.tabs.addTab(self.trade_tab, 'Trade')

    def load_country(self):
        country_dutch = self.input_field.text()
        country_english = self.country_map.get_country_name(country_dutch)
        global_state.translated_country_name = country_english
        for tab in [self.military_tab, self.social_tab, self.housing_tab, self.agri_tab, self.trade_tab]:
            if hasattr(tab, 'update_data'):
                tab.update_data()
