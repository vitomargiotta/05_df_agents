import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetching environment variables with fallback defaults
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = 'localhost'
DB_PORT = 5432

# SQL commands to create the tables
create_agents_table = """
CREATE TABLE IF NOT EXISTS agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon TEXT,
    tags VARCHAR(255),
    slug VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_jobs_table = """
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    result JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Function to attempt a database connection
def connect_to_db(host):
    try:
        # Attempt to connect to the PostgreSQL database
        print(f"Attempting to connect to the database at {host}...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=host,
            port=DB_PORT
        )
        print(f"Connected to the database using host: {host}")
        return conn
    except Exception as e:
        print(f"Error occurred during the connection to the database at {host}: {e}")
        return None

# Function to create tables
def create_tables():
    # First, try to connect using the value of DB_HOST
    connection = connect_to_db(DB_HOST)

    # If the connection fails, fall back to localhost
    if not connection:
        print("Falling back to localhost...")
        connection = connect_to_db('localhost')

    # If the connection still fails, exit with an error message
    if not connection:
        print("Failed to connect to the database with both DB_HOST and localhost.")
        return

    try:
        cur = connection.cursor()

        # Create tables
        cur.execute(create_agents_table)
        cur.execute(create_jobs_table)

        # Commit changes
        connection.commit()

        # Close the cursor and connection
        cur.close()
        connection.close()

        print("Tables created successfully!")
    except Exception as e:
        print(f"Error occurred while creating tables: {e}")

if __name__ == '__main__':
    create_tables()