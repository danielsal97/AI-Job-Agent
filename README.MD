+++

AI Job Agent

This project is a Python-based tool that matches job descriptions with resumes by calculating similarity scores using embeddings and natural language processing techniques. It includes functionalities for scraping job postings, generating embeddings, and evaluating similarity metrics to provide insights into how well a resume aligns with job opportunities.

Features
	•	Job Scraping:
	•	Uses CSS selectors to scrape job listings from websites like NVIDIA.
	•	Extracts job titles, descriptions, and other relevant details.
	•	Resume Processing:
	•	Processes resumes for embedding generation using SentenceTransformer models.
	•	Job Processing:
	•	Generates embeddings for job descriptions and compares them with the resume.
	•	Similarity Scoring:
	•	Calculates similarity scores using cosine similarity and dot product.
	•	Provides metrics such as Job-to-Resume Match, Resume-to-Job Match, Semantic Match, Contextual Match, and Overall Score.

Project File Structure

AI_Job_Agent/
├── pycache/                # Auto-generated Python cache files
├── venv/                   # Virtual environment (not included in version control)
├── .gitignore              # Git configuration to ignore specific files
├── config.py               # Configuration for settings (e.g., selectors, paths)
├── CV_processing.py        # Resume processing and embedding generation
├── Daniel_Salame_CV.txt    # Sample resume file
├── hybrid_job_scraper.py   # Hybrid job scraper implementation
├── installer.py            # Installer script for dependencies
├── Job_processign.py       # Job posting processing and embedding generation
├── job_scraper_context.py  # Handles context and orchestration for job scraping
├── main.py                 # Entry point for running the application
├── README.MD               # Documentation for the project
├── requirements.txt        # Dependencies required for the project

Setup Instructions

Prerequisites
	1.	Install Python 3.7 or higher.
	2.	Install required dependencies using one of the following methods:

Option 1: Using Virtual Environment
	1.	Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows


	2.	Install dependencies:

pip install -r requirements.txt



Option 2: Using Installer Script

Run the installer script to install all dependencies:

python installer.py

Clone the Repository

Clone the project repository and navigate to the project directory:

git clone https://github.com/danielsal97/AI-Job-Agent.git
cd AI_Job_Agent

Environment Configuration
	1.	Suppress Tokenizer Warnings:

export TOKENIZERS_PARALLELISM=false


	2.	Set Resume Path:
Open the main.py file and set the path to your resume file:

resume_path = 'Daniel_Salame_CV.txt'



Run the Project
	1.	Run the main.py file to start the process:

python main.py


	2.	The script will:
	•	Scrape job postings using CSS selectors.
	•	Generate embeddings for the resume and job descriptions.
	•	Calculate similarity scores between the resume and job descriptions.
	•	Display the matching scores and job details.

Configuration

CSS Selectors for Job Scraping

The CSS selectors for scraping job postings are stored in config.py. Example configuration:

websites = {
    "nvidia": {
        "url": "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite",
        "job_card": "li.css-1q2dra3",
        "job_title": "h3 a[data-automation-id='jobTitle']",
        "job_title_detail": "h2[data-automation-id='jobPostingHeader']",
        "job_location": "div[data-automation-id='locations']",
        "job_date": "div[data-automation-id='postedOn']",
        "job_description": "div[data-automation-id='jobPostingDescription']",
        "next_button": "button[aria-label='Next']",
    }
}

Code Structure

Main Files
	•	main.py: Entry point for running the project. Loads the resume, scrapes job postings, and calculates similarity scores.
	•	config.py: Stores configuration settings like CSS selectors for job scraping.
	•	hybrid_job_scraper.py: Contains the hybrid implementation for scraping job postings.
	•	job_scraper_context.py: Manages the context and orchestration for job scraping.
	•	CV_processing.py: Handles resume processing and embedding generation.
	•	Job_processign.py: Handles job description processing and embedding generation.
	•	installer.py: Script to automate dependency installation.

Supporting Files
	•	Daniel_Salame_CV.txt: Example resume for testing.
	•	requirements.txt: List of required Python libraries.
	•	README.MD: Detailed documentation for the project.

Sample Output

==================================================
Job Title: Software Engineer - AI
Scores:
  - Job Matches CV: 0.8921
  - CV Matches Job: 0.8754
  - Semantic Match: 0.8838
  - Contextual Match: 0.7137
  - Overall Score: 0.8413
Description: Work on cutting-edge AI projects to deliver next-gen solutions.
Job Link: https://nvidia.jobs/12345
==================================================

Future Improvements
	1.	Add advanced NLP models like GPT or LLaMA for generating detailed explanations of matches.
	2.	Expand scraping functionality to support dynamic rendering (e.g., Selenium).
	3.	Create a web-based interface for user interaction.

Contributors
	•	Daniel Salame: Developer and maintainer of the project.
+++
