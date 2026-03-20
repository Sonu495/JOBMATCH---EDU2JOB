import sqlite3
import bcrypt
from datetime import datetime
import logging

logging.basicConfig(
    filename="db_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_NAME = "jobmatch.db"

# -----------------------------
# CONNECT
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn

# -----------------------------
# CREATE TABLES
# -----------------------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- USERS ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ---------------- PROFILE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT,
        role TEXT,
        field TEXT,
        skills TEXT,
        profile_complete INTEGER DEFAULT 40,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ---------------- PREDICTION HISTORY ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        degree TEXT,
        specialization TEXT,
        cgpa REAL,
        predicted_role TEXT,
        confidence REAL,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ---------------- RESUME TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        user_id INTEGER PRIMARY KEY,
        file_name TEXT,
        file_data BLOB,
        uploaded_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# ADD USER
# -----------------------------
def add_user(email, username, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 🔐 Hash password
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cur.execute(
            "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
            (email, username, hashed_pw)
        )
        conn.commit()
        return True

    except Exception as e:
        logging.error(f"ADD USER ERROR: {e}")
        return False
    finally:
        conn.close()
# -----------------------------
# LOGIN USER
# -----------------------------
def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user:
            stored_hash = user[3]
            if bcrypt.checkpw(password.encode(), stored_hash):
                return user
        return None

    except Exception as e:
        print("LOGIN ERROR:", e)
        return None
    finally:
        conn.close()

# -----------------------------
# GET PROFILE
# -----------------------------
def get_profile(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,))
    profile = cur.fetchone()

    conn.close()
    return profile

# -----------------------------
# SAVE / UPDATE PROFILE
# -----------------------------
def save_profile(user_id, name, role, field, skills):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM profiles WHERE user_id=?", (user_id,))
    exists = cur.fetchone()

    completeness = 40
    if name: completeness += 15
    if role: completeness += 15
    if field: completeness += 15
    if skills: completeness += 15

    if exists:
        cur.execute("""
            UPDATE profiles
            SET full_name=?, role=?, field=?, skills=?, profile_complete=?
            WHERE user_id=?
        """, (name, role, field, skills, completeness, user_id))
    else:
        cur.execute("""
            INSERT INTO profiles (user_id, full_name, role, field, skills, profile_complete)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, name, role, field, skills, completeness))

    conn.commit()
    conn.close()

# -----------------------------
# SAVE PREDICTION HISTORY
# -----------------------------
def save_prediction(user_id, degree, specialization, cgpa, role, confidence):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO predictions 
        (user_id, degree, specialization, cgpa, predicted_role, confidence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        degree,
        specialization,
        cgpa,
        role,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

# -----------------------------
# GET PREDICTION HISTORY
# -----------------------------
def get_predictions(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT degree, specialization, cgpa, predicted_role, confidence, created_at
        FROM predictions
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows

# -----------------------------
# SAVE / UPDATE RESUME
# -----------------------------
def save_resume(user_id, file_name, file_bytes):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM resumes WHERE user_id=?", (user_id,))
    exists = cur.fetchone()

    if exists:
        cur.execute("""
            UPDATE resumes
            SET file_name=?, file_data=?, uploaded_at=?
            WHERE user_id=?
        """, (
            file_name,
            file_bytes,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id
        ))
    else:
        cur.execute("""
            INSERT INTO resumes (user_id, file_name, file_data, uploaded_at)
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            file_name,
            file_bytes,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()
# -----------------------------
# GET RESUME
# -----------------------------
def get_resume(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT file_name, file_data, uploaded_at
        FROM resumes
        WHERE user_id=?
    """, (user_id,))

    data = cur.fetchone()
    conn.close()
    return data