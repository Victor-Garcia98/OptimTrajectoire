import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class DataLoader:
    def __init__(self):
        pass

    def load_flight_data(self, file_path):
        return pd.read_csv(file_path)


class TrajectoryModeler:
    def __init__(self, flight_data):
        self.flight_data = flight_data
        self.graph = nx.Graph()

    def build_graph(self):
        for _, row in self.flight_data.iterrows():
            departure = row['airport_departure']
            arrival = row['airport_arrival']
            fuel_consumption = row['fuel_consumption']
            self.graph.add_edge(departure, arrival, weight=fuel_consumption)

    def get_graph(self):
        return self.graph


class TrajectoryOptimizer:
    def __init__(self, graph):
        self.graph = graph

    def optimize_trajectory(self, start, end, objective="min_fuel"):
        if objective == "min_fuel":
            path = nx.dijkstra_path(self.graph, start, end, weight='weight')
            cost = nx.dijkstra_path_length(self.graph, start, end, weight='weight')
            return path, cost
        else:
            raise ValueError("Objectif non supporté. Utilisez 'min_fuel'.")


class TrajectoryVisualizer:
    def __init__(self, graph, path=None):
        self.graph = graph
        self.path = path

    def plot_trajectory(self):
        pos = nx.spring_layout(self.graph)
        plt.figure(figsize=(10, 8))

        # Dessin du graphe complet
        nx.draw_networkx_nodes(self.graph, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_edges(self.graph, pos, edge_color='gray')
        nx.draw_networkx_labels(self.graph, pos)

        # Mise en évidence du chemin optimal
        if self.path:
            path_edges = list(zip(self.path[:-1], self.path[1:]))
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges,
                                   edge_color='red', width=2)
            nx.draw_networkx_nodes(self.graph, pos, nodelist=self.path,
                                   node_color='red', node_size=700)

        plt.title("Trajectoire de Vol Optimale")
        plt.show()


class UserInterface:
    def __init__(self):
        self.data_loader = DataLoader()
        self.flight_data = None
        self.trajectory_modeler = None
        self.trajectory_optimizer = None
        self.trajectory_visualizer = None

    def load_data(self):
        self.flight_data = self.data_loader.load_flight_data("flight_data.csv")


    def model_trajectories(self):
        self.trajectory_modeler = TrajectoryModeler(self.flight_data)
        self.trajectory_modeler.build_graph()

    def optimize_trajectory(self, start, end):
        graph = self.trajectory_modeler.get_graph()
        self.trajectory_optimizer = TrajectoryOptimizer(graph)
        path, cost = self.trajectory_optimizer.optimize_trajectory(start, end)
        print(f"Trajectoire optimale : {path}")
        print(f"Coût total (carburant) : {cost}")
        return path

    def visualize_trajectory(self, path):
        graph = self.trajectory_modeler.get_graph()
        self.trajectory_visualizer = TrajectoryVisualizer(graph, path)
        self.trajectory_visualizer.plot_trajectory()


# Exécution du programme
if __name__ == "__main__":
    ui = UserInterface()
    ui.load_data()
    ui.model_trajectories()

    start_airport = "JFK"
    end_airport = "LAX"

    optimal_path = ui.optimize_trajectory(start_airport, end_airport)
    ui.visualize_trajectory(optimal_path)