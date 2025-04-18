"""
Module de chargement des données de vol et des coordonnées d'aéroports.
"""

import pandas as pd

class DataLoader:
    """
    Charge les données de vols et les coordonnées des aéroports.
    """
    def __init__(self):
        self.airport_coords = None

    def load_flight_data(self, file_path):
        """
        Charge les données de vols depuis un fichier CSV et les coordonnées depuis une source en ligne.

        :param: file_path : Chemin du fichier CSV contenant les données de vol.
        :type: file_path : str

        :return: Les données de vol chargées.
        :rtype: DataFrame

        """
        flight_data = pd.read_csv(file_path)
        airports = pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat",
                               header=None,
                               names=['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO',
                                      'Lat', 'Lon', 'Alt', 'Timezone', 'DST', 'Tz',
                                      'Type', 'Source'])
        self.airport_coords = dict(zip(airports['IATA'], zip(airports['Lat'], airports['Lon'])))
        return flight_data

