import sys
import pandas as pd
from Ministerie_Base import MinisterieBaseApp
from PyQt5.QtWidgets import QApplication


class MinisterieVanLegerApp(MinisterieBaseApp):
    def __init__(self):
        super().__init__(
            'Ministerie van Defensie',
            'Dit is uw huidige minister van defensie'
        )

    def get_indicator_codes(self) -> dict:
        return {
            'Militaire Uitgaven (US$)': 'MS.MIL.XPND.CD',
            'Militaire Uitgaven (% van BBP)': 'MS.MIL.XPND.GD.ZS',
            'Personeel in de Strijdkrachten': 'MS.MIL.TOTL.P1'
        }

    def format_value(self, indicator: str, value) -> str:
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
