-- Create the main database
CREATE DATABASE mangetamain;

-- Connect to the database
\c mangetamain;

-- Create tables for your raw data
CREATE TABLE IF NOT EXISTS raw_recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    ingredients TEXT,
    -- Add other columns based on your CSV structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    recipe_id INTEGER,
    rating DECIMAL,
    -- Add other columns based on your CSV structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_raw_recipes_name ON raw_recipes(name);
CREATE INDEX idx_raw_interactions_user_id ON raw_interactions(user_id);
CREATE INDEX idx_raw_interactions_recipe_id ON raw_interactions(recipe_id);-- Create the main database
CREATE DATABASE mangetamain;

-- Connect to the database
\c mangetamain;

-- Create tables for your raw data
CREATE TABLE IF NOT EXISTS raw_recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    ingredients TEXT,
    -- Add other columns based on your CSV structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    recipe_id INTEGER,
    rating DECIMAL,
    -- Add other columns based on your CSV structure
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_raw_recipes_name ON raw_recipes(name);
CREATE INDEX idx_raw_interactions_user_id ON raw_interactions(user_id);
CREATE INDEX idx_raw_interactions_recipe_id ON raw_interactions(recipe_id);