import sys
import pandas as pd
from Ministerie_Base import MinisterieBaseApp
from PyQt5.QtWidgets import QApplication


class MinisterieVanHuisvestingApp(MinisterieBaseApp):
    def __init__(self):
        super().__init__(
            'Ministerie van Huisvesting',
            'Dit is uw huidige minister van huisvesting'
        )

    def get_indicator_codes(self) -> dict:
        return {
            'Bevolkingsdichtheid (per km²)': 'EN.POP.DNST',
            'Stedelijke Bevolking (%)': 'SP.URB.TOTL.IN.ZS',
            'Bevolking in Sloppenwijken (%)': 'EN.POP.SLUM.UR.ZS'
        }

    def format_value(self, indicator: str, value) -> str:
        if pd.isna(value):
            return "N/A"
        if '(%' in indicator:
            return f"{value:.2f}%"
        else:
            return f"{value:,.2f}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MinisterieVanHuisvestingApp()
    main_app.show()
    sys.exit(app.exec_())
