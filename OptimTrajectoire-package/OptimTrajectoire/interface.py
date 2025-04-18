"""
Interface utilisateur pour charger les données, choisir les paramètres et lancer les calculs.
"""
from .aircraft import Aircraft
from .loader import DataLoader
from .modeler import TrajectoryModeler
from .optimizer import TrajectoryOptimizer
from .visualizer import TrajectoryVisualizer
import os
from pathlib import Path

class UserInterface:
    """
    Interface en ligne de commande permettant d'exécuter le simulateur de trajectoires aériennes.
    """
    def __init__(self):
        self.data_loader = DataLoader()
        self.flight_data = None
        self.airport_coords = None
        self.trajectory_modeler = None
        self.airports = []

    def load_data(self):
        """
        Charge les données de vol et initialise la liste des aéroports.
        """
        file_path = Path(__file__).parent / "data" / "Distance_airports.csv"
        self.flight_data = self.data_loader.load_flight_data(file_path)
        self.airport_coords = self.data_loader.airport_coords
        self._init_airports()

    def _init_airports(self):
        """
        Initialise la liste des aéroports disponibles dans les données.
        """
        valid_airports = set(self.airport_coords.keys())
        departures = set(self.flight_data['ORIGIN']) & valid_airports
        arrivals = set(self.flight_data['DEST']) & valid_airports
        self.airports = sorted(list(departures | arrivals))

    def select_airports(self):
        """
        Permet à l'utilisateur de sélectionner un aéroport de départ et d'arrivée.

        :return: Le code IATA de l'aéroport de départ et d'arrivée.
        :rtype:  tuple[str, str]

        """
        print("\n" + "=" * 40)
        print("\nAÉROPORTS DISPONIBLES:")
        print(", ".join(self.airports))
        print("=" * 40 + "\n")
        while True:
            start = input("Aéroport de départ: ").strip().upper()
            if start in self.airports:
                break
            print(f"Erreur: {start} n'existe pas dans la base de données\n")
        while True:
            end = input("Aéroport d'arrivée: ").strip().upper()
            if end in self.airports and end != start:
                break
            print("L'aéroport d'arrivée doit être différent du départ!")
        return start, end

    def run(self):
        """
        Lance le processus complet : chargement, sélection, modélisation, optimisation et visualisation.
        """
        self.load_data()
        aircraft = Aircraft()
        aircraft.select_model()
        self.trajectory_modeler = TrajectoryModeler(self.flight_data, self.airport_coords, aircraft)
        self.trajectory_modeler.build_graph()
        while True:
            start, end = self.select_airports()
            try:
                optimizer = TrajectoryOptimizer(self.trajectory_modeler.get_graph())
                path, cost, duration = optimizer.optimize_trajectory(start, end)
                print("\n" + "=" * 40)
                print(f"TRAJET OPTIMAL: {' → '.join(path)}")
                print(f"CONSOMMATION TOTALE: {cost:.2f} kg de carburant")
                print(f"DUREE TOTALE DU CHEMIN: {duration:.2f} heures")
                print("=" * 40 + "\n")
                m = TrajectoryVisualizer(self.trajectory_modeler.get_graph(), path).plot_trajectory()
                m.save("map.html")
                map_path = os.path.abspath("map.html")
                print(f"Carte enregistrée sous 'map.html'. Ouvrez-la ici : file://{map_path}")
            except ValueError as e:
                print(f"\nErreur: {str(e)}\n")
            if input("Voulez-vous faire une autre recherche? (o/n) ").lower() != 'o':
                break