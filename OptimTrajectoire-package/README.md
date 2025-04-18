# OptimTrajectoire

Module Python pour optimiser des trajets aériens avec visualisation cartographique.

# Installation 

Se placer dans le fichier OptimTrajectoire-package et exécuter la commande : 
python setup.py install 

# Utilisation 

Le fonctionnement standard s'effectue en exécutant la fonction run() de la class UserInterface
Donc dans le terminal python : 
import OptimTrajectoire 
OptimTrajectoire.UserInterface().run()

Puis suivre les indications pour les entrées utilisateurs : choix de l'appareil puis choix du trajet

le module sortira une carte disponible dans les fichiers du projet python ainsi que au lieu fourni.

# Librairies requises 
 Networkx
 folium 
 pandas
