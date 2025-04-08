import pandas as pd
import networkx as nx
import folium


class DataLoader:
    def __init__(self):
        self.airport_coords = None

    def load_flight_data(self, file_path):
        flight_data = pd.read_csv(file_path)
        airports = pd.read_csv("https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat",
                               header=None,
                               names=['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO',
                                      'Lat', 'Lon', 'Alt', 'Timezone', 'DST', 'Tz',
                                      'Type', 'Source'])
        self.airport_coords = dict(zip(airports['IATA'], zip(airports['Lat'], airports['Lon'])))
        return flight_data


class Aircraft:
    def __init__(self):
        self.models = {
            'A320': {'fuel_burn_kgph': 2406, 'cruise_speed_kts': 447, 'max_fuel_per_flight' : 24456.33},
            'B777': {'fuel_burn_kgph': 6834, 'cruise_speed_kts': 488, 'max_fuel_per_flight' : 145538},
            'CRJ9': {'fuel_burn_kgph': 1476, 'cruise_speed_kts': 447, 'max_fuel_per_flight' : 8888},
            'C56X': {'fuel_burn_kgph': 558, 'cruise_speed_kts': 430, 'max_fuel_per_flight' : 3057.213},
        }
        self.selected_model = None

    def select_model(self):
        print("Modèles d'avions disponibles :")
        for model in self.models:
            print(f"- {model}")
        while True:
            model = input("Choisissez un modèle d'avion : ").strip().upper()
            if model in self.models:
                self.selected_model = model
                break
            print("Modèle invalide. Essayez encore.")
        return self.models[model]

    def get_consumption_per_mile(self):
        if self.selected_model is None:
            raise ValueError("Aucun modèle sélectionné.")
        data = self.models[self.selected_model]
        speed_knots = data['cruise_speed_kts']
        fuel_burn_kgph = data['fuel_burn_kgph']
        speed_mph = speed_knots * 1.15078  # conversion knots → miles/h
        return fuel_burn_kgph / speed_mph  # kg/mile


class TrajectoryModeler:
    def __init__(self, flight_data, airport_coords, aircraft):
        self.flight_data = flight_data
        self.airport_coords = airport_coords
        self.graph = nx.Graph()
        self.aircraft = aircraft

    def build_graph(self):
        fuel_per_mile = self.aircraft.get_consumption_per_mile()
        max_fuel_allowed =0.95 * self.aircraft.models[self.aircraft.selected_model]['max_fuel_per_flight']
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
        return self.graph


class TrajectoryVisualizer:
    def __init__(self, graph, path=None):
        self.graph = graph
        self.path = path

    def plot_trajectory(self):
        airport_positions = [self.graph.nodes[node]['pos'] for node in self.graph.nodes()] # centrer la carte
        avg_lat = sum(lat for lat, lon in airport_positions) / len(airport_positions)
        avg_lon = sum(lon for lat, lon in airport_positions) / len(airport_positions)

        min_lon, max_lon = -180, 180
        min_lat, max_lat = -180, 180

        m = folium.Map(max_bounds = True,
                       location = [avg_lat, avg_lon],
                       zoom_start=3,
                       min_lat = min_lat,
                       max_lat = max_lat,
                       min_lon = min_lon,
                       max_lon = max_lon,
                       )
        folium.CircleMarker([max_lat, min_lon], tooltip="Upper Left Corner").add_to(m)
        folium.CircleMarker([min_lat, min_lon], tooltip="Lower Left Corner").add_to(m)
        folium.CircleMarker([min_lat, max_lon], tooltip="Lower Right Corner").add_to(m)
        folium.CircleMarker([max_lat, max_lon], tooltip="Upper Right Corner").add_to(m)

        airports_marker = folium.FeatureGroup(name='Airports', overlay=True, control=True, show=False)
        for node in self.graph.nodes():
            if 'pos' in self.graph.nodes[node]:
                lat, lon = self.graph.nodes[node]['pos']
                folium.Marker([lat, lon], popup=node, icon=folium.Icon(color='gray')).add_to(airports_marker)
                airports_marker.add_to(m)

        if self.path:
            path_coords = [self.graph.nodes[airport]['pos'] for airport in self.path]
            start_coords =self.graph.nodes[self.path[0]]['pos']
            end_coords = self.graph.nodes[self.path[len(self.path)-1]]['pos']

            folium.map.CustomPane(name='path', z_index=625)
            traj_group = folium.FeatureGroup(name="Trajectory", overlay=True, control = True, pane = 'path')
            folium.Marker(start_coords, popup=self.path[0], icon=folium.Icon(color='blue')).add_to(traj_group)
            if len(self.path) != 2 :
                for airports in self.path[1:-1]:
                    coords = self.graph.nodes[airports]['pos']
                    folium.Marker(coords, popup=airports, icon=folium.Icon(color='green')).add_to(traj_group)
            folium.Marker(end_coords, popup=self.path[len(self.path)-1], icon=folium.Icon(color='red')).add_to(traj_group)
            folium.PolyLine(
                locations=path_coords,
                color='red',
                weight=3,
                opacity=0.7,
                pane = 'top'
            ).add_to(traj_group)
            traj_group.add_to(m)

        legend_html = '''
                    <div style="position: fixed; 
                                bottom: 50px; left: 50px; width: 180px; height: 120px; 
                                background-color: white; z-index:9999; font-size:14px;
                                border:2px solid grey; padding: 10px;">
                    <b>Légende</b><br>
                    <i style="color:blue">■</i> Aéroport de départ<br>
                    <i style="color:green">■</i> Aéroport de transition<br>
                    <i style="color:red">■</i> Aéroport d'arrivée<br>
                    <i style="color:red">―</i> Trajectoire optimale
                    </div>
                '''
        m.get_root().html.add_child(folium.Element(legend_html))

        folium.LayerControl().add_to(m)
        return m


class TrajectoryOptimizer:
    def __init__(self, graph):
        self.graph = graph

    def optimize_trajectory(self, start, end):
        try:
            path = nx.dijkstra_path(self.graph, start, end, weight='weight')
            cost = nx.dijkstra_path_length(self.graph, start, end, weight='weight')
            duration = sum(self.graph[u][v]['time'] for u, v in zip(path[:-1], path[1:]))
            return path, cost, duration

        except nx.NetworkXNoPath:
            raise ValueError(f"Aucun chemin trouvé entre {start} et {end}")


class UserInterface:
    def __init__(self):
        self.data_loader = DataLoader()
        self.flight_data = None
        self.airport_coords = None
        self.trajectory_modeler = None
        self.airports = []

    def load_data(self):
        self.flight_data = self.data_loader.load_flight_data("Distance_airports.csv")
        self.airport_coords = self.data_loader.airport_coords
        self._init_airports()

    def _init_airports(self):
        valid_airports = set(self.airport_coords.keys())
        departures = set(self.flight_data['ORIGIN']) & valid_airports
        arrivals = set(self.flight_data['DEST']) & valid_airports
        self.airports = sorted(list(departures | arrivals))

    def select_airports(self):
        print("\n" + "=" * 40)
        print("AÉROPORTS DISPONIBLES:")
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
            print("L'aéroport d'arrivée doit être différent du départ!\n")
        return start, end

    def run(self):
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
                print("Carte enregistrée sous 'map.html'. Ouvrez-la dans un navigateur pour la voir.")
            except ValueError as e:
                print(f"\nErreur: {str(e)}\n")
            if input("Voulez-vous faire une autre recherche? (o/n) ").lower() != 'o':
                break


if __name__ == "__main__":
    interface = UserInterface()
    interface.run()
