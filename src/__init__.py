"""
Package principal pour le projet MangeTaMain
Contient les modules de traitement des données et d'analyse
"""

__version__ = "1.0.0"
__author__ = "Votre Nom"

# Import des modules principaux pour faciliter l'accès
from . import data_loader
from . import preprocessing
from . import data_visualization
# Optionnel: exposer les fonctions les plus utilisées
from .data_loader import load_interactions_data, load_recipes_data,load_clean_recipes,load_clean_interactions, load_clean_merged
from .preprocessing import detect_missing_values


__all__ = [
    "data_loader",
    "preprocessing",
    "load_interactions_data",
    "load_recipes_data",
    "data_visualization",
    "load_clean_recipes",
    "load_clean_interactions",
    "load_clean_merged",
    "detect_missing_values",
]
