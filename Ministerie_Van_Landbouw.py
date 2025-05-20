import sys
import pandas as pd
from Ministerie_Base import MinisterieBaseApp
from PyQt5.QtWidgets import QApplication


class MinisterieVanLandbouwApp(MinisterieBaseApp):
    def __init__(self):
        super().__init__(
            'Ministerie van Landbouw',
            'Dit is uw huidige minister van landbouw'
        )

    def get_indicator_codes(self) -> dict:
        return {
            'Landbouwgrond (km²)': 'AG.LND.AGRI.K2',
            'Landbouw, Bosbouw en Visserij (% van BBP)': 'NV.AGR.TOTL.ZS',
            'Werkgelegenheid in Landbouw (% van Totale Werkgelegenheid)': 'SL.AGR.EMPL.ZS'
        }

    def format_value(self, indicator: str, value) -> str:
        if pd.isna(value):
            return "N/A"
        if '(%' in indicator:
            return f"{value:.2f}%"
        elif 'km²' in indicator:
            return f"{value:,.0f}"
        else:
            return f"{value:,.2f}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MinisterieVanLandbouwApp()
    main_app.show()
    sys.exit(app.exec_())
