import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

from path_config import RAW_DATA_DIR, DB_DIR

load_dotenv(dotenv_path=os.path.join(DB_DIR, '.env'))


class Db:
    def __init__(self, overwrite_raw_data=False):
        # Create SQLAlchemy engine using environment variables
        db_url = (
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
            f"{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOSTNAME')}:"
            f"{os.getenv('POSTGRES_PORT')}/"
            f"{os.getenv('POSTGRES_DB')}"
        )
        self.engine = create_engine(db_url)

        self.raw_recipes_path = os.path.join(RAW_DATA_DIR, 'RAW_recipes.csv')
        self.raw_interactions_path = os.path.join(
            RAW_DATA_DIR, 'RAW_interactions.csv'
        )
        self.final_data_path = os.path.join(RAW_DATA_DIR, 'final_data.csv')

        if overwrite_raw_data:
            # Save to database
            self._save_raw_recipes_to_db()
            self._save_raw_interactions_to_db()

    def _save_raw_recipes_to_db(self):
        pd.read_csv(self.raw_recipes_path).to_sql(
            'raw_recipes', self.engine, if_exists='replace', index=False
        )

    def _save_raw_interactions_to_db(self):
        pd.read_csv(self.raw_interactions_path).to_sql(
            'raw_interactions', self.engine, if_exists='replace', index=False
        )

    def fetch_raw_recipes(self):
        query = "SELECT * FROM raw_recipes;"
        return pd.read_sql(query, self.engine)

    def fetch_raw_interactions(self):
        query = "SELECT * FROM raw_interactions;"
        return pd.read_sql(query, self.engine)

    def close(self):
        self.engine.dispose()
