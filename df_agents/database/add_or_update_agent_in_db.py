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

# Define the agent data in a variable, easy to edit
agent_data = {
    "id": 3,  # Set this to the agent's id if you want to update, else None
    "name": "Paid User Onboarding Agent",
    "description": "Writes onboarding emails based on the usecases identified.",
    "icon": "fa-regular fa-landmark-magnifying-glass",
    "tags": "Sales, CSM",
    "slug": "user-onboarding-agent",  # Slug must be unique
    "status": "Active",
    "visibility": "dealfronters_only",
    "metadata": {"question": "What is the account id?", "placeholder": "Enter account id OR JSON with account info", "additional_info": "To get the JSON about your account, open this metabase report LINK, download and copy the content here."}
}
# agent_data = {
#     "id": None,  # Set this to the agent's id if you want to update, else None
#     "name": "Company Research Agent",
#     "description": "This is a new agent for demonstrating how to add agents.",
#     "icon": "fa-regular fa-landmark-magnifying-glass",
#     "tags": "Sales, Operations",
#     "slug": "company-research-agent",  # Slug must be unique
#     "status": "Active",
#     "visibility": "public",
#     "metadata": {"question": "What data do you need?", "placeholder": "Enter data"}
# }

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

# Function to insert or update agent
def upsert_agent(agent_data):
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

        # Check if the agent already exists by id (for update)
        if agent_data['id']:
            # Update existing agent
            cur.execute("""
                UPDATE agents
                SET name = %s, description = %s, icon = %s, tags = %s, slug = %s,
                    status = %s, visibility = %s, metadata = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """, (
                    agent_data['name'], agent_data['description'], agent_data['icon'], 
                    agent_data['tags'], agent_data['slug'], agent_data['status'], 
                    agent_data['visibility'], Json(agent_data['metadata']), agent_data['id']
                ))
            print(f"Agent with id {agent_data['id']} updated successfully.")
        else:
            # Insert new agent and return the generated id
            cur.execute("""
                INSERT INTO agents (name, description, icon, tags, slug, status, visibility, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (
                    agent_data['name'], agent_data['description'], agent_data['icon'],
                    agent_data['tags'], agent_data['slug'], agent_data['status'],
                    agent_data['visibility'], Json(agent_data['metadata'])
                ))

            # Fetch the ID of the newly inserted agent
            new_agent_id = cur.fetchone()[0]
            print(f"New agent added with id: {new_agent_id}")

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cur.close()
        connection.close()

    except Exception as e:
        print(f"Error occurred while inserting/updating the agent: {e}")

if __name__ == '__main__':
    upsert_agent(agent_data)