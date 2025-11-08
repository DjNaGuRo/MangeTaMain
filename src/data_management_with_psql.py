from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

from .logging_config import get_logger

# Essayer d'importer python-dotenv pour charger le fichier .env
try:
    # Charger le fichier .env s'il existe
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger = get_logger('data_management_psql')
        logger.info(f"Loaded environment variables from {env_path}")
    else:
        logger = get_logger('data_management_psql')
        logger.info("No .env file found, using system environment variables")
except ImportError:
    logger = get_logger('data_management_psql')
    logger.info("python-dotenv not installed, using system environment variables only")


# --- Configuration de base de données ---
def get_database_url():
    """Construit l'URL de la base de données à partir des variables d'environnement."""
    # Variables d'environnement OBLIGATOIRES - aucune valeur par défaut pour la sécurité
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_sslmode = os.getenv('DB_SSLMODE', 'require')  # Seule cette variable a une valeur par défaut sécurisée
    
    # Vérifier que toutes les variables requises sont définies
    missing_vars = []
    if not db_host:
        missing_vars.append('DB_HOST')
    if not db_port:
        missing_vars.append('DB_PORT')
    if not db_name:
        missing_vars.append('DB_NAME')
    if not db_user:
        missing_vars.append('DB_USER')
    if not db_password:
        missing_vars.append('DB_PASSWORD')
    
    if missing_vars:
        raise ValueError(
            f"Missing required database environment variables: {', '.join(missing_vars)}. "
            f"Please set these variables in your .env file or system environment. "
            f"See .env.template for an example."
        )
    
    # URL-encode le mot de passe pour gérer les caractères spéciaux comme @
    encoded_password = quote_plus(db_password)
    
    # Masquer le mot de passe dans les logs
    database_url = f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}?sslmode={db_sslmode}"
    logger.info(f"Database URL configured for {db_user}@{db_host}:{db_port}/{db_name} (password: {'*' * len(db_password)})")
    return database_url

DATABASE_URL = get_database_url()

# SQLAlchemy setup
Base = declarative_base()
engine = None
SessionLocal = None

# --- Définition des chemins ---
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Fichiers bruts
RAW_RECIPES = RAW_DIR / "RAW_recipes.csv"
RAW_INTERACTIONS = RAW_DIR / "RAW_interactions.csv"

# Fichiers nettoyés
CLEAN_RECIPES = PROCESSED_DIR / "recipes_cleaned.csv"
CLEAN_INTERACTIONS = PROCESSED_DIR / "interactions_cleaned.csv"
CLEAN_MERGED = PROCESSED_DIR / "merged_cleaned.csv"

# --- Noms des tables ---
TABLE_RAW_RECIPES = "raw_recipes"
TABLE_RAW_INTERACTIONS = "raw_interactions"
TABLE_CLEAN_RECIPES = "clean_recipes"
TABLE_CLEAN_INTERACTIONS = "clean_interactions"
TABLE_CLEAN_MERGED = "clean_merged"


def init_database():
    """Initialise la connexion à la base de données SQLAlchemy."""
    global engine, SessionLocal
    try:
        logger.info("Initializing SQLAlchemy database connection")
        engine = create_engine(DATABASE_URL, echo=False)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Successfully initialized database connection")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def get_session():
    """Retourne une session SQLAlchemy."""
    if SessionLocal is None:
        init_database()
    return SessionLocal()


def create_tables():
    """Crée les tables nécessaires dans la base de données."""
    try:
        if engine is None:
            init_database()
            
        logger.info("Creating database tables")
        Base.metadata.create_all(bind=engine)
        
        # Créer les tables avec SQL brut pour plus de contrôle
        with engine.connect() as conn:
            # Table pour les recettes brutes
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_RAW_RECIPES} (
                    name TEXT,
                    id INTEGER,
                    minutes INTEGER,
                    contributor_id INTEGER,
                    submitted DATE,
                    tags TEXT,
                    nutrition TEXT,
                    n_steps INTEGER,
                    steps TEXT,
                    description TEXT,
                    ingredients TEXT,
                    n_ingredients INTEGER
                );
            """))
            
            # Table pour les interactions brutes
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_RAW_INTERACTIONS} (
                    user_id INTEGER,
                    recipe_id INTEGER,
                    date DATE,
                    rating INTEGER,
                    review TEXT
                );
            """))
            
            # Table pour les recettes nettoyées
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_CLEAN_RECIPES} (
                    name TEXT,
                    id INTEGER,
                    minutes INTEGER,
                    contributor_id INTEGER,
                    submitted DATE,
                    tags TEXT,
                    nutrition TEXT,
                    n_steps INTEGER,
                    steps TEXT,
                    description TEXT,
                    ingredients TEXT,
                    n_ingredients INTEGER,
                    calories REAL,
                    total_fat REAL,
                    sugar REAL,
                    sodium REAL,
                    protein REAL,
                    saturated_fat REAL,
                    carbohydrates REAL
                );
            """))
            
            # Table pour les interactions nettoyées
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_CLEAN_INTERACTIONS} (
                    user_id INTEGER,
                    recipe_id INTEGER,
                    date DATE,
                    rating INTEGER,
                    review TEXT,
                    binary_sentiment INTEGER
                );
            """))
            
            # Table pour les données fusionnées nettoyées
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_CLEAN_MERGED} (
                    recipe_id INTEGER,
                    total_reviews INTEGER,
                    negative_reviews INTEGER,
                    minutes INTEGER,
                    submitted DATE,
                    tags TEXT,
                    nutrition TEXT,
                    n_steps INTEGER,
                    steps TEXT,
                    ingredients TEXT,
                    n_ingredients INTEGER,
                    calories REAL,
                    total_fat REAL,
                    sugar REAL,
                    sodium REAL,
                    protein REAL,
                    saturated_fat REAL,
                    carbohydrates REAL
                );
            """))
            
            conn.commit()
            
        logger.info("Successfully created all database tables")
        
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise


# --- Fonctions de stockage pour chaque table ---

def store_raw_recipes():
    """Stocke les données brutes des recettes dans la base de données."""
    try:
        if not RAW_RECIPES.exists():
            logger.warning(f"Raw recipes file not found: {RAW_RECIPES}")
            return
            
        logger.info(f"Loading raw recipes from {RAW_RECIPES}")
        df_recipes = pd.read_csv(RAW_RECIPES)
        logger.info(f"Storing {len(df_recipes)} raw recipes")
        
        if engine is None:
            init_database()
        
        # S'assurer que les colonnes correspondent au schéma de la table
        expected_columns = [
            'name', 'id', 'minutes', 'contributor_id', 'submitted', 'tags', 'nutrition',
            'n_steps', 'steps', 'description', 'ingredients', 'n_ingredients'
        ]
        df_recipes_mapped = df_recipes.copy()
        # Reorder and filter columns
        df_recipes_mapped = df_recipes_mapped[[col for col in expected_columns if col in df_recipes_mapped.columns]]

        with engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {TABLE_RAW_RECIPES}"))
            logger.info("Cleared existing raw recipes data")
            chunk_size = 100
            total_chunks = (len(df_recipes_mapped) + chunk_size - 1) // chunk_size
            for i, chunk in enumerate(df_recipes_mapped.groupby(df_recipes_mapped.index // chunk_size)):
                chunk_df = chunk[1]
                chunk_df.to_sql(
                    TABLE_RAW_RECIPES,
                    conn,
                    if_exists='append',
                    index=False
                )
                if (i + 1) % 10 == 0:
                    logger.info(f"Inserted chunk {i + 1}/{total_chunks} ({(i + 1) * chunk_size} records)")
        
        logger.info("Successfully stored raw recipes")
        
    except Exception as e:
        logger.error(f"Error storing raw recipes: {str(e)}")
        raise


def store_raw_interactions():
    """Stocke les données brutes des interactions dans la base de données."""
    try:
        if not RAW_INTERACTIONS.exists():
            logger.warning(f"Raw interactions file not found: {RAW_INTERACTIONS}")
            return
            
        logger.info(f"Loading raw interactions from {RAW_INTERACTIONS}")
        df_interactions = pd.read_csv(RAW_INTERACTIONS)
        logger.info(f"Storing {len(df_interactions)} raw interactions")
        
        if engine is None:
            init_database()
        
        # Utiliser une transaction pour tout le processus
        with engine.begin() as conn:
            # Vider la table existante
            conn.execute(text(f"DELETE FROM {TABLE_RAW_INTERACTIONS}"))
            logger.info("Cleared existing raw interactions data")
            
            # Insérer par chunks plus petits pour éviter les timeouts
            chunk_size = 100
            total_chunks = (len(df_interactions) + chunk_size - 1) // chunk_size
            
            for i, chunk in enumerate(df_interactions.groupby(df_interactions.index // chunk_size)):
                chunk_df = chunk[1]
                
                # Utiliser to_sql sans method='multi' pour éviter les gros statements
                chunk_df.to_sql(
                    TABLE_RAW_INTERACTIONS, 
                    conn, 
                    if_exists='append', 
                    index=False
                )
                
                if (i + 1) % 10 == 0:  # Log progress every 10 chunks
                    logger.info(f"Inserted chunk {i + 1}/{total_chunks} ({(i + 1) * chunk_size} records)")
        
        logger.info("Successfully stored raw interactions")
        
    except Exception as e:
        logger.error(f"Error storing raw interactions: {str(e)}")
        raise


def store_clean_recipes():
    """Stocke les données nettoyées des recettes dans la base de données."""
    try:
        if not CLEAN_RECIPES.exists():
            logger.warning(f"Clean recipes file not found: {CLEAN_RECIPES}")
            return
            
        logger.info(f"Loading clean recipes from {CLEAN_RECIPES}")
        df_recipes = pd.read_csv(CLEAN_RECIPES)
        logger.info(f"Storing {len(df_recipes)} clean recipes")
        
        if engine is None:
            init_database()
        
        # S'assurer que les colonnes correspondent au schéma de la table
        expected_columns = [
            'name', 'id', 'minutes', 'contributor_id', 'submitted', 'tags', 'nutrition',
            'n_steps', 'steps', 'description', 'ingredients', 'n_ingredients',
            'calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates'
        ]
        df_recipes_mapped = df_recipes.copy()
        # Reorder and filter columns
        df_recipes_mapped = df_recipes_mapped[[col for col in expected_columns if col in df_recipes_mapped.columns]]

        with engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {TABLE_CLEAN_RECIPES}"))
            logger.info("Cleared existing clean recipes data")
            chunk_size = 100
            total_chunks = (len(df_recipes_mapped) + chunk_size - 1) // chunk_size
            for i, chunk in enumerate(df_recipes_mapped.groupby(df_recipes_mapped.index // chunk_size)):
                chunk_df = chunk[1]
                chunk_df.to_sql(
                    TABLE_CLEAN_RECIPES,
                    conn,
                    if_exists='append',
                    index=False
                )
                if (i + 1) % 10 == 0:
                    logger.info(f"Inserted chunk {i + 1}/{total_chunks} ({(i + 1) * chunk_size} records)")
        
        logger.info("Successfully stored clean recipes")
        
    except Exception as e:
        logger.error(f"Error storing clean recipes: {str(e)}")
        raise


def store_clean_interactions():
    """Stocke les données nettoyées des interactions dans la base de données."""
    try:
        if not CLEAN_INTERACTIONS.exists():
            logger.warning(f"Clean interactions file not found: {CLEAN_INTERACTIONS}")
            return
            
        logger.info(f"Loading clean interactions from {CLEAN_INTERACTIONS}")
        df_interactions = pd.read_csv(CLEAN_INTERACTIONS)
        logger.info(f"Storing {len(df_interactions)} clean interactions")
        
        if engine is None:
            init_database()
        
        # S'assurer que les colonnes correspondent au schéma de la table
        expected_columns = [
            'user_id', 'recipe_id', 'date', 'rating', 'review', 'binary_sentiment'
        ]
        df_interactions_mapped = df_interactions.copy()
        # Add missing column if not present
        if 'binary_sentiment' not in df_interactions_mapped.columns:
            df_interactions_mapped['binary_sentiment'] = None
        # Reorder and filter columns
        df_interactions_mapped = df_interactions_mapped[[col for col in expected_columns if col in df_interactions_mapped.columns]]

        with engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {TABLE_CLEAN_INTERACTIONS}"))
            logger.info("Cleared existing clean interactions data")
            chunk_size = 100
            total_chunks = (len(df_interactions_mapped) + chunk_size - 1) // chunk_size
            for i, chunk in enumerate(df_interactions_mapped.groupby(df_interactions_mapped.index // chunk_size)):
                chunk_df = chunk[1]
                chunk_df.to_sql(
                    TABLE_CLEAN_INTERACTIONS,
                    conn,
                    if_exists='append',
                    index=False
                )
                if (i + 1) % 10 == 0:
                    logger.info(f"Inserted chunk {i + 1}/{total_chunks} ({(i + 1) * chunk_size} records)")
        
        logger.info("Successfully stored clean interactions")
        
    except Exception as e:
        logger.error(f"Error storing clean interactions: {str(e)}")
        raise


def store_clean_merged():
    """Stocke les données fusionnées nettoyées dans la base de données."""
    try:
        if not CLEAN_MERGED.exists():
            logger.warning(f"Clean merged file not found: {CLEAN_MERGED}")
            return
            
        logger.info(f"Loading clean merged data from {CLEAN_MERGED}")
        df_merged = pd.read_csv(CLEAN_MERGED)
        logger.info(f"Storing {len(df_merged)} clean merged records")
        
        if engine is None:
            init_database()
        
        # S'assurer que les colonnes correspondent au schéma de la table
        expected_columns = [
            'recipe_id', 'total_reviews', 'negative_reviews', 'minutes', 'submitted', 'tags',
            'nutrition', 'n_steps', 'steps', 'ingredients', 'n_ingredients',
            'calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates'
        ]
        df_merged_mapped = df_merged.copy()
        # Reorder and filter columns
        df_merged_mapped = df_merged_mapped[[col for col in expected_columns if col in df_merged_mapped.columns]]

        with engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {TABLE_CLEAN_MERGED}"))
            logger.info("Cleared existing clean merged data")
            chunk_size = 100
            total_chunks = (len(df_merged_mapped) + chunk_size - 1) // chunk_size
            for i, chunk in enumerate(df_merged_mapped.groupby(df_merged_mapped.index // chunk_size)):
                chunk_df = chunk[1]
                chunk_df.to_sql(
                    TABLE_CLEAN_MERGED,
                    conn,
                    if_exists='append',
                    index=False
                )
                if (i + 1) % 10 == 0:
                    logger.info(f"Inserted chunk {i + 1}/{total_chunks} ({(i + 1) * chunk_size} records)")
        
        logger.info("Successfully stored clean merged data")
        
    except Exception as e:
        logger.error(f"Error storing clean merged data: {str(e)}")
        raise


# --- Fonctions de stockage groupées ---

def store_all_raw_data():
    """Stocke toutes les données brutes dans la base de données."""
    try:
        logger.info("Starting to store all raw data")
        store_raw_recipes()
        store_raw_interactions()
        logger.info("Successfully stored all raw data")
    except Exception as e:
        logger.error(f"Error storing all raw data: {str(e)}")
        raise


def store_all_processed_data():
    """Stocke toutes les données traitées dans la base de données."""
    try:
        logger.info("Starting to store all processed data")
        store_clean_recipes()
        store_clean_interactions()
        store_clean_merged()
        logger.info("Successfully stored all processed data")
    except Exception as e:
        logger.error(f"Error storing all processed data: {str(e)}")
        raise


# --- Fonctions de récupération (format data_loader.py) ---

def load_recipes_data_from_db() -> pd.DataFrame:
    """Charge les données brutes des recettes depuis la base de données."""
    try:
        logger.info("Loading raw recipes data from database")
        
        if engine is None:
            init_database()
            
        query = f"SELECT * FROM {TABLE_RAW_RECIPES} ORDER BY id"
        df = pd.read_sql_query(query, engine)
            
        logger.info(f"Successfully loaded recipes data from DB: {df.shape[0]} rows, {df.shape[1]} columns")
        logger.debug(f"Recipes columns: {list(df.columns)}")
        return df
        
    except Exception as e:
        logger.error(f"Error loading recipes data from database: {str(e)}")
        raise


def load_interactions_data_from_db() -> pd.DataFrame:
    """Charge les données brutes des interactions depuis la base de données."""
    try:
        logger.info("Loading raw interactions data from database")
        
        if engine is None:
            init_database()
            
        query = f"SELECT * FROM {TABLE_RAW_INTERACTIONS} ORDER BY user_id, recipe_id"
        df = pd.read_sql_query(query, engine)
            
        logger.info(f"Successfully loaded interactions data from DB: {df.shape[0]} rows, {df.shape[1]} columns")
        logger.debug(f"Interactions columns: {list(df.columns)}")
        return df
        
    except Exception as e:
        logger.error(f"Error loading interactions data from database: {str(e)}")
        raise


def load_clean_recipes_from_db() -> pd.DataFrame:
    """Charge les recettes nettoyées depuis la base de données."""
    try:
        logger.info("Loading cleaned recipes data from database")
        
        if engine is None:
            init_database()
            
        query = f"SELECT * FROM {TABLE_CLEAN_RECIPES} ORDER BY id"
        df = pd.read_sql_query(query, engine)
            
        logger.info(f"Successfully loaded cleaned recipes from DB: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
        
    except Exception as e:
        logger.error(f"Error loading cleaned recipes data from database: {str(e)}")
        raise


def load_clean_interactions_from_db() -> pd.DataFrame:
    """Charge les interactions nettoyées depuis la base de données."""
    try:
        logger.info("Loading cleaned interactions data from database")
        
        if engine is None:
            init_database()
            
        query = f"SELECT * FROM {TABLE_CLEAN_INTERACTIONS} ORDER BY user_id, recipe_id"
        df = pd.read_sql_query(query, engine)
            
        logger.info(f"Successfully loaded cleaned interactions from DB: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
        
    except Exception as e:
        logger.error(f"Error loading cleaned interactions data from database: {str(e)}")
        raise


def load_clean_merged_from_db() -> pd.DataFrame:
    """Charge les données fusionnées nettoyées depuis la base de données."""
    try:
        logger.info("Loading merged cleaned data from database")
        
        if engine is None:
            init_database()

        query = f"SELECT * FROM {TABLE_CLEAN_MERGED} ORDER BY recipe_id"
        df = pd.read_sql_query(query, engine)
            
        logger.info(f"Successfully loaded merged data from DB: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
        
    except Exception as e:
        logger.error(f"Error loading merged cleaned data from database: {str(e)}")
        raise


def get_table_info():
    """Affiche des informations sur les tables de la base de données."""
    try:
        if engine is None:
            init_database()
            
        with engine.connect() as conn:
            tables = [
                TABLE_RAW_RECIPES,
                TABLE_RAW_INTERACTIONS,
                TABLE_CLEAN_RECIPES,
                TABLE_CLEAN_INTERACTIONS,
                TABLE_CLEAN_MERGED
            ]
            
            logger.info("Database table information:")
            print("\n=== DATABASE TABLE INFORMATION ===")
            
            for table in tables:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"{table}: {count} records")
                    logger.info(f"Table {table}: {count} records")
                except Exception as e:
                    print(f"{table}: Error - {str(e)}")
                    logger.warning(f"Error querying table {table}: {str(e)}")
            
            print("===================================\n")
                
    except Exception as e:
        logger.error(f"Error getting table info: {str(e)}")
        raise


# --- Fonctions utilitaires ---

def setup_database():
    """Configure la base de données (crée les tables si nécessaire)."""
    try:
        logger.info("Setting up database")
        init_database()
        create_tables()
        logger.info("Database setup completed successfully")
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        raise


def store_all_data():
    """Stocke toutes les données (brutes et traitées) dans la base de données."""
    try:
        logger.info("Starting to store all data")
        store_all_raw_data()
        store_all_processed_data()
        logger.info("Successfully stored all data")
    except Exception as e:
        logger.error(f"Error storing all data: {str(e)}")
        raise


def main():
    """Fonction principale pour tester la connexion et les opérations de base."""
    try:
        # Initialiser la base de données
        init_database()
        
        # Test de connexion
        with engine.connect() as conn:
            result = conn.execute(text('SELECT VERSION()'))
            version = result.fetchone()[0]
            print("PostgreSQL version:", version)
            logger.info(f"Connected to PostgreSQL version: {version}")
        
        # Créer les tables
        create_tables()
        
        # Afficher les informations sur les tables
        get_table_info()
        # Stocker toutes les données
        store_all_data()
        
        logger.info("Main function completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        raise


if __name__ == "__main__":
    get_table_info()
    