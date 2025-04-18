"""
Module de gestion des modèles d'avions.
"""

class Aircraft:
    """
    Gère différents modèles d'avions et calcule la consommation.
    """
    def __init__(self):
        self.models = {
            'A320': {'fuel_burn_kgph': 2406, 'cruise_speed_kts': 447, 'max_fuel_per_flight': 24456.33},
            'B777': {'fuel_burn_kgph': 6834, 'cruise_speed_kts': 488, 'max_fuel_per_flight': 145538},
            'A380': {'fuel_burn_kgph': 6834, 'cruise_speed_kts': 488, 'max_fuel_per_flight': 253983},
            'E195': {'fuel_burn_kgph': 2406, 'cruise_speed_kts': 470, 'max_fuel_per_flight': 12971},
            'B737': {'fuel_burn_kgph': 2406, 'cruise_speed_kts': 453, 'max_fuel_per_flight': 21011.4},
            'CRJ9': {'fuel_burn_kgph': 1476, 'cruise_speed_kts': 447, 'max_fuel_per_flight': 8888},
            'C56X': {'fuel_burn_kgph': 558, 'cruise_speed_kts': 430, 'max_fuel_per_flight': 3057.213},
        }
        self.selected_model = None

    def select_model(self):
        """
        Permet à l'utilisateur de sélectionner un modèle d'avion parmi ceux disponibles.
        """
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
        """
        Calcule la consommation de carburant par mile pour le modèle sélectionné.

        :return: Consommation en kg/mile.
        :rtype: float


        :raises: ValueError Si aucun modèle n'est sélectionné.

        """
        if self.selected_model is None:
            raise ValueError("Aucun modèle sélectionné.")
        data = self.models[self.selected_model]
        speed_knots = data['cruise_speed_kts']
        fuel_burn_kgph = data['fuel_burn_kgph']
        speed_mph = speed_knots * 1.15078
        return fuel_burn_kgph / speed_mph
