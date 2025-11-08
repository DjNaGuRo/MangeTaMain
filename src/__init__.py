"""
Package principal pour le projet MangeTaMain
Contient les modules de traitement des données et d'analyse
"""

__version__ = "1.0.0"
__author__ = "Votre Nom"

# Import des modules principaux pour faciliter l'accès
from . import preprocessing
from . import data_visualization
from . import data_management_with_psql

# Optionnel: exposer les fonctions les plus utilisées
from .data_management_with_psql import (
    load_clean_recipes_from_db,
    load_clean_interactions_from_db,
    load_clean_merged_from_db,
    load_recipes_data_from_db,
    load_interactions_data_from_db,
)

from .preprocessing import detect_missing_values


__all__ = [
    "data_management_with_psql",
    "preprocessing",
    "load_interactions_data_from_db",
    "load_recipes_data_from_db",
    "data_visualization",
    "load_clean_recipes_from_db",
    "load_clean_interactions_from_db",
    "load_clean_merged_from_db",
    "detect_missing_values",
]
