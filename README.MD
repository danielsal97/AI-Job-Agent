# AI Job Agent
## Table of Contents
```sh
export TOKENIZERS_PARALLELISM=false
```

- [Introduction](#introduction)
- [Features](#features)
- [Project File Structure](#project-file-structure)
- [Setup Instructions](#setup-instructions)
	- [Clone the Repository](#clone-the-repository)
	- [Prerequisites](#prerequisites)
		- [Option 1: Using Virtual Environment](#option-1-using-virtual-environment)
		- [Option 2: Using Installer Script](#option-2-using-installer-script)
	- [Environment Configuration](#environment-configuration)
	- [Run the Project](#run-the-project)
- [Configuration](#configuration)
	- [CSS Selectors for Job Scraping](#css-selectors-for-job-scraping)
- [Code Structure](#code-structure)
	- [Main Files](#main-files)
	- [Supporting Files](#supporting-files)
- [Sample Output](#sample-output)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)
This project is a Python-based tool that matches job descriptions with resumes by calculating similarity scores using embeddings and natural language processing techniques. It includes functionalities for scraping job postings, generating embeddings, and evaluating similarity metrics to provide insights into how well a resume aligns with job opportunities.

## Features

- **Job Scraping:**
	- Uses CSS selectors to scrape job listings from websites like NVIDIA.
	- Extracts job titles, descriptions, and other relevant details.
- **Resume Processing:**
	- Processes resumes for embedding generation using SentenceTransformer models.
- **Job Processing:**
	- Generates embeddings for job descriptions and compares them with the resume.
- **Similarity Scoring:**
	- Calculates similarity scores using cosine similarity and dot product.
	- Provides metrics such as Job-to-Resume Match, Resume-to-Job Match, Semantic Match, Contextual Match, and Overall Score.

## Project File Structure

Here is an overview of the project files:

```
AI_Job_Agent/
├── __pycache__/                # Auto-generated Python cache files
├── venv/                       # Virtual environment (not included in version control)
├── .gitignore                  # Git configuration to ignore specific files
├── config.py                   # Configuration for settings (e.g., selectors, paths)
├── CV_processing.py            # Resume processing and embedding generation
├── Daniel_Salame_CV.txt        # Sample resume file
├── hybrid_job_scraper.py       # Hybrid job scraper implementation
├── installer.py                # Installer script for dependencies
├── Job_processing.py           # Job posting processing and embedding generation
├── job_scraper_context.py      # Handles context and orchestration for job scraping
├── main.py                     # Entry point for running the application
├── README.MD                   # Documentation for the project
├── requirements.txt            # Dependencies required for the project
```

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

1. Run the `main.py` file to start the process:

	```sh
	python main.py
	```

2. The script will:
	- Scrape job postings using CSS selectors.
	- Generate embeddings for
