import sys
import pandas as pd
import plotly
import plotly.offline as offline
import world_bank_data as wb
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os


def version_to_int_list(version):
    return [int(s) for s in version.split('.')]


assert version_to_int_list(plotly.__version__) >= version_to_int_list('3.8.0'), 'Sunburst plots require Plotly >= 3.8.0'


class WereldPopulatieApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.generate_population_plot()

    def initUI(self):
        self.setWindowTitle('Wereldpopulatie 2023')
        self.setGeometry(100, 100, 800, 600)

        # Gebruik QVBoxLayout om de QWebEngineView widget toe te voegen
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def generate_population_plot(self):
        pd.set_option('display.max_rows', 12)

        # Haal landen en regio's op
        countries = wb.get_countries()

        # Population dataset, by the World Bank (most recent value)
        population = wb.get_series('SP.POP.TOTL', mrv=1)

        # Zelfde dataset, geïndexeerd met de landcode
        population = wb.get_series('SP.POP.TOTL', id_or_value='id', simplify_index=True, mrv=1)

        # Aggregaat regio, land en bevolking
        df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
        df['population'] = population

        # Sunburst plot voorbereiden
        columns = ['parents', 'labels', 'values']

        level1 = df.copy()
        level1.columns = columns
        level1['text'] = level1['values'].apply(lambda pop: '{:,.0f}'.format(pop))

        level2 = df.groupby('region').population.sum().reset_index()[['region', 'region', 'population']]
        level2.columns = columns
        level2['parents'] = 'World'
        level2['text'] = level2['values'].apply(lambda pop: '{:,.0f}'.format(pop))
        level2['values'] = 0

        level3 = pd.DataFrame({'parents': [''], 'labels': ['World'],
                               'values': [0.0], 'text': ['{:,.0f}'.format(population.loc['WLD'])]})

        all_levels = pd.concat([level1, level2, level3], axis=0).reset_index(drop=True)

        # Plot de wereldbevolking
        fig = dict(
            data=[dict(type='sunburst', hoverinfo='text', **all_levels)],
            layout=dict(title='Klik op een regio om te zoemen',
                        width=1200, height=1200)
        )

        # Sla de plot op als een HTML-bestand
        offline.plot(fig, filename='world_population_sunburst.html', auto_open=False)

        # Laad de HTML in de QWebEngineView widget
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath('world_population_sunburst.html')))
