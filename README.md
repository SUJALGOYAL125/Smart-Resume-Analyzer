# 📄 Smart Resume Analyzer

> AI-powered resume analyzer that extracts skills, scores ATS compatibility and predicts job roles from PDF resumes using NLP

🌐 **Live Demo:** [Click here](https://sujalgoyal125-smart-resume-analyzer-app-dnxtfb.streamlit.app/)
📁 **GitHub:** [Repository](https://github.com/SUJALGOYAL125/Smart-Resume-Analyzer)

---

## ✨ Features

- 📊 ATS Score (0-100) with improvement suggestions
- 🛠️ Skills Extraction (50+ technical skills)
- 📧 Contact Info Extraction (email, phone, LinkedIn, GitHub)
- 💼 Job Role Prediction (ML Engineer, Full Stack, Data Scientist etc.)
- 🚀 Project Domain Analysis
- ☁️ Resume Word Cloud
- 📥 Download Improvement Suggestions

---

## 🤖 How It Works

Upload PDF Resume

↓

Extract Text (pdfplumber)

↓

NLP Processing (spaCy + NLTK)

↓

Skills & Contact Extraction

↓

ATS Scoring + Job Role Prediction

↓

Visual Results + Suggestions

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web interface |
| spaCy | NLP processing |
| NLTK | Text analysis |
| pdfplumber | PDF text extraction |
| WordCloud | Resume visualization |
| Scikit-learn | ML utilities |
| Matplotlib | Charts |

---

## 🚀 Run Locally

```bash
# Clone repo
git clone https://github.com/SUJALGOYAL125/Smart-Resume-Analyzer.git
cd Smart-Resume-Analyzer

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

---

## 📊 ATS Scoring Criteria

| Criteria | Points |
|---|---|
| Email present | 10 |
| Phone present | 10 |
| LinkedIn present | 5 |
| GitHub present | 5 |
| Skills (10+) | 20 |
| Education section | 10 |
| Experience/Projects | 10 |
| Summary/Objective | 10 |
| Word count 300+ | 10 |
| Certifications | 10 |
| **Total** | **100** |

---

## ⚠️ Disclaimer

This tool is for educational purposes only.
ATS scores are approximate and may vary from actual ATS systems.

---

## 👨‍💻 Author

**Sujal Goyal**
- GitHub: [@SUJALGOYAL125](https://github.com/SUJALGOYAL125)
- LinkedIn: [sujalgoyal](https://linkedin.com/in/sujalgoyal)
