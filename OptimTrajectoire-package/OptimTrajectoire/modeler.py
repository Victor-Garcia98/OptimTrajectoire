"""
Module de modélisation des trajectoires aériennes sous forme de graphe.
"""

import networkx as nx

class TrajectoryModeler:
    """
    Crée un graphe représentant les trajets aériens en fonction de la consommation de carburant.
    """
    def __init__(self, flight_data, airport_coords, aircraft):
        self.flight_data = flight_data
        self.airport_coords = airport_coords
        self.graph = nx.Graph()
        self.aircraft = aircraft

    def build_graph(self):
        """
        Construit le graphe des trajets possibles entre aéroports selon les limitations de carburant.
        """
        fuel_per_mile = self.aircraft.get_consumption_per_mile()
        max_fuel_allowed = 0.95 * self.aircraft.models[self.aircraft.selected_model]['max_fuel_per_flight']
        takeoff_penalty = 300  # kg

        for _, row in self.flight_data.iterrows():
            origin = row['ORIGIN']
            dest = row['DEST']
            distance = row['DISTANCE IN MILES']
            if origin in self.airport_coords and dest in self.airport_coords:
                fuel_consumption = fuel_per_mile * distance + takeoff_penalty
                if fuel_consumption > max_fuel_allowed:
                    continue
                speed_mph = self.aircraft.models[self.aircraft.selected_model]['cruise_speed_kts'] * 1.15078
                flight_time = distance / speed_mph
                self.graph.add_node(origin, pos=self.airport_coords[origin])
                self.graph.add_node(dest, pos=self.airport_coords[dest])
                self.graph.add_edge(origin, dest, weight=fuel_consumption, time=flight_time)

    def get_graph(self):
        """
        Renvoie le graphe construit des aéroports et trajets valides.

        Returns
        -------
        networkx.Graph
            Graphe des trajets valides avec poids en carburant et temps.
        """
        return self.graph
