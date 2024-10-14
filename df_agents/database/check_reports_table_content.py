import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection details
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_HOST = 'localhost'
DB_PORT = 5432

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

# Function to execute a query and display the results
def check_table_content(query):
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

        # Execute the passed query
        cur.execute(query)
        rows = cur.fetchall()

        # Print the result rows
        print(f"Results of the query '{query}':")
        for row in rows:
            print(row)

        # Close the cursor and connection
        cur.close()
        connection.close()

    except Exception as e:
        print(f"Error occurred while querying the database: {e}")

# Function to check the content of the reports table specifically
def check_reports_content():
    query = "SELECT * FROM reports;"
    check_table_content(query)

if __name__ == '__main__':
    check_reports_content()