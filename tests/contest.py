# tests/conftest.py
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
import matplotlib
matplotlib.use("Agg")  # backend non graphique pour les tests
# rendre importable "src/"
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

print("[pytest] sys.path head =", sys.path[0])
print("[pytest] exists(data_visualization.py)?", (SRC / "data_visualization.py").exists())
