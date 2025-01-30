import os
import re
import spacy
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NLP model
nlp = spacy.load("en_core_web_trf")

# Job Fields Dataset (you can modify this or load from a CSV file)
job_fields = {
    "Data Analyst": {
        "skills": ["Python", "SQL", "Pandas", "NumPy", "Machine Learning", "Data Visualization", "Power BI", "Tableau", "Excel", "Statistics", "Big Data", "ETL", "Data Warehousing"],
        "description": "Looking for a Data Analyst with expertise in Python, SQL, and data visualization tools."
    },
    "DevOps Engineer": {
        "skills": ["Linux", "Git", "GitHub", "Jenkins", "Docker", "Kubernetes", "Terraform", "Ansible", "CI/CD", "AWS", "GCP", "Azure", "Monitoring", "Infrastructure as Code", "Shell Scripting", "Networking", "Cloud Security", "Prometheus", "Grafana"],
        "description": "Seeking a DevOps Engineer with strong expertise in Kubernetes, CI/CD, and cloud security."
    },
    "Cloud Engineer": {
        "skills": ["AWS", "Azure", "Google Cloud Platform", "Terraform", "CloudFormation", "Serverless Computing", "IAM", "Networking", "Kubernetes", "CI/CD", "Cloud Security", "Observability", "Load Balancing", "Auto Scaling", "Cloud Storage", "Cloud Databases"],
        "description": "Looking for a Cloud Engineer with experience in AWS, Kubernetes, and Terraform."
    },
    "Cybersecurity Engineer": {
        "skills": ["Network Security", "Penetration Testing", "SIEM", "Incident Response", "SOC Operations", "Threat Hunting", "Encryption", "Firewall Management", "Ethical Hacking", "Malware Analysis", "Forensics", "Risk Assessment", "Zero Trust Security", "Cloud Security", "IAM"],
        "description": "Seeking a Cybersecurity Engineer with expertise in penetration testing, incident response, and threat hunting."
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Angular", "Node.js", "Express.js", "Django", "Flask", "REST API", "GraphQL", "TypeScript", "Next.js", "Tailwind CSS", "Bootstrap", "MongoDB", "PostgreSQL", "Firebase"],
        "description": "Hiring a Web Developer with experience in JavaScript frameworks and full-stack development."
    },
    "Mobile App Developer": {
        "skills": ["Flutter", "React Native", "Swift", "Kotlin", "Java", "Dart", "Firebase", "Jetpack Compose", "Xamarin", "iOS Development", "Android Development", "Mobile UI/UX", "Push Notifications", "App Store Optimization"],
        "description": "Looking for a Mobile App Developer with expertise in Flutter and React Native."
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "TensorFlow", "PyTorch", "Scikit-Learn", "Deep Learning", "NLP", "Computer Vision", "Data Preprocessing", "Feature Engineering", "Keras", "CNN", "RNN", "Transformers", "AI Ethics", "MLOps"],
        "description": "Seeking a Machine Learning Engineer with experience in deep learning, NLP, and AI ethics."
    },
    "Blockchain Developer": {
        "skills": ["Ethereum", "Solidity", "Smart Contracts", "Hyperledger", "NFTs", "Cryptography", "DeFi", "DApps", "Blockchain Security", "Consensus Mechanisms"],
        "description": "Hiring a Blockchain Developer with strong knowledge of Solidity and smart contract development."
    },
    "Database Administrator": {
        "skills": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "OracleDB", "Cassandra", "Redis", "Elasticsearch", "DynamoDB", "Data Modeling", "Normalization", "ACID Transactions", "NoSQL", "Database Administration"],
        "description": "Looking for a Database Administrator with expertise in SQL and NoSQL databases."
    },
    "UI/UX Designer": {
        "skills": ["Figma", "Adobe XD", "Sketch", "Wireframing", "Prototyping", "User Research", "Typography", "Color Theory", "Usability Testing", "Interaction Design", "Responsive Design", "Information Architecture", "Design Systems"],
        "description": "Seeking a UI/UX Designer with experience in wireframing, prototyping, and user research."
    },
    "Software Engineer": {
        "skills": ["Python", "Java", "C++", "C#", "JavaScript", "Go", "Rust", "Swift", "Version Control", "Algorithms", "Data Structures", "Object-Oriented Programming", "Microservices", "Design Patterns"],
        "description": "Hiring a Software Engineer with experience in multiple programming languages and OOP principles."
    },
    "Embedded Systems Engineer": {
        "skills": ["Embedded C", "Arduino", "Raspberry Pi", "Microcontrollers", "Sensors", "RTOS", "IoT Security", "MQTT", "LoRaWAN", "Zigbee", "Edge Computing", "IoT Protocols", "Industrial IoT"],
        "description": "Looking for an Embedded Systems Engineer with experience in IoT and microcontrollers."
    },
    "Game Developer": {
        "skills": ["Unity", "Unreal Engine", "C#", "C++", "Game Physics", "3D Modeling", "Animation", "VR/AR", "Game AI", "Shader Programming", "Multiplayer Networking"],
        "description": "Seeking a Game Developer with experience in Unity and Unreal Engine."
    },
    "System Administrator": {
        "skills": ["Linux", "Windows Server", "Networking", "Shell Scripting", "Active Directory", "DNS", "Bash", "PowerShell", "Virtualization", "Backup & Recovery", "Monitoring & Logging", "Load Balancing"],
        "description": "Hiring a System Administrator with strong Linux and Windows Server expertise."
    },
    "Digital Marketer": {
        "skills": ["SEO", "Content Marketing", "Google Ads", "Social Media Marketing", "Email Marketing", "Affiliate Marketing", "Analytics", "Conversion Optimization", "Facebook Ads", "LinkedIn Ads", "PPC"],
        "description": "Looking for a Digital Marketer with expertise in SEO and social media advertising."
    },
    "AI & Robotics Engineer": {
        "skills": ["ROS", "Computer Vision", "Reinforcement Learning", "Robotic Arms", "SLAM", "Deep Learning for Robotics", "Sensor Fusion", "Path Planning"],
        "description": "Seeking an AI & Robotics Engineer with experience in deep learning for robotics."
    },
    "Data Scientist": {
        "skills": ["Python", "R", "SQL", "Big Data", "Data Wrangling", "Feature Engineering", "Time Series Analysis", "Data Ethics", "MLOps", "Predictive Modeling", "EDA", "Data Governance"],
        "description": "Hiring a Data Scientist with expertise in machine learning and predictive modeling."
    },
    "Network Engineer": {
        "skills": ["CCNA", "Firewalls", "TCP/IP", "Routing & Switching", "VPN", "BGP", "DNS", "DHCP", "Load Balancing", "Wi-Fi Security", "LAN/WAN", "Packet Analysis", "Subnetting"],
        "description": "Looking for a Network Engineer with experience in CCNA, routing, and switching."
    },
    "IT Project Manager": {
        "skills": ["Agile", "Scrum", "Kanban", "JIRA", "Trello", "Risk Management", "Stakeholder Communication", "Waterfall", "PRINCE2", "PMP", "Budgeting", "Scope Management"],
        "description": "Seeking an IT Project Manager with expertise in Agile and Scrum methodologies."
    }
}


# Check if file is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Extract Name, Email, Phone, Skills, Experience, Education from resume text
def extract_info(text):
    doc = nlp(text)

    # Extract Name using Named Entity Recognition (NER)
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract Email
    email = re.findall(r"[\w.+-]+@[\w-]+\.[a-z]+", text)

    # Extract Phone Number
    phone = re.findall(r"\+?\d[\d -]{8,}\d", text)

    # Extract Skills (Using predefined skills set)
    predefined_skills = {"Python", "Machine Learning", "NLP", "Data Science", "Docker", "Kubernetes", "AWS", "React",
                         "JavaScript", "SQL"}
    skills = [token.text for token in doc if token.text in predefined_skills]

    # Extract Years of Experience
    experience = re.findall(r"(\d+\s+years?)", text)
    experience = experience[0] if experience else "Not Found"

    # Extract Education (Look for keywords like 'University', 'Bachelor', 'Master')
    education = ""
    for line in text.split("\n"):
        if any(word in line.lower() for word in ["university", "bachelor", "master", "degree"]):
            education = line
            break

    return {
        "Name": name if name else "Unknown",
        "Email": email[0] if email else "Not Found",
        "Phone": phone[0] if phone else "Not Found",
        "Skills": list(set(skills)),  # Unique skills
        "Experience": experience,
        "Education": education if education else "Not Found"
    }

# Exact Keyword Matching
def exact_keyword_match(resume_skills, job_required_skills):
    return set(resume_skills).intersection(set(job_required_skills))

# Semantic Similarity Matching using TF-IDF and Cosine Similarity
def semantic_similarity(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return cosine_sim[0][0]

# Rank the resume based on the selected job field
def rank_resume(resume_data, job_field):
    job_info = job_fields.get(job_field, {})

    # Exact keyword matching for skills
    matching_skills = exact_keyword_match(resume_data["Skills"], job_info["skills"])
    skills_match = (len(matching_skills) / len(job_info["skills"])) * 100

    # Semantic similarity for skills and job description
    skills_similarity_score = semantic_similarity(" ".join(resume_data["Skills"]), job_info["description"])

    # Experience Match (we will assume some basic logic for now)
    experience_match = 80 if "years" in resume_data["Experience"] else 0

    # Education Match (assuming basic check for relevant keywords)
    education_match = 100 if "University" in resume_data["Education"] else 0

    # Final ranking score
    total_score = (skills_match * 0.5) + (experience_match * 0.3) + (education_match * 0.2)
    return total_score, skills_match, experience_match, education_match, matching_skills, skills_similarity_score



@app.route("/", methods=["GET", "POST"])
def upload_resume():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        job_field = request.form["job_field"]  # Get selected job field

        if file.filename == "":
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif filename.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                return "Unsupported file format"

            resume_data = extract_info(text)

            # Rank the resume based on the selected job field
            score, skills_match, experience_match, education_match, matching_skills, similarity_score = rank_resume(resume_data, job_field)

            return render_template("result.html", resume=resume_data, job_field=job_field, matching_skills=matching_skills,
                                   score=score, skills_match=skills_match, experience_match=experience_match,
                                   education_match=education_match, similarity_score=similarity_score)

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
