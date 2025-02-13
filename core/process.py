import os
from sentence_transformers import SentenceTransformer
from core.CV_processing import load_resume, generate_embedding
from core.Job_processign import calculate_scores
from core.hybrid_job_scraper import HybridPageScraper
from core.job_scraper_context import JobScraperContext
from core.filttering_url import get_filter_url
from DB.show_data import display_all_jobs
from configuration.config import websites
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
# Suppress tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def show_data():
    """
    Display all jobs from the database.
    """
    display_all_jobs()

def run_scraping(selected_websites):
    """
    Scrape jobs from the selected websites and process them.
    """
    # Load the resume
    resume_file_path = 'core/Daniel_Salame_CV.txt'
    resume_text = load_resume(resume_file_path)

    # Load embedding model
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    resume_embedding = generate_embedding(resume_text, embedding_model)

    for website_name in selected_websites:
        print(f"Scraping jobs from {website_name}...")
        config = websites[website_name]
        newurl = get_filter_url(config["url"], config["filters"])
        if newurl is None:
            print("Invalid filter selected. Skipping website.")
            continue

        scraper = HybridPageScraper(config["selectors"], newurl)
        context = JobScraperContext(scraper)
        jobs = context.scrape_jobs(newurl, use_requests=False)  # Change to True for Requests
        print(f"Scraped {len(jobs)} jobs from {website_name}.\n")

        # Process each job
        for job in jobs:
            job_title = job['title']
            job_description = job['description']
            job_link = job['link']

            # Generate embeddings for job description
            job_embedding = generate_embedding(job_description, embedding_model)

            # Calculate similarity scores
            scores = calculate_scores(resume_embedding, job_embedding)

            # Display results
            print("=" * 50)
            print(f"Job Title: {job_title}")
            print("Scores:")
            print(f"  - Job Matches CV: {scores['job_matches_cv']:.4f}")
            print(f"  - CV Matches Job: {scores['cv_matches_job']:.4f}")
            print(f"  - Semantic Match: {scores['semantic_match']:.4f}")
            print(f"  - Contextual Match: {scores['contextual_match']:.4f}")
            print(f"  - Overall Score: {scores['overall_score']:.4f}")
            print(f"Description: {job_description}")
            print(f"Job Link: {job_link}")
            print("=" * 50)

            # Insert job into the database if not exists
            scraper.insert_job_to_db(
                job.get("id", ""),
                job.get("company", "Unknown"),
                job_title,
                job_description,
                job_link,
                job.get("location", "Unknown"),
            )