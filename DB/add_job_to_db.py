import hashlib  # For creating a unique hash
import psycopg2  # For database connection

# Database configuration
DATABASE = {
    'dbname': 'jobs_db',
    'user': 'danielsa',
    'password': '',  # Add your PostgreSQL password if needed
    'host': 'localhost',
    'port': 5432
}

# Function to generate a UUID from job details
def generate_uuid(job_id, job_title, company, link):
    # Combine fields into a single string
    unique_string = f"{job_id}_{job_title}_{company}_{link}"
    # Create a hash of the combined string
    return hashlib.md5(unique_string.encode()).hexdigest()

# Function to insert a job into the database
def insert_job_to_db(job_id, company, title, description, link, location):
    # Ensure job_id is unique by generating a UUID if it's missing or "Unknown"
    if not job_id or job_id.strip() == "" or job_id == "Unknown":
        job_id = generate_uuid(job_id, title, company, link)

    # Default company if it is None or empty
    if not company or company.strip() == "":
        company = "Unknown"

    query = """
    INSERT INTO jobs (job_id, company, title, description, link, location)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (job_id, company, link) DO NOTHING;  -- Prevent duplicate entries
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DATABASE)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query, (job_id, company, title, description, link, location))

        # Commit changes
        conn.commit()
        print(f"Job '{title}' added to the database successfully!")

    except Exception as e:
        print(f"Error inserting job into database: {e}")

    finally:
        # Close the connection
        cursor.close()
        conn.close()

