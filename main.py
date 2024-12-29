import os
from sentence_transformers import SentenceTransformer
from CV_processing import load_resume, generate_embedding
from Job_processign import calculate_scores
from hybrid_job_scraper import HybridJobScraper
from job_scraper_context import JobScraperContext
from config import websites

# Suppress tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def main():
    # Load the resume
    resume_path = 'Daniel_Salame_CV.txt'
    resume_text = load_resume(resume_path)

    # Load embedding model
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    resume_embedding = generate_embedding(resume_text, embedding_model)

    # Scrape and process jobs
    for website_name, config in websites.items():
        print(f"Scraping jobs from {website_name}...")
        scraper = HybridJobScraper(config["selectors"], config["url"])
        context = JobScraperContext(scraper)
        jobs = context.scrape_jobs(config["url"], use_requests=False)  # Change to True for Requests
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

if __name__ == "__main__":
    main()