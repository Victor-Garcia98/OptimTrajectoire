# OptimTrajectoire

Module Python pour optimiser des trajets aériens avec visualisation cartographique.

# Installation 

Se placer dans le fichier OptimTrajectoire-package et exécuter la commande : 
python setup.py install 

# Librairies requises 
 Networkx
 folium 
 pandas

# Utilisation 

Le fonctionnement standard s'effectue en exécutant la fonction run() de la class UserInterface
Donc dans le terminal python : 
import OptimTrajectoire 
OptimTrajectoire.UserInterface().run()

Puis suivre les indications pour les entrées utilisateurs : choix de l'appareil puis choix du trajet

le module sortira une carte disponible dans les fichiers du projet python ainsi que au lieu fourni.

Si besoin : exécuter main() pour un résultat similaire

# Documentation 

La documentation est disponible en HTML dans le dossier build

# Contenu package 

Ce package contient 3 dossiers : 
OptimTrajectoire qui contient les fichiers python nécéssaire au fonctionnement 
build qui contient la documentation générée par Sphinx
source qui contient les fichiers rst si il y a besoin de re-générer la documentation 

La license MIT
Ce fichier README
les fichiers setup pour l'installation
Le fichier requirements pour l'installation rapide des librairies


