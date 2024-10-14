import os
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetching environment variables with fallback defaults
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = 'localhost'
DB_PORT = 5432

# Seed data
agents = [
    ('Company Research Agent', 'Researches information and creates a comprehensive report about a given company.', 'fa-regular fa-landmark-magnifying-glass', 'Sales, Marketing', 'companyresearchagent', {"question": "What company do you want to research?", "placeholder": "Enter company name"}),
    ('Similar Companies Agent', 'Discovers key similar companies to the one provided.', 'fa-regular fa-chart-network', 'Sales, Operations', 'similarcompaniesagent', {"question": "What is the company you want to find similar companies for?", "placeholder": "Enter company name"})
]

reports = [
    (1, 101, 201, 'Not Started', {"summary": "Company research complete"}),
    (1, 101, 201, 'Completed', {"summary": "Company research complete"}),
    (1, 101, 201, 'In Progress', {"summary": "Sales forecast is being generated"}),
    (3, 103, 203, 'Failed', {"summary": "Unable to complete market analysis"})
]

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

# Function to seed the database
def seed_database():
    # First, try to connect using the value of DB_HOST
    connection = connect_to_db(DB_HOST)

    # If the connection fails, fall back to localhost
    if not connection:
        print("Falling back to localhost...")
        connection = connect_to_db('localhost')

    # If connection still fails, exit with an error message
    if not connection:
        print("Failed to connect to the database with both DB_HOST and localhost.")
        return

    try:
        cur = connection.cursor()

        # Insert into agents table
        cur.executemany("""
        INSERT INTO agents (name, description, icon, tags, slug, metadata)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, [(agent[0], agent[1], agent[2], agent[3], agent[4], Json(agent[5])) for agent in agents])

        # Insert into reports table
        cur.executemany("""
        INSERT INTO reports (agent_id, user_id, account_id, status, result)
        VALUES (%s, %s, %s, %s, %s)
        """, [(report[0], report[1], report[2], report[3], Json(report[4])) for report in reports])
        
        # Commit changes
        connection.commit()

        # Close the cursor and connection
        cur.close()
        connection.close()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error occurred while seeding the database: {e}")

if __name__ == '__main__':
    seed_database()