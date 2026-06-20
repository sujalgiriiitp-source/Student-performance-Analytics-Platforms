import sqlite3
import pandas as pd
import numpy as np
import os

# Define the path to the database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'database.db')

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """ Create tables in the SQLite database """
    try:
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                grade_level INTEGER NOT NULL,
                major TEXT NOT NULL
            );
        """)
        
        # Create attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                student_id INTEGER,
                term TEXT NOT NULL,
                total_classes INTEGER NOT NULL,
                attended_classes INTEGER NOT NULL,
                attendance_percentage REAL NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            );
        """)
        
        # Create scores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                student_id INTEGER,
                subject TEXT NOT NULL,
                term TEXT NOT NULL,
                score INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (student_id)
            );
        """)
        
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def generate_mock_data(conn):
    """ Generate mock data using numpy and pandas, and insert into SQLite """
    np.random.seed(42)
    num_students = 100
    
    # 1. Generate Students Data
    first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia", "James", "Isabella", "Oliver", "Mia", "Benjamin", "Charlotte", "Elijah", "Amelia", "Lucas", "Harper", "Mason", "Evelyn", "Logan"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    majors = ["Computer Science", "Mechanical Engineering", "Business Administration", "Psychology", "Biology"]
    
    students_data = []
    for i in range(1, num_students + 1):
        name = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
        grade_level = np.random.choice([1, 2, 3, 4])
        major = np.random.choice(majors)
        students_data.append((i, name, grade_level, major))
        
    students_df = pd.DataFrame(students_data, columns=['student_id', 'name', 'grade_level', 'major'])
    
    # 2. Generate Attendance and Scores Data
    terms = ["Fall 2023", "Spring 2024"]
    subjects = ["Mathematics", "Physics", "Literature", "Computer Science", "History"]
    
    attendance_data = []
    scores_data = []
    
    for student_id in range(1, num_students + 1):
        # Determine student's base aptitude (influences both attendance and scores)
        base_aptitude = np.random.normal(75, 10) 
        base_aptitude = np.clip(base_aptitude, 40, 95)
        
        for term in terms:
            # Attendance is correlated with base aptitude
            attendance_mean = min(base_aptitude + 10, 98)
            attendance_pct = np.random.normal(attendance_mean, 5)
            attendance_pct = np.clip(attendance_pct, 50, 100)
            
            total_classes = 40
            attended_classes = int((attendance_pct / 100) * total_classes)
            actual_attendance_pct = round((attended_classes / total_classes) * 100, 2)
            
            attendance_data.append((student_id, term, total_classes, attended_classes, actual_attendance_pct))
            
            # Scores are correlated with attendance and base aptitude
            for subject in subjects:
                # Add some subject-specific variance
                subject_variance = np.random.normal(0, 5)
                score = base_aptitude + (actual_attendance_pct - 80) * 0.3 + subject_variance
                score = int(np.clip(score, 0, 100))
                scores_data.append((student_id, subject, term, score))
                
    attendance_df = pd.DataFrame(attendance_data, columns=['student_id', 'term', 'total_classes', 'attended_classes', 'attendance_percentage'])
    scores_df = pd.DataFrame(scores_data, columns=['student_id', 'subject', 'term', 'score'])
    
    # Insert Data into SQLite
    try:
        students_df.to_sql('students', conn, if_exists='replace', index=False)
        attendance_df.to_sql('attendance', conn, if_exists='replace', index=False)
        scores_df.to_sql('scores', conn, if_exists='replace', index=False)
        print("Mock data generated and inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

def main():
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    print(f"Initializing database at {DB_PATH}...")
    conn = create_connection(DB_PATH)
    
    if conn is not None:
        create_tables(conn)
        generate_mock_data(conn)
        conn.close()
        print("Database setup complete.")
    else:
        print("Error: Could not establish connection to the database.")

if __name__ == '__main__':
    main()
