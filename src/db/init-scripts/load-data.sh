#!/bin/bash
set -e

echo "Loading raw data into PostgreSQL..."

# Load recipes data
if [ -f "/docker-entrypoint-initdb.d/RAW_recipes.csv" ]; then
    echo "Loading recipes data..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        \copy raw_recipes FROM '/docker-entrypoint-initdb.d/RAW_recipes.csv' DELIMITER ',' CSV HEADER;
EOSQL
fi

# Load interactions data
if [ -f "/docker-entrypoint-initdb.d/RAW_interactions.csv" ]; then
    echo "Loading interactions data..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        \copy raw_interactions FROM '/docker-entrypoint-initdb.d/RAW_interactions.csv' DELIMITER ',' CSV HEADER;
EOSQL
fi

echo "Data loading completed!"