# AI Job Agent

This project is a Python-based tool designed to match job descriptions with resumes by calculating similarity scores using embeddings and natural language processing techniques. It includes functionalities for scraping job postings, generating embeddings, and evaluating similarity metrics to provide insights into how well a resume aligns with job opportunities.

## Features

- **Job Scraping:**
	- Utilizes CSS selectors to scrape job listings from websites such as NVIDIA.
	- Extracts job titles, descriptions, and other pertinent details.
- **Resume Processing:**
	- Processes resumes for embedding generation using SentenceTransformer models.
- **Job Processing:**
	- Generates embeddings for job descriptions and compares them with the resume.
- **Similarity Scoring:**
	- Calculates similarity scores using cosine similarity and dot product.
	- Provides metrics such as Job-to-Resume Match, Resume-to-Job Match, Semantic Match, Contextual Match, and Overall Score.


## Setup Instructions

### Clone the Repository

Clone the project repository and navigate to the project directory:

```sh
git clone https://github.com/your-repo-name.git
cd AI_Job_Agent
```

### Prerequisites

1. Install Python 3.7 or higher.
2. Install required dependencies using one of the following methods:

#### Option 1: Using Virtual Environment

1. Create and activate a virtual environment:

	```sh
	python -m venv venv
	source venv/bin/activate  # For Linux/macOS
	venv\Scripts\activate  # For Windows
	```

2. Install dependencies:

	```sh
	pip install -r requirements.txt
	```

#### Option 2: Using Installer Script

Run the `installer.py` script to install all dependencies:

```sh
python installer.py
```

### Environment Configuration

1. Suppress Tokenizer Warnings:
		Add this environment variable to suppress tokenizers’ parallelism warnings:

		```sh
		export TOKENIZERS_PARALLELISM=false
		```

2. Set Resume Path:
		Open the `main.py` file and set the path to your resume file:

		```python
		resume_path = 'Daniel_Salame_CV.txt'
		```

### Run the Project

1. Execute the `main.py` file to start the process:

	```sh
	python main.py
	```

2. The script will:
		- Scrape job postings using CSS selectors.
		- Generate embeddings for the resume and job descriptions.
		- Calculate similarity scores between the resume and job descriptions.
		- Display the matching scores and job details.

## Configuration

### CSS Selectors for Job Scraping

The CSS selectors for scraping job postings are stored in `config.py`. Example configuration:

```python
websites_css_selectors = {
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
```


## Sample Output

```
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
```

## Future Improvements

1. Integrate advanced NLP models like GPT or LLaMA for generating detailed explanations of matches.
2. Expand scraping functionality to support dynamic rendering (e.g., Selenium).
3. Develop a web-based interface for user interaction.

## Contributors

- **Daniel Salame:** Developer and maintainer of the project.
