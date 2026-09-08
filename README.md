# 📄 Smart Resume Analyzer

AI-powered resume analyzer that extracts skills, scores ATS compatibility, and predicts job roles from PDF resumes using NLP.

**🌐 Live Demo:** [Click here](https://sujalgoyal125-smart-resume-analyzer-app-dnxtfb.streamlit.app/)
**📁 GitHub:** [Repository](https://github.com/SUJALGOYAL125/Smart-Resume-Analyzer)

---

## ✨ Features

- 📊 **ATS Score** (0-100) with improvement suggestions
- 🛠️ **Skills Extraction** (50+ technical skills, with semantic matching to catch synonyms and variant phrasing — e.g., "ML" is recognized as "Machine Learning")
- 📧 **Contact Info Extraction** (email, phone, LinkedIn, GitHub)
- 💼 **Job Role Prediction** (ML Engineer, Full Stack, Data Scientist, etc.)
- 🚀 **Project Domain Analysis**
- ☁️ **Resume Word Cloud**
- 📥 **Download Improvement Suggestions**

---

## 🤖 How It Works

```
Upload PDF Resume
        ↓
Extract Text (pdfplumber)
        ↓
NLP Processing (spaCy + NLTK)
        ↓
Skill Matching — exact keyword match first,
then embedding-based semantic similarity
(sentence-transformers) for anything missed
        ↓
Contact Extraction
        ↓
ATS Scoring + Job Role Prediction
        ↓
Visual Results + Suggestions
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web interface |
| spaCy | NLP processing |
| NLTK | Text analysis |
| pdfplumber | PDF text extraction |
| sentence-transformers | Semantic skill matching (catches synonyms exact keyword matching misses) |
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

## 🔍 Known Limitations

Being upfront about how this actually works under the hood:

- **ATS scoring is rule-based**, not a trained ML classifier — it checks for the presence of specific sections and keywords rather than learning from real ATS behavior. Scores are directional, not a guarantee of how any specific company's actual ATS system would score the same resume.
- **Job role prediction uses weighted keyword overlap**, not a trained classification model — despite `scikit-learn` being a listed dependency, the current role-matching logic is rule-based rather than model-based.
- **Semantic skill matching adds processing time** compared to pure keyword matching, since it runs a local embedding model (`all-MiniLM-L6-v2`) as a second pass — the tradeoff is worth it for catching real synonyms, but analysis takes a second or two longer than before.
- **The similarity threshold for semantic matching is fixed** (not adaptive per-skill), so it's tuned to work well generally but may occasionally miss a very loosely-phrased skill mention or flag a borderline false positive.

## 💡 Possible Future Improvements

- Fine-tune or replace the rule-based ATS scorer with a model trained on real resume/outcome data
- Add a genuinely trained classifier for job-role prediction instead of keyword-overlap scoring
- Support additional file formats beyond PDF (e.g., DOCX)

---

## ⚠️ Disclaimer

This tool is for educational purposes only. ATS scores are approximate and may vary from actual ATS systems.

---

## 👨‍💻 Author

**Sujal Goyal**
GitHub: [@SUJALGOYAL125](https://github.com/SUJALGOYAL125)
LinkedIn: [sujalgoyal](https://linkedin.com/in/sujalgoyal)
