"""
Module d'optimisation de trajectoires entre aéroports.
"""

import networkx as nx

class TrajectoryOptimizer:
    """
    Trouve la trajectoire optimale (minimisant le carburant) entre deux aéroports.
    """
    def __init__(self, graph):
        self.graph = graph

    def optimize_trajectory(self, start, end):
        """
        Calcule le plus court chemin en carburant entre deux aéroports.

        :param: start: Code IATA de l'aéroport de départ.
        :type: start: str

        :param: end: Code IATA de l'aéroport d'arrivée.
        :type: end: str

        :return: Chemin optimal, consommation totale, durée totale.
        :rtype: tuple[list[str], float, float]

        :raises: Erreur Si aucun chemin n'existe entre les deux aéroports.

        """
        try:
            path = nx.dijkstra_path(self.graph, start, end, weight='weight')
            cost = nx.dijkstra_path_length(self.graph, start, end, weight='weight')
            duration = sum(self.graph[u][v]['time'] for u, v in zip(path[:-1], path[1:]))
            return path, cost, duration
        except nx.NetworkXNoPath:
            raise ValueError(f"Aucun chemin trouvé entre {start} et {end}")
