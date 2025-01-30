Resume Ranking System
Overview
This project is a Resume Ranking System that helps match resumes to specific job fields using Natural Language Processing (NLP) and Machine Learning (ML) techniques. The system extracts relevant information from resumes (in PDF and DOCX formats), such as skills, experience, and education, and ranks the resume based on its relevance to the selected job field. The project uses Flask for web development, spaCy for NLP tasks, and scikit-learn for text similarity matching.

Features
Upload resumes in PDF and DOCX formats.
Extract key information from resumes such as name, email, phone number, skills, experience, and education.
Match resumes with predefined job fields (e.g., Data Scientist, Software Engineer, DevOps Engineer).
Rank resumes based on:
Exact keyword matching for skills.
Semantic similarity between resume text and job descriptions using TF-IDF and cosine similarity.
Experience and education relevance.
View a detailed report with ranking and matching skills.
Libraries and Technologies Used
Flask: Web framework for creating the web application and handling file uploads.
spaCy: Natural Language Processing (NLP) library for extracting key entities (name, skills, etc.).
scikit-learn: Used for text vectorization (TF-IDF) and calculating cosine similarity.
pdfminer.six: For extracting text from PDF files.
python-docx: For extracting text from DOCX files.
Werkzeug: For handling secure file uploads.
Regular Expressions (Regex): For extracting structured information (email, phone number, experience) from resumes.
Installation
Prerequisites
Make sure you have Python 3 installed. Then, create a virtual environment (optional but recommended):

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
Step 1: Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/resume-ranking-system.git
cd resume-ranking-system
Step 2: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Create a requirements.txt file in the root of your project with the following contents:

Copy
Edit
Flask
Werkzeug
pdfminer.six
python-docx
spacy
scikit-learn
numpy
Step 3: Install the SpaCy Model
Run the following command to download the necessary spaCy model for NER (Named Entity Recognition):

bash
Copy
Edit
python -m spacy download en_core_web_trf
Step 4: Set Up Uploads Folder
Ensure the uploads folder exists in the root of your project to store uploaded resume files.

bash
Copy
Edit
mkdir uploads
Running the Application
Step 1: Start the Flask Application
In the project directory, run:

bash
Copy
Edit
python app.py
This will start the web server locally.

Step 2: Open the Application in Your Browser
Visit http://127.0.0.1:5000/ to use the Resume Ranking System. You can upload a resume file and select a job field to get a detailed ranking.

Usage
Upload a PDF or DOCX resume.
Select a job field (e.g., Data Scientist, Software Engineer, DevOps Engineer).
The system will process the resume, extract key information, and rank it based on its relevance to the selected job field.
View the score and the matching skills along with details about the experience and education match.
Project Structure
graphql
Copy
Edit
resume-ranking-system/
│
├── app.py                # Main Flask application
├── requirements.txt      # Project dependencies
├── uploads/              # Folder for storing uploaded resume files
├── templates/            # HTML templates for rendering
│   ├── result.html       # Template to display resume ranking results
│   └── upload.html       # Template for uploading resume files
├── static/               # Static assets (CSS, JS, images)
├── README.md             # Project README
└── requirements.txt      # List of Python dependencies
Contributing
If you'd like to contribute to this project, feel free to fork it and submit a pull request. You can also open issues if you encounter any bugs or have feature suggestions.
