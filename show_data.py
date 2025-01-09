import psycopg2

# Database configuration
DATABASE = {
    'dbname': 'jobs_db',
    'user': 'danielsa',
    'password': '',  # Add your PostgreSQL password if needed
    'host': 'localhost',
    'port': 5432
}

def fetch_all_jobs_from_db():
    """
    Fetch all job data from the database and return it.
    """
    query = "SELECT job_id, company, title, description, link, location FROM jobs;"
    jobs = []
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DATABASE)
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query)
        jobs = cursor.fetchall()  # Get all results

        # Close the connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching jobs from database: {e}")
    
    return jobs

def display_all_jobs():
    """
    Fetch and display all jobs in the database.
    """
    jobs = fetch_all_jobs_from_db()
    
    if not jobs:
        print("No jobs found in the database.")
        return

    # # Display the job data in a readable format
    # print(f"\n{'Job ID':<30} {'Company':<20} {'Title':<50} {'Location':<20} {'Link':<100}")
    # print("="*220)  # Separator for readability

    for i , job in enumerate(jobs):
        job_id, company, title, description, link, location = job
        print(f"job number {i+1} \n{title:<30}\n ")

if __name__ == "__main__":
    display_all_jobs()