import psycopg2
import os
import json
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = 5432

def get_db_connection():
    """Creates and returns a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None
    
def fetch_job_details(job_id):
    """Reads job details from the database using job_id."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM reports WHERE id = %s;", (job_id,))
            job_details = cur.fetchone()  # Retrieve the job details
        return job_details
    except Exception as e:
        print(f"Error fetching job details: {e}")
        return None
    finally:
        conn.close()

def update_job_status(job_id, status, result=None):
    """Updates the status and result of a job."""
    conn = get_db_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE reports
                SET status = %s, result = %s, updated_at = NOW()
                WHERE id = %s;
                """,
                (status, json.dumps(result) if result else None, job_id)
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating job: {e}")
        return False
    finally:
        conn.close()