# AI-Powered Resume and Job Matching Tool

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Feature Progress](#feature-progress)
   - [Current Focus](#current-focus)
4. [Setup Instructions](#setup-instructions)
   - [Clone the Repository](#clone-the-repository)
   - [Prerequisites](#prerequisites)
   - [Environment Configuration](#environment-configuration)
   - [Run the Project](#run-the-project)
5. [Future Improvements](#future-improvements)
6. [Contributors](#contributors)
7. [License](#license)

---

## Project Overview

The **AI-Powered Resume and Job Matching Tool** leverages state-of-the-art embeddings and similarity scoring techniques to analyze and compare job descriptions with resumes. By utilizing advanced natural language processing (NLP), it provides actionable insights into which jobs are the best matches for a given resume. The tool includes functionality for:
- Scraping job postings from websites.
- Processing resumes and job descriptions into embeddings.
- Scoring the similarity between job descriptions and resumes.
- **Storing data in PostgreSQL** using unique UUIDs to ensure efficient and conflict-free record management.

---

## Features

### Key Features
- **Job Scraping**: Extract job descriptions, titles, and other details from websites.
- **Resume Processing**: Convert resumes into embeddings using advanced NLP models.
- **Job Processing**: Generate embeddings for job descriptions to enable comparisons.
- **Similarity Scoring**: Compute metrics such as cosine similarity for matching resumes with jobs.

---

## Feature Progress

| Feature               | Stage          | Description                                                                                 |
|-----------------------|----------------|---------------------------------------------------------------------------------------------|
| **Job Scraping**      | In Progress    | Supports scraping for NVIDIA jobs. Optimizations are ongoing to add synchronous scraping for faster performance and support additional websites. |
| **Data Handling**     | Demo        | To implement clustering, deduplication, and efficient storage in PostgreSQL with UUIDs for unique identification. |
| **Resume Processing** | Testing        | Converts resumes into embeddings using SentenceTransformer models. Needs verification to ensure embeddings are accurate and consistent. |
| **Job Processing**    | Testing        | Processes job descriptions into embeddings and handles comparisons. Requires further validation of its effectiveness. |
| **Similarity Scoring**| Demo           | Basic similarity scoring (e.g., cosine similarity) is functional, but advanced metrics like contextual matching need further development. |

---

### Current Focus

1. **Job Scraping**:
   - **Synchronous Optimization**:
     - Introduce synchronous scraping to reduce processing time and handle multiple requests in parallel.
     - Enhance reliability by implementing retry mechanisms for failed requests.
   - **Expanding Website Support**:
     - Extend the scraping functionality to include additional websites beyond NVIDIA.
     - Allow user configuration of CSS selectors for flexibility.

2. **Testing and Validation**:
   - **Resume Processing**:
     - Verify the accuracy and consistency of embeddings generated from resumes.
   - **Job Processing**:
     - Evaluate whether the embeddings from job descriptions are processed correctly and compared effectively.

3. **Data Handling**:
   - Implement efficient data clustering and deduplication methods to clean and organize scraped data.
   - Store cleaned data in PostgreSQL using UUIDs to ensure unique identification and easy retrieval.

---
## Setup Instructions

### Clone the Repository

Clone the project repository and navigate to the project directory:

```sh
git clone https://github.com/danielsal97/AI-Job-Agent.git
cd AI_Job_Agent
```

### Prerequisites

## Prerequisites
1. Install Python 3.7 or higher.
2. Install PostgreSQL:
   - Linux: `sudo apt install postgresql`
   - macOS: Use `brew install postgresql`
   - Windows: Download from (https://www.postgresql.org/download/)

3. Configure a PostgreSQL database for the project:
   - Create a database: `CREATE DATABASE mydb;`
   - Set up a user with access: `CREATE USER myuser WITH PASSWORD 'mypassword';`

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


	The command export TOKENIZERS_PARALLELISM=false is used to suppress warnings related to the parallel execution of tokenizers in libraries such as Hugging Face’s Transformers.

Context:
	•	Tokenizers in NLP libraries may use multi-threading to improve performance.
	•	In certain environments (e.g., during debugging, or when multiple instances of the tokenizer are used simultaneously), this parallelism can cause warnings or lead to issues like resource contention.

Purpose:

Setting TOKENIZERS_PARALLELISM=false disables this parallelism, which:
	1.	Prevents Warnings: Suppresses the frequent warning messages like:

Token indices sequence length is longer than the specified maximum sequence length for this model.


	2.	Improves Stability: Reduces potential conflicts or performance issues caused by multi-threaded operations in environments that aren’t optimized for them.

Usage:
	•	Add the command to your shell environment before running the script, or set it programmatically in your Python code:

import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'



This ensures the script runs without cluttering the output with unnecessary warnings, leading to cleaner logs and a smoother debugging experience.

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




## Future Improvements

1. Integrate advanced NLP models like GPT or LLaMA for generating detailed explanations of matches.
2. Develop a web-based interface for user interaction.

## Contributors

- **Daniel Salame:** Developer and maintainer of the project.
