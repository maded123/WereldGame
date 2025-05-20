import sys
import pandas as pd
from Ministerie_Base import MinisterieBaseApp
from PyQt5.QtWidgets import QApplication


class MinisterieVanEconomischeZakenApp(MinisterieBaseApp):
    def __init__(self):
        super().__init__(
            'Ministerie van Economische Zaken',
            'Dit is uw huidige minister van financiën'
        )

    def get_indicator_codes(self) -> dict:
        return {
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
            'Totale Reserves (inclusief Goud, Huidige US$)': 'FI.RES.TOTL.CD'
        }

    def format_value(self, indicator: str, value) -> str:
        if pd.isna(value):
            return "N/A"
        if indicator in ['BBP (totaal)', 'BBP per Hoofd van de Bevolking']:
            return f"€{value:,.2f}"
        elif indicator == 'Bevolking':
            return f"{value:,.0f}"
        elif indicator in [
            'Inflatie (CPI)', 'Werkloosheid', 'Stedelijke Bevolking (%)',
            'Handelsbalans (% van BBP)', 'High-tech Export (% van Totale Export)',
            'Werkgelegenheid in Landbouw (% van Totale Werkgelegenheid)',
            'Werkgelegenheid in Industrie (% van Totale Werkgelegenheid)',
            'Werkgelegenheid in Diensten (% van Totale Werkgelegenheid)',
            'Buitenlandse Directe Investeringen (% van BBP)'
        ]:
            return f"{value:.2f}%"
        elif indicator == 'Levensverwachting':
            return f"{value:.2f} jaar"
        else:
            return str(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MinisterieVanEconomischeZakenApp()
    main_app.show()
    sys.exit(app.exec_())
