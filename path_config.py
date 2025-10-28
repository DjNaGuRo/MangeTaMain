from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

SRC_DIR = Path.joinpath(PROJECT_ROOT, "src")
DB_DIR = Path.joinpath(SRC_DIR, "db")
STREAMLIT_DIR = Path.joinpath(SRC_DIR, "streamlit")

DATA_DIR = Path.joinpath(PROJECT_ROOT, "data")
RAW_DATA_DIR = Path.joinpath(DATA_DIR, "raw")
POSTGRES_VOLUME = Path.joinpath(DATA_DIR, "postgresDB")

""" print("\n")
print("---- In path_config file ----")
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"SRC_DIR: {SRC_DIR}")
print(f"DB_DIR: {DB_DIR}")
print(f"STREAMLIT_DIR: {STREAMLIT_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
print(f"RAW_DATA_DIR: {RAW_DATA_DIR}")
print(f"POSTGRES_VOLUME: {POSTGRES_VOLUME}")
print("\n") """

