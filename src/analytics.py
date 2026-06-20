import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'database.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_students():
    """Retrieve all students."""
    conn = get_connection()
    query = "SELECT * FROM students"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_student_details(student_id):
    """Retrieve details, attendance, and scores for a specific student."""
    conn = get_connection()
    
    student_query = f"SELECT * FROM students WHERE student_id = {student_id}"
    student_df = pd.read_sql(student_query, conn)
    
    attendance_query = f"SELECT * FROM attendance WHERE student_id = {student_id}"
    attendance_df = pd.read_sql(attendance_query, conn)
    
    scores_query = f"SELECT * FROM scores WHERE student_id = {student_id}"
    scores_df = pd.read_sql(scores_query, conn)
    
    conn.close()
    return student_df, attendance_df, scores_df

def get_attendance_vs_performance():
    """Analyze correlation between attendance and performance."""
    conn = get_connection()
    
    query = """
    SELECT 
        a.student_id, 
        a.term, 
        a.attendance_percentage, 
        AVG(s.score) as average_score
    FROM attendance a
    JOIN scores s ON a.student_id = s.student_id AND a.term = s.term
    GROUP BY a.student_id, a.term
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_subject_performance():
    """Analyze subject-wise performance."""
    conn = get_connection()
    
    query = """
    SELECT 
        subject, 
        AVG(score) as average_score, 
        MAX(score) as max_score, 
        MIN(score) as min_score
    FROM scores
    GROUP BY subject
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_performance_trends():
    """Analyze performance trends over terms."""
    conn = get_connection()
    
    query = """
    SELECT 
        term, 
        AVG(score) as average_term_score
    FROM scores
    GROUP BY term
    ORDER BY term
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_top_performers(term, top_n=10):
    """Get the top performing students for a specific term."""
    conn = get_connection()
    
    query = f"""
    SELECT 
        st.student_id,
        st.name,
        AVG(sc.score) as average_score
    FROM students st
    JOIN scores sc ON st.student_id = sc.student_id
    WHERE sc.term = '{term}'
    GROUP BY st.student_id
    ORDER BY average_score DESC
    LIMIT {top_n}
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
