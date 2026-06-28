import os
# os.system("python -m spacy download en_core_web_sm")

import streamlit as st
import pdfplumber
import spacy
import nltk
import re
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# ============ DOWNLOAD NLTK DATA ============
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# ============ LOAD SPACY MODEL ============
@st.cache_resource
def load_nlp():
    return spacy.load('en_core_web_sm')

nlp = load_nlp()

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide"
)








# ============ TITLE ============
st.title("📄 Smart Resume Analyzer")
st.markdown("### AI Powered Resume Analysis & ATS Scoring")
st.markdown("---")

# ============ SIDEBAR ============
st.sidebar.title("ℹ️ About")
st.sidebar.info("""
Upload your resume to get:
- 📊 ATS Score
- 🛠️ Skills Extracted
- 📧 Contact Info
- 💼 Experience Details
- 🎓 Education Found
- 💡 Improvement Tips
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Built with:** spaCy + NLTK + Streamlit")

# ============ FILE UPLOAD ============
st.markdown("### 📤 Upload Your Resume")
uploaded_file = st.file_uploader(
    "Choose PDF Resume",
    type=['pdf']
)

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
else:
    st.info("👆 Please upload your resume in PDF format")







# ============ EXTRACT TEXT FROM PDF ============
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ============ SHOW EXTRACTED TEXT ============
if uploaded_file:
    st.markdown("---")
    
    # Extract text
    with st.spinner("📖 Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    if resume_text:
        st.success("✅ Resume text extracted successfully!")
        
        # Show raw text in expander
        with st.expander("📄 View Extracted Text"):
            st.text(resume_text)
    else:
        st.error("❌ Could not extract text from PDF!")







# ============ EXTRACT CONTACT INFO ============
def extract_contact_info(text):
    contact = {}

    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    contact['email'] = emails[0] if emails else "Not found"

    # Extract phone
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    contact['phone'] = phones[0] if phones else "Not found"

    # Extract LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin = re.findall(linkedin_pattern, text.lower())
    contact['linkedin'] = linkedin[0] if linkedin else "Not found"

    # Extract GitHub
    github_pattern = r'github\.com/[\w-]+'
    github = re.findall(github_pattern, text.lower())
    contact['github'] = github[0] if github else "Not found"

    return contact









# ============ SKILLS LIST ============
SKILLS_LIST = [
      # Programming Languages
      'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php',
      'swift', 'kotlin', 'golang', 'rust', 'scala', 'r', 'c',

      # Web Development
      'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
      'django', 'flask', 'fastapi', 'bootstrap', 'tailwind',
      'rest api', 'rest apis', 'graphql',

      # Database
      'mysql', 'mongodb', 'postgresql', 'sqlite', 'redis', 'firebase',
      'oracle', 'cassandra', 'dynamodb', 'mongoose', 'sql',

      # ML/AI
      'machine learning', 'deep learning', 'nlp', 'computer vision',
      'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'opencv',
      'pandas', 'numpy', 'matplotlib', 'seaborn', 'xgboost',
      'data preprocessing', 'eda', 'exploratory data analysis',
      'ann', 'cnn', 'rnn', 'lstm', 'gru',
      'transfer learning', 'transformers', 'bert', 'gpt',
      'random forest', 'decision tree', 'svm', 'knn',
      'neural network', 'natural language processing',

      # Cloud & DevOps
      'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
      'git', 'github', 'gitlab', 'linux', 'ci/cd',
      'vercel', 'netlify', 'heroku', 'render', 'hugging face',

      # Mobile
      'android', 'ios', 'react native', 'flutter',

      # Auth & Security
      'jwt', 'session', 'authentication', 'authorization',
      'oauth', 'bcrypt',

      # Other
      'microservices', 'agile', 'scrum',
      'figma', 'postman', 'jira', 'tableau', 'power bi'
]


# ============ SHOW CONTACT INFO ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### 📧 Contact Information")

    contact_info = extract_contact_info(resume_text)

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"📧 **Email:** {contact_info['email']}")
        st.info(f"📱 **Phone:** {contact_info['phone']}")

    with col2:
        st.info(f"💼 **LinkedIn:** {contact_info['linkedin']}")
        st.info(f"🐙 **GitHub:** {contact_info['github']}")




# ============ EXTRACT SKILLS ============
def extract_skills(text):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.append(skill.upper())

    return list(set(found_skills))






# # ============ EXTRACT PROJECTS ============
# def extract_projects(text):
#     projects = []
    
#     # Common project section headers
#     project_keywords = [
#         'project', 'projects', 'work', 'portfolio',
#         'built', 'developed', 'created', 'implemented'
#     ]
    
#     lines = text.split('\n')
#     project_section = False
#     current_project = []
    
#     for line in lines:
#         line = line.strip()
#         if not line:
#             continue
            
#         # Check if we're in projects section
#         if any(keyword in line.lower() for keyword in project_keywords):
#             project_section = True
            
#         if project_section and line:
#             current_project.append(line)
            
#         # Save project after collecting lines
#         if len(current_project) >= 3:
#             projects.append(' '.join(current_project))
#             current_project = []
    
    # return projects[:5]  # Return top 5 projects

# ============ EXTRACT PROJECT SKILLS ============
def extract_project_skills(text):
    project_skills = {
        'Machine Learning': [
            'xgboost', 'random forest', 'svm', 'knn',
            'scikit-learn', 'model', 'prediction', 'accuracy',
            'dataset', 'training', 'classification', 'regression'
        ],
        'Deep Learning': [
            'cnn', 'ann', 'rnn', 'lstm', 'neural network',
            'tensorflow', 'keras', 'pytorch', 'epoch',
            'transfer learning', 'vgg', 'resnet', 'bert'
        ],
        'Full Stack': [
            'react', 'nodejs', 'express', 'mongodb',
            'authentication', 'api', 'frontend', 'backend',
            'database', 'deployed', 'rest'
        ],
        'NLP': [
            'nlp', 'text', 'sentiment', 'classification',
            'bert', 'transformers', 'spacy', 'nltk',
            'language', 'corpus'
        ],
        'Computer Vision': [
            'image', 'opencv', 'detection', 'classification',
            'cnn', 'yolo', 'segmentation', 'recognition'
        ],
        'Data Science': [
            'pandas', 'numpy', 'matplotlib', 'seaborn',
            'analysis', 'visualization', 'eda', 'insight'
        ]
    }

    text_lower = text.lower()
    found_domains = {}

    for domain, keywords in project_skills.items():
        matches = sum(1 for k in keywords if k in text_lower)
        if matches > 0:
            found_domains[domain] = matches

    return dict(sorted(
        found_domains.items(),
        key=lambda x: x[1],
        reverse=True
    ))

# ============ SHOW PROJECTS ANALYSIS ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### 🚀 Project Domain Analysis")

    project_domains = extract_project_skills(resume_text)

    if project_domains:
        st.success(f"✅ Found {len(project_domains)} project domains!")

        for domain, score in project_domains.items():
            st.markdown(f"**{domain}**")
            st.progress(min(score * 10, 100))
            st.caption(f"Found {score} related keywords")
    else:
        st.warning("⚠️ No project domains detected!")







# ============ SHOW SKILLS ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### 🛠️ Skills Extracted")

    skills = extract_skills(resume_text)

    if skills:
        st.success(f"✅ Found {len(skills)} skills!")

        # Show skills as tags
        skills_html = ""
        for skill in skills:
            skills_html += f'<span style="background-color:#4e54c8; color:white; padding:5px 10px; border-radius:15px; margin:3px; display:inline-block; font-size:0.85rem">{skill}</span>'

        st.markdown(skills_html, unsafe_allow_html=True)

    else:
        st.warning("⚠️ No skills found!")










  # ============ CALCULATE ATS SCORE ============
def calculate_ats_score(text, skills):
    score = 0
    suggestions = []

    # Check email (10 points)
    if re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        score += 10
    else:
        suggestions.append("❌ Add your email address")

    # Check phone (10 points)
    if re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text):
        score += 10
    else:
        suggestions.append("❌ Add your phone number")

    # Check LinkedIn (5 points)
    if 'linkedin' in text.lower():
        score += 5
    else:
        suggestions.append("❌ Add your LinkedIn profile")

    # Check GitHub (5 points)
    if 'github' in text.lower():
        score += 5
    else:
        suggestions.append("❌ Add your GitHub profile")

    # Check skills (20 points)
    if len(skills) >= 10:
        score += 20
    elif len(skills) >= 5:
        score += 10
        suggestions.append("⚠️ Add more technical skills")
    else:
        score += 5
        suggestions.append("❌ Add more technical skills")

    # Check education (10 points)
    education_keywords = ['education', 'university', 'college', 'degree',
                         'bachelor', 'master', 'b.tech', 'm.tech', 'bsc', 'msc']
    if any(word in text.lower() for word in education_keywords):
        score += 10
    else:
        suggestions.append("❌ Add your education details")

    # Check experience (10 points)
    experience_keywords = ['experience', 'worked', 'internship',
                          'project', 'developed', 'built', 'created']
    if any(word in text.lower() for word in experience_keywords):
        score += 10
    else:
        suggestions.append("❌ Add work experience or projects")

    # Check summary/objective (10 points)
    summary_keywords = ['summary', 'objective', 'about', 'profile']
    if any(word in text.lower() for word in summary_keywords):
        score += 10
    else:
        suggestions.append("❌ Add a professional summary")

    # Check length (10 points)
    words = len(text.split())
    if words >= 300:
        score += 10
    else:
        suggestions.append("⚠️ Resume is too short, add more details")

    # Check certifications (10 points)
    cert_keywords = ['certification', 'certified', 'certificate', 'course']
    if any(word in text.lower() for word in cert_keywords):
        score += 10
    else:
        suggestions.append("⚠️ Add certifications if any")

    return score, suggestions

# ============ SHOW ATS SCORE ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### 📊 ATS Score")

    skills = extract_skills(resume_text)
    ats_score, suggestions = calculate_ats_score(resume_text, skills)

    # Score display
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ATS Score", f"{ats_score}/100")

    with col2:
        if ats_score >= 80:
            st.success("🏆 Excellent Resume!")
        elif ats_score >= 60:
            st.warning("👍 Good Resume!")
        elif ats_score >= 40:
            st.warning("😐 Average Resume!")
        else:
            st.error("😟 Needs Improvement!")

    with col3:
        st.metric("Skills Found", len(skills))

    # Progress bar
    st.progress(ats_score)

    # Suggestions
    if suggestions:
        st.markdown("### 💡 Improvement Suggestions")
        for suggestion in suggestions:
            st.markdown(suggestion)





  # ============ GENERATE WORD CLOUD ============
def generate_wordcloud(text):
    stop_words = set(stopwords.words('english'))
    
    # Clean text
    words = text.lower().split()
    words = [w for w in words if w.isalpha() and w not in stop_words]
    clean_text = ' '.join(words)
    
    # Generate wordcloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(clean_text)
    
    return wordcloud

# ============ SHOW WORD CLOUD ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### ☁️ Resume Word Cloud")

    with st.spinner("Generating word cloud..."):
        wordcloud = generate_wordcloud(resume_text)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)






  # ============ PREDICT JOB ROLE ============
def predict_job_role(skills, resume_text=""):
    skills_lower = [s.lower() for s in skills]
    text_lower = resume_text.lower()

    job_roles = {
        'Machine Learning Engineer': [
            'machine learning', 'deep learning', 'tensorflow',
            'pytorch', 'scikit-learn', 'nlp', 'python', 'keras',
            'xgboost', 'ann', 'cnn', 'rnn', 'lstm', 'gru',
            'transfer learning', 'transformers', 'data preprocessing',
            'eda', 'random forest', 'neural network', 'model',
            'prediction', 'accuracy', 'dataset', 'training'
        ],
        'Full Stack Developer': [
            'react', 'nodejs', 'express', 'mongodb', 'html',
            'css', 'javascript', 'rest api', 'rest apis',
            'jwt', 'authentication', 'mongoose', 'sql',
            'frontend', 'backend', 'deployed', 'api'
        ],
        'AI/Deep Learning Engineer': [
            'deep learning', 'ann', 'cnn', 'rnn', 'lstm', 'gru',
            'tensorflow', 'keras', 'pytorch', 'transfer learning',
            'transformers', 'bert', 'nlp', 'computer vision',
            'neural network', 'epoch', 'vgg', 'resnet'
        ],
        'Data Scientist': [
            'python', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'machine learning', 'scikit-learn', 'tableau', 'power bi',
            'eda', 'data preprocessing', 'xgboost', 'analysis',
            'visualization', 'insight', 'dataset'
        ],
        'Frontend Developer': [
            'html', 'css', 'javascript', 'react', 'angular',
            'vue', 'bootstrap', 'tailwind', 'typescript',
            'responsive', 'ui', 'ux'
        ],
        'Backend Developer': [
            'nodejs', 'express', 'django', 'flask', 'fastapi',
            'mysql', 'mongodb', 'postgresql', 'rest api',
            'jwt', 'authentication', 'mongoose', 'api'
        ],
        'DevOps Engineer': [
            'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'jenkins', 'linux', 'ci/cd', 'git', 'github',
            'deployment', 'pipeline', 'automation'
        ],
    }

    # Calculate match score
    role_scores = {}
    for role, keywords in job_roles.items():
        # Check both skills and full text
        skill_match = sum(1 for k in keywords if k in skills_lower)
        text_match = sum(1 for k in keywords if k in text_lower)
        
        # Combined score
        total = len(keywords)
        score = ((skill_match * 2 + text_match) / (total * 3)) * 100
        role_scores[role] = round(score, 1)

    sorted_roles = sorted(
        role_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_roles[:3]





# ============ SHOW JOB ROLE PREDICTION ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### 💼 Predicted Job Roles")

    skills = extract_skills(resume_text)
    predicted_roles = predict_job_role(skills, resume_text)

    if predicted_roles:
        for i, (role, score) in enumerate(predicted_roles):
            if i == 0:
                st.success(f"🏆 Best Match: **{role}** — {score}% match")
            else:
                st.info(f"#{i+1} **{role}** — {score}% match")

            st.progress(int(score))
    else:
        st.warning("⚠️ Could not predict job role!")






  # ============ RESUME SUMMARY ============
if uploaded_file and resume_text:
    st.markdown("---")
    st.markdown("### 📋 Resume Summary")

    skills = extract_skills(resume_text)
    ats_score, suggestions = calculate_ats_score(resume_text, skills)
    contact_info = extract_contact_info(resume_text)
    predicted_roles = predict_job_role(skills, resume_text)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("ATS Score", f"{ats_score}/100")

    with col2:
        st.metric("Skills Found", len(skills))

    with col3:
        st.metric("Best Role Match", predicted_roles[0][0] if predicted_roles else "N/A")

    with col4:
        words = len(resume_text.split())
        st.metric("Word Count", words)

    # Overall feedback
    st.markdown("---")
    st.markdown("### 🎯 Overall Feedback")

    if ats_score >= 80:
        st.success("""
        🏆 **Excellent Resume!**
        Your resume is well optimized for ATS systems.
        Keep applying with confidence!
        """)
    elif ats_score >= 60:
        st.warning("""
        👍 **Good Resume!**
        Your resume is decent but needs some improvements.
        Check suggestions above!
        """)
    elif ats_score >= 40:
        st.warning("""
        😐 **Average Resume!**
        Your resume needs significant improvements.
        Follow all suggestions above!
        """)
    else:
        st.error("""
        😟 **Needs Major Improvement!**
        Your resume is missing many important sections.
        Please follow all suggestions above!
        """)

    # Download suggestions as text
    st.markdown("---")
    suggestions_text = "\n".join(suggestions)
    st.download_button(
        label="📥 Download Improvement Suggestions",
        data=suggestions_text,
        file_name="resume_suggestions.txt",
        mime="text/plain"
    )