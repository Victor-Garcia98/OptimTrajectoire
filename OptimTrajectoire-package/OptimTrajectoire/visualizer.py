"""
Module de visualisation des trajectoires sur une carte interactive.
"""

import folium

class TrajectoryVisualizer:
    """
    Affiche la trajectoire optimale entre aéroports sur une carte Folium.
    """
    def __init__(self, graph, path=None):
        self.graph = graph
        self.path = path

    def plot_trajectory(self):
        """
        Génère une carte interactive avec la trajectoire optimale.

        :return: Carte Folium avec la trajectoire tracée
        :rtype: folium.Map
            .
        """
        airport_positions = [self.graph.nodes[node]['pos'] for node in self.graph.nodes()]
        avg_lat = sum(lat for lat, lon in airport_positions) / len(airport_positions)
        avg_lon = sum(lon for lat, lon in airport_positions) / len(airport_positions)

        min_lon, max_lon = -180, 180
        min_lat, max_lat = -180, 180

        m = folium.Map(max_bounds=True,
                       location=[avg_lat, avg_lon],
                       zoom_start=3,
                       min_lat=min_lat,
                       max_lat=max_lat,
                       min_lon=min_lon,
                       max_lon=max_lon,
                       )

        airports_marker = folium.FeatureGroup(name='Airports', overlay=True, control=True, show=False)
        for node in self.graph.nodes():
            if 'pos' in self.graph.nodes[node]:
                lat, lon = self.graph.nodes[node]['pos']
                folium.Marker([lat, lon], popup=node, icon=folium.Icon(color='gray')).add_to(airports_marker)
                airports_marker.add_to(m)

        if self.path:
            path_coords = [self.graph.nodes[airport]['pos'] for airport in self.path]
            start_coords = self.graph.nodes[self.path[0]]['pos']
            end_coords = self.graph.nodes[self.path[len(self.path) - 1]]['pos']

            folium.map.CustomPane(name='path', z_index=625)
            traj_group = folium.FeatureGroup(name="Trajectory", overlay=True, control=True, pane='path')
            folium.Marker(start_coords, popup=self.path[0], icon=folium.Icon(color='blue')).add_to(traj_group)
            if len(self.path) != 2:
                for airports in self.path[1:-1]:
                    coords = self.graph.nodes[airports]['pos']
                    folium.Marker(coords, popup=airports, icon=folium.Icon(color='green')).add_to(traj_group)
            folium.Marker(end_coords, popup=self.path[len(self.path) - 1], icon=folium.Icon(color='red')).add_to(
                traj_group)
            folium.PolyLine(
                locations=path_coords,
                color='red',
                weight=3,
                opacity=0.7,
                pane='top'
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
