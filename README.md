# 🚀 JOBMATCH: EDU2JOB
### AI-Powered Career Prediction System

JOBMATCH: EDU2JOB is a Machine Learning based career recommendation system that predicts the most suitable job role based on a user's educational background.

The system analyzes **Degree, Specialization, and CGPA** to predict career paths and provides **confidence scores and top job suggestions**.

The application is built using **Python, Streamlit, Machine Learning, and SQLite**, providing an interactive dashboard for career guidance.

---

# 📌 Project Overview

Many students struggle to decide the right career path based on their education.

This project solves that problem by building an **AI-powered system that maps academic details to suitable job roles**.

The system combines:
- Machine Learning
- Web Application Development
- Database Management
- Interactive Data Visualization

---

# ✨ Features

## 🔐 Authentication System
- User Registration
- Secure Login
- Password strength validation
- Password hashing
- Logout functionality

---

## 👤 User Profile
Users can manage their personal and academic information.

Profile includes:
- Full Name
- Role (Student / Job Seeker / Professional)
- Field of Interest
- Skills
- Profile completion indicator

---

## 🎯 Career Prediction
The system predicts job roles based on education details.

### Input
- Degree
- Specialization
- CGPA

### Output
- Predicted Job Role
- Confidence Score
- Top 3 Career Suggestions

---

## 📜 Prediction History
Every prediction is saved and displayed in the history section.

History includes:
- Degree
- Specialization
- CGPA
- Predicted Role
- Confidence Score
- Date and Time

---

## 📄 Resume Upload
Users can upload their resumes.

Features:
- Resume file upload
- Secure storage
- Linked to user account

---

## 📊 Dashboard
The application provides a modern dashboard including:

- Welcome section
- Profile card
- Quick action buttons
- Career insights
- Prediction summary
- Job distribution charts

---

# 🧠 Machine Learning Model

### Algorithm Used
Random Forest Classifier

### Why Random Forest?

- Handles categorical features well
- High prediction accuracy
- Reduces overfitting
- Suitable for classification tasks

---

### Machine Learning Workflow

Data Collection  
→ Data Preprocessing  
→ Feature Encoding  
→ Model Training  
→ Model Evaluation  
→ Model Pipeline Creation  
→ Model Saving (.pkl)

---

# 📁 Dataset

The dataset maps academic qualifications to job roles.

### Features
- Degree
- Specialization
- CGPA

### Target
- JobRole

### Dataset Characteristics
- Balanced job role distribution
- CGPA range from 6.5 to 9.0
- Multiple educational backgrounds

---

# 🏗 System Architecture

User Interface (Streamlit)  
↓  
Authentication System  
↓  
User Dashboard & Profile  
↓  
Machine Learning Prediction Engine  
↓  
SQLite Database

---

# 🛠 Technologies Used

| Category | Technology |
|--------|-----------|
| Programming Language | Python |
| Web Framework | Streamlit |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Database | SQLite |
| Model Storage | Joblib |

---

# 🗄 Database Design

## Users Table

| Column | Description |
|------|-------------|
| id | Unique user ID |
| email | User email |
| username | Username |
| password | Hashed password |

---

## Profiles Table

| Column | Description |
|------|-------------|
| user_id | Linked user ID |
| full_name | User name |
| role | User role |
| field | Field of interest |
| skills | User skills |
| profile_complete | Profile completion percentage |

---

## Predictions Table

| Column | Description |
|------|-------------|
| id | Prediction ID |
| user_id | Linked user |
| degree | User degree |
| specialization | User specialization |
| cgpa | CGPA |
| predicted_role | Predicted job |
| confidence | Confidence score |
| created_at | Prediction timestamp |

---

# 📂 Project Structure

```
JOBMATCH-EDU2JOB
│
├── streamlit_app.py
├── database.py
├── model_training.py
│
├── model_pipeline.pkl
├── model.pkl
│
├── degree_encoder.pkl
├── specialization_encoder.pkl
├── jobrole_encoder.pkl
│
├── job_dataset.csv
├── requirements.txt
├── README.md
│
├── presentation
│   └── JOBMATCH_EDU2JOB_Presentation.pptx
│
├── report
│   └── project_report.pdf
│
└── screenshots
```

---

# ▶️ How to Run the Project

## 1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/JOBMATCH-EDU2JOB.git
```

---

## 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 3️⃣ Run the Application

```
streamlit run streamlit_app.py
```

---

## Screenshots
## Landing Page
<img width="1919" height="869" alt="Screenshot 2026-03-09 171530" src="https://github.com/user-attachments/assets/edbeefa4-b31b-42c5-b545-612258419f6b" />
## Register Page
<img width="1919" height="863" alt="Screenshot 2026-03-09 171550" src="https://github.com/user-attachments/assets/5d4bfbb3-fb09-4947-aeac-0b28fbaee1ea" />
## Login Page
<img width="1919" height="860" alt="Screenshot 2026-03-09 171612" src="https://github.com/user-attachments/assets/98f07176-4e81-4a7b-8ef2-608e19715105" />
## Dashboard
<img width="1919" height="866" alt="Screenshot 2026-03-09 171644" src="https://github.com/user-attachments/assets/c81dfa7c-34ce-4459-9c03-e7e9d3285327" />
## Prediction Page
<img width="1919" height="863" alt="Screenshot 2026-03-09 171713" src="https://github.com/user-attachments/assets/ca8823fd-4c50-47cc-a857-a36bf54f71d7" />
## Prediction Result
<img width="953" height="502" alt="Screenshot 2026-03-09 171746" src="https://github.com/user-attachments/assets/1e547700-af17-43d0-85e2-08e3b79f12b2" />
## Prediction History
<img width="1774" height="842" alt="Screenshot 2026-03-09 171811" src="https://github.com/user-attachments/assets/cadbf791-06b2-425c-afdf-5f54bed46dde" />
## Profile Page
<img width="1186" height="658" alt="Screenshot 2026-03-09 171852" src="https://github.com/user-attachments/assets/c9b21c31-2ec9-418f-964a-acf5704af378" />

---
# 🚀 Future Enhancements

### Resume Skill Extraction
Use Natural Language Processing (NLP) to automatically extract skills from uploaded resumes.

### Resume-Based Job Prediction
Predict job roles directly from resume content.

### Skill Gap Analysis
Suggest missing skills required for predicted job roles.

### Course Recommendations
Recommend courses based on predicted career paths.

### Job Portal Integration
Fetch real-time job listings from job APIs.

---

# 🎓 Author

**Sonali Singh**  
B.Tech Computer Science  
Sagar Institute of Research & Technology, Bhopal

---

# 📜 License

This project is developed for **educational and academic purposes**.