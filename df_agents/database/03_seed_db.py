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
    ('Company Research Agent', 'Researches information and creates a comprehensive report about a given company.', 'fa-regular fa-landmark-magnifying-glass', 'Sales, Marketing', 'company-research-agent', 'Active', 'public', {"question": "What company do you want to research?", "placeholder": "Enter company name"}),
    ('Competitors Research Agent', 'Finds info about the main competitors for the given company.', 'fa-regular fa-landmark-magnifying-glass', 'Sales, Operations', 'competitors-research-agent', 'Active', 'public', {"question": "What company do you want to find competitors for?", "placeholder": "Enter company website. E.g. www.dealfront.com"})
]

reports = [
    (1, 101, 201, 'Not Started', {"company": "Coca Cola"}, {"summary": "Company research complete"}),
    (1, 101, 201, 'Completed', {"company": "Twitter"},  {"summary": "Company research complete"}),
    (1, 101, 201, 'In Progress', {"company": "Tesla"},  {"summary": "Sales forecast is being generated"}),
    (3, 103, 203, 'Failed', {"company": "Dealfront"},  {"summary": "Unable to complete market analysis"})
] # Uncomment the function below, else these will not be seeded

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
        INSERT INTO agents (name, description, icon, tags, slug, status, visibility, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, [(agent[0], agent[1], agent[2], agent[3], agent[4], agent[5], agent[6], Json(agent[7])) for agent in agents])
        
        # Insert into reports table. Uncomment when needed.
        cur.executemany("""
        INSERT INTO reports (agent_id, user_id, account_id, status, user_input, result)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, [(report[0], report[1], report[2], report[3], Json(report[4]), Json(report[5])) for report in reports])
        
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