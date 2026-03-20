import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import re
import email
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from database import*
create_tables()  # Ensure DB tables are created on app start
# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="JOBMATCH: EDU2JOB",
    page_icon="🚀",
    layout="wide"
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

# -------- AUTHENTICATION --------
if "users_db" not in st.session_state:
    st.session_state.users_db = {}   # optional in-memory

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None   # username

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# -------- USER DATA --------
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# -------------------------------------------------
# GLOBAL CSS
# -------------------------------------------------
st.markdown("""
<style>
header[data-testid="stHeader"] {display:none;}
.block-container {padding-top:0rem !important;}

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
    font-family: 'Inter', sans-serif;
}

            /* ================= NAVBAR ================= */

.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 75px;
    background: linear-gradient(90deg,#0b1120,#111827);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 80px;
    z-index: 999999;
    border-bottom: 3px solid rgba(99,102,241,0.5);
    box-shadow: 0 10px 40px rgba(0,0,0,0.7);
}

.navbar::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
}

.logo {
    font-size: 22px;
    font-weight: 700;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 35px;
}

.nav-link {
    color: #cbd5e1;
    text-decoration: none;
    font-weight: 500;
    transition: 0.3s;
}

.nav-link:hover {
    color: white;
}

.nav-btn {
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    padding: 8px 22px;
    border-radius: 30px;
    font-weight: 600;
    color: white;
    text-decoration: none;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4);
}

/* Push content below navbar */
.page-content {
    margin-top: 90px;
    padding: 0 80px;
}
/* ================= HERO ================= */

.hero-title {
    font-size: 64px;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(90deg,#a78bfa,#6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 20px;
    color: #cbd5e1;
    margin-top: 20px;
    max-width: 600px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg,#6366f1,#8b5cf6) !important;
    color:white !important;
    border:none !important;
    border-radius:50px !important;
    height:50px !important;
    width:220px !important;
    font-weight:600 !important;
    box-shadow:0 10px 30px rgba(99,102,241,0.5) !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
}

/* ================= FEATURES ================= */

.feature-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s ease;
    min-height: 180px;
    margin-bottom: 30px;   /* 👈 Equal vertical spacing */
}

.feature-card:hover {
    transform: translateY(-5px);
    border: 1px solid #6366f1;
}


/* Labels */
label {
    color:#e2e8f0 !important;
    font-weight:700 !important;
    font-size:16px !important;
}
/* ================= CONTACT SECTION ================= */

.contact-section {
    margin-top: 80px;
}

.contact-card {
    background: rgba(255,255,255,0.05);
    padding: 35px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    transition: 0.3s ease;
    min-height: 220px;
}

.contact-card:hover {
    transform: translateY(-6px);
    border: 1px solid #6366f1;
    box-shadow: 0 15px 40px rgba(99,102,241,0.2);
}

.contact-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #a78bfa;
}

.contact-text {
    color: #cbd5e1;
    line-height: 1.8;
    font-size: 16px;
}

.contact-highlight {
    color: #22c55e;
    font-weight: 500;
}
            section.main > div {
    padding-left: 80px;
    padding-right: 80px;
}

/* Footer */
.footer {
    text-align:center;
    padding:60px 0;
    color:#94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LANDING PAGE
# ======================================================

if st.session_state.page == "landing":
    query_params = st.query_params

    if "page" in query_params:
        st.session_state.page = query_params["page"]
    st .markdown("""<div id = "top"></div>""", unsafe_allow_html=True)
    st.markdown("""
        <div class="navbar">
            <div class="logo">🚀 JOBMATCH</div>
            <div class="nav-right">
                <a class="nav-link" href="#top">Home</a>
                <a class="nav-link" href="#features">Features</a>
                <a class="nav-link" href="#contact">Contact</a>
                <a class="nav-btn" href="?page=predictor">Get Started</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2,1])

    with col1:
        st.markdown('<div class="hero-title">Turn Your Education<br>Into Career Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">JOBMATCH: EDU2JOB is an AI-powered job role prediction system that analyzes academic background and predicts the most suitable career path with confidence scoring.</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Get Started"):
            if st.session_state.logged_in:
                st.session_state.page = "dashboard"
            else:
                st.session_state.page = "auth"
            st.rerun()

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71",
            use_container_width=True
        )

    # FEATURES
    st.markdown('<div id="features"></div>', unsafe_allow_html=True)
    st.markdown("<br><br><h2>Why Choose JOBMATCH?</h2>", unsafe_allow_html=True)
    st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)

    row1_col1, row1_col2, row1_col3 = st.columns([1,1,1], gap="large")

    row2_col1, row2_col2, row2_col3 = st.columns([1,1,1], gap="large")
    with row1_col1:
        st.markdown('<div class="feature-card"><h4>🧠 Smart Prediction Engine</h4>ML pipeline with preprocessing and probability-based classification.</div>', unsafe_allow_html=True)

    with row1_col2:
        st.markdown('<div class="feature-card"><h4>⚡ Real-Time Insights</h4>Instant analysis of academic background for quick results.</div>', unsafe_allow_html=True)

    with row1_col3:
        st.markdown('<div class="feature-card"><h4>📊 Data-Driven Model</h4>Structured dataset mapping education to job roles.</div>', unsafe_allow_html=True)

    with row2_col1:
        st.markdown('<div class="feature-card"><h4>🎯 Confidence Scoring</h4>Displays prediction probability for transparency.</div>', unsafe_allow_html=True)

    with row2_col2:
        st.markdown('<div class="feature-card"><h4>🎨 Modern Interface</h4>Interactive and responsive UI with custom styling.</div>', unsafe_allow_html=True)

    with row2_col3:
        st.markdown('<div class="feature-card"><h4>🚀 Scalable Architecture</h4>Extendable for advanced ML models and larger datasets.</div>', unsafe_allow_html=True)

    #CONTACTS
    st.markdown('<div class="contact-section">', unsafe_allow_html=True)
    st.markdown("<br><br><h2>Contact</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-title">📬 Get In Touch</div>
            <div class="contact-text">
                📧 <span class="contact-highlight">sonali04037@gmail.com</span><br>
                📍 Bhopal, India<br>
                💼 LinkedIn: https://www.linkedin.com/in/sonali-singh-73644a248/<br>
                💻 GitHub: https://github.com/Sonu495<br>
                📞 Contact: 5672728933
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="contact-card">
            <div class="contact-title">🚀 Open For</div>
            <div class="contact-text">
                ✔ AI/ML Projects<br>
                ✔ Internship Opportunities<br>
                ✔ Research Collaboration<br>
                ✔ Tech Discussions
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# AUTH PAGE (LOGIN / REGISTER)
# ======================================================
elif st.session_state.page == "auth":

    st.markdown("<h1 style='text-align:center;'>🔐 Login / Register</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN ----------------
    with tab1:
        st.subheader("🔐 Login")

        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(login_username, login_password)
            if user:
                st.session_state.logged_in = True
                st.session_state.current_user = user[2]
                st.session_state.user_id = user[0]
                st.success("Login successful!")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password")

    # ---------------- REGISTER ----------------
    with tab2:
        st.subheader("📝 Register")

        email = st.text_input("Email")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        def is_strong_password(password):
            if len(password) < 8: return False
            if not re.search(r"[A-Z]", password): return False
            if not re.search(r"[a-z]", password): return False
            if not re.search(r"[0-9]", password): return False
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): return False
            return True
        
        def is_valid_email(email):
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, email)

        if st.button("Register"):
            if not email or not username or not password:
                st.error("All fields required")

            elif not is_valid_email(email):
                st.error("Invalid email format")

            elif not is_strong_password(password):
                st.error("Weak password")

            else:
                ok = add_user(email, username, password)
                if ok:
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Email or Username already exists")
# ======================================================
# DASHBOARD PAGE
# ======================================================                   
elif st.session_state.page == "dashboard":

        # ---------------- DASHBOARD NAVBAR ----------------
    nav1, nav2, nav3, nav4 = st.columns([6,2,2,2])

    with nav1:
        st.markdown(f"### 👋 Welcome, {st.session_state.current_user}")

    with nav2:
        if st.button("📊 Prediction History"):
            st.session_state.page = "history"
            st.rerun()

    with nav3:
        if st.button("👤 Profile"):
            st.session_state.page = "dashboard"
            st.rerun()

    with nav4:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_id = None
            st.session_state.page = "landing"
            st.rerun()

    st.markdown("---")
    user_id = st.session_state.user_id
    username = st.session_state.current_user

    profile = get_profile(user_id)

    col1, col2 = st.columns([1,2])

    # ---------------- PROFILE CARD ----------------
    with col1:
        if profile:
            name = profile[1] or ""
            role = profile[2] or "Student"
            field = profile[3] or ""
            skills = profile[4] or ""
            complete = profile[5]
        else:
            name = role = field = skills = ""
            complete = 40

        st.markdown(f"""
        ### 👤 Profile
        **Name:** {name if name else "Not Set"}  
        **Role:** {role}  
        **Field:** {field if field else "Not Set"}  
        **Skills:** {skills if skills else "Not Set"}  
        **Completion:** {complete}%
        """)

    # ---------------- EDIT PROFILE ----------------
    with col2:
        st.markdown("### ✏ Edit Profile")

        name = st.text_input("Full Name", value=name)
        role = st.selectbox("Role", ["Student","Job Seeker","Professional"])
        field = st.text_input("Field of Interest", value=field)
        skills = st.text_area("Skills (comma separated)", value=skills)

        if st.button("💾 Save Profile"):
            save_profile(user_id, name, role, field, skills)
            st.success("Profile Updated!")
            st.rerun()

    st.markdown("---")

    # ---------------- QUICK ACTIONS ----------------
    st.markdown("### ⚡ Quick Actions")

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("🎯 New Prediction"):
            st.session_state.page = "predictor"
            st.rerun()

    with q2:
        if st.button("📄 Upload Resume"):
            st.session_state.page = "resume"
            st.rerun()

    with q3:
        if st.button("💼 Browse Jobs"):
            st.session_state.page = "jobs"
            st.rerun()

# ======================================================
# PREDICTION HISTORY PAGE
# ======================================================
elif st.session_state.page == "history":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.session_state.page = "auth"
        st.rerun()

    st.markdown("## 🧾 Prediction History")

    history = get_predictions(st.session_state.user_id)

    if not history:
        st.info("No predictions yet")
    else:
        for row in history:
            degree, spec, cgpa, role, confidence, created = row

            st.markdown(f"""
            <div style="
                max-width:800px;
                margin:20px auto;
                padding:20px;
                border-radius:16px;
                background: rgba(255,255,255,0.05);
                border:1px solid rgba(255,255,255,0.08);
            ">
                <h4 style="margin-bottom:8px;">🎯 {role}</h4>
                <p style="margin:0;">📈 Confidence: <b>{confidence:.2f}%</b></p>
                <p style="margin:0;">🎓 {degree} • {spec} • CGPA: {cgpa}</p>
                <p style="margin:0; color:#94a3b8;">🗓 {created}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([4,2,4])
    with col2:
        if st.button("⬅ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

# ======================================================
# RESUME PAGE
# ======================================================
elif st.session_state.page == "resume":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.session_state.page = "auth"
        st.rerun()

    st.markdown("""
    <div style="max-width:900px; margin:0 auto; padding-top:30px;">
    """, unsafe_allow_html=True)

    st.markdown("## 📄 Resume Upload")

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.05);
        padding:30px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:30px;">
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF/DOCX)",
        type=["pdf", "docx"]
    )

    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- BACK BUTTON ----------------
    c1, c2, c3 = st.columns([4,2,4])
    with c2:
        if st.button("⬅ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
# ======================================================
# PREDICTOR PAGE
# ======================================================
elif st.session_state.page == "predictor":

    if not st.session_state.logged_in:
        st.warning("Please login first")
        st.session_state.page = "auth"
        st.rerun()
    model = joblib.load("model_pipeline.pkl")
    df = pd.read_csv("job_dataset.csv")

    # Container wrapper
    st.markdown("""
    <div style="max-width:900px; margin:0 auto; padding-top:30px;">
    """, unsafe_allow_html=True)

    st.markdown(
        "<h1 style='text-align:center; margin-bottom:40px;'>🎓 Career Prediction Dashboard</h1>",
        unsafe_allow_html=True
    )

    # ------------------ INPUT CARD ------------------
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.05);
        padding:35px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:40px;">
    """, unsafe_allow_html=True)

    degree = st.selectbox("Degree", sorted(df["Degree"].unique()))
    specialization = st.selectbox(
        "Specialization",
        sorted(df[df["Degree"] == degree]["Specialization"].unique())
    )
    cgpa = st.number_input("CGPA", 5.0, 10.0, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([4,2,4])
    with col2:
        predict_clicked = st.button("✨ Predict Career")

    st.markdown("</div>", unsafe_allow_html=True)

    # Session init
    if "predicted_job" not in st.session_state:
        st.session_state.predicted_job = None
        st.session_state.confidence = None

    # PREDICTION 
    if predict_clicked:
        input_df = pd.DataFrame(
            [[degree, specialization, cgpa]],
            columns=["Degree","Specialization","CGPA"]
        )

        # Probabilities for all jobs
        probs = model.predict_proba(input_df)[0]
        classes = model.classes_

        # Top 3 predictions
        top3_idx = probs.argsort()[-3:][::-1]
        top3_jobs = [(classes[i], probs[i]*100) for i in top3_idx]

        # Store best prediction (for existing UI)
        st.session_state.predicted_job = top3_jobs[0][0]
        st.session_state.confidence = top3_jobs[0][1]

        # Store top 3 list
        st.session_state.top3 = top3_jobs

        # ✅ NEW: Save prediction history to database
        save_prediction(
            user_id=st.session_state.user_id,
            degree=degree,
            specialization=specialization,
            cgpa=cgpa,
            role=st.session_state.predicted_job,
            confidence=st.session_state.confidence
        )

# ------------------ RESULT CARD ------------------
    if st.session_state.predicted_job:

        # CSS (load once)
        st.markdown("""
        <style>
        .result-card {
            max-width: 750px;
            margin: 40px auto;
            padding: 35px;
            border-radius: 20px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(99,102,241,0.3);
            backdrop-filter: blur(10px);
            text-align: center;
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }
        .result-title {
            font-size: 16px;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #94a3b8;
            margin-bottom: 15px;
        }
        .result-role {
            font-size: 36px;
            font-weight: 700;
            color: #a78bfa;
            margin-bottom: 15px;
        }
        .result-confidence {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 30px;
            background: rgba(34,197,94,0.15);
            border: 1px solid rgba(34,197,94,0.4);
            color: #22c55e;
            font-weight: 600;
            font-size: 16px;
        }
        .suggestion-title {
            margin-top: 25px;
            font-weight: 600;
            color: #cbd5e1;
            text-align: left;
        }
        .suggestion-item {
            margin-top: 8px;
            padding: 10px 18px;
            border-radius: 12px;
            background: rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            font-size:15px;
            text-align:left;
        }
        </style>
        """, unsafe_allow_html=True)

        # Build suggestions
        suggestions_html = ""
        if "top3" in st.session_state and len(st.session_state.top3) > 1:
            for i, (job, prob) in enumerate(st.session_state.top3[1:], start=2):
                suggestions_html += (
                    f'<div class="suggestion-item">'
                    f'⭐ Option {i}: <b>{job}</b> — {prob:.2f}%'
                    f'</div>'
                )

        # Card HTML
        card_html = (
            f'<div class="result-card">'
            f'<div class="result-title">Prediction</div>'
            f'<div class="result-role">{st.session_state.predicted_job}</div>'
            f'<div class="result-confidence">Confidence: {st.session_state.confidence:.2f}%</div>'
            f'<div class="suggestion-title">Other Suggestions:</div>'
            f'{suggestions_html}'
            f'</div>'
        )

        st.markdown(card_html, unsafe_allow_html=True)
# ------------------ GRAPH ------------------
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2>📊 Job Distribution</h2>", unsafe_allow_html=True)

    job_counts = df["JobRole"].value_counts().reset_index()
    job_counts.columns = ["JobRole","Count"]

    fig = px.bar(job_counts, x="JobRole", y="Count", color="JobRole")
    st.plotly_chart(fig, use_container_width=True)

    # ------------------ BACK BUTTON ------------------
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([4,2,4])
    with col2:
        if st.button("⬅ Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    # Close wrapper
    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
<div class="footer">
© 2026 JOBMATCH: EDU2JOB — Built by Sonali Singh
</div>
""", unsafe_allow_html=True)