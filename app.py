import streamlit as st
import pandas as pd
import os

from src.analytics import (
    get_all_students, get_student_details, 
    get_attendance_vs_performance, get_subject_performance, 
    get_performance_trends, get_top_performers
)
from src.predictive_model import predict_future_toppers
from src.visualization import (
    plot_attendance_vs_performance, plot_subject_performance, 
    plot_performance_trends
)
from src.export_utils import export_to_csv, export_to_pdf

# Check if database exists, prompt setup if not
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'database.db')

st.set_page_config(page_title="Student Performance Analytics", page_icon="🎓", layout="wide")

st.title("🎓 Student Performance Analytics Platform")
st.markdown("A professional portfolio project built with Python, Pandas, Matplotlib, and Streamlit.")

if not os.path.exists(DB_PATH):
    st.error("Database not found. Please run `python src/db_setup.py` to initialize the database and generate mock data.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Module:", 
                        ["Dashboard Overview", "Student Directory", "Topper Prediction", "Detailed Reports"])

if page == "Dashboard Overview":
    st.header("Overall Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Attendance vs. Performance")
        att_df = get_attendance_vs_performance()
        if not att_df.empty:
            fig1 = plot_attendance_vs_performance(att_df)
            st.pyplot(fig1)
        else:
            st.info("No data available.")
            
    with col2:
        st.subheader("Subject-wise Averages")
        subj_df = get_subject_performance()
        if not subj_df.empty:
            fig2 = plot_subject_performance(subj_df)
            st.pyplot(fig2)
        else:
            st.info("No data available.")
            
    st.divider()
    st.subheader("Performance Trends Across Terms")
    trend_df = get_performance_trends()
    if not trend_df.empty:
        fig3 = plot_performance_trends(trend_df)
        st.pyplot(fig3)

elif page == "Student Directory":
    st.header("Student Directory & Profiles")
    students_df = get_all_students()
    
    if students_df.empty:
        st.warning("No students found in the database.")
    else:
        st.dataframe(students_df, use_container_width=True)
        
        st.subheader("Lookup Student")
        student_id = st.selectbox("Select Student ID for details", students_df['student_id'].tolist())
        
        if student_id:
            student_info, attendance, scores = get_student_details(student_id)
            
            st.markdown(f"### Profile: {student_info['name'].iloc[0]} (Grade {student_info['grade_level'].iloc[0]}) - {student_info['major'].iloc[0]}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Attendance Record**")
                st.dataframe(attendance)
            with col2:
                st.write("**Subject Scores**")
                st.dataframe(scores)

elif page == "Topper Prediction":
    st.header("Topper Prediction Model")
    st.write("Using a Machine Learning model (Linear Regression) to predict future scores based on current attendance patterns.")
    
    att_df = get_attendance_vs_performance()
    
    if att_df.empty:
        st.warning("Not enough data to run predictions.")
    else:
        # Get latest term's attendance to predict future
        latest_term = att_df['term'].max()
        current_data = att_df[att_df['term'] == latest_term]
        
        st.write(f"Predicting based on {latest_term} attendance...")
        predictions = predict_future_toppers(current_data, top_n=10)
        
        # Merge with student names
        students_df = get_all_students()
        predictions_merged = pd.merge(predictions, students_df[['student_id', 'name']], on='student_id')
        predictions_display = predictions_merged[['student_id', 'name', 'attendance_percentage', 'predicted_score']]
        
        st.dataframe(predictions_display.style.highlight_max(subset=['predicted_score']), use_container_width=True)
        
        st.subheader("Current Top Performers (Actual)")
        top_actual = get_top_performers(latest_term)
        st.dataframe(top_actual, use_container_width=True)

elif page == "Detailed Reports":
    st.header("Export Data & Reports")
    st.write("Download data for external analysis or reporting.")
    
    report_type = st.selectbox("Select Data to Export:", 
                               ["Subject Performance", "Attendance vs Performance", "Overall Trends"])
    
    df_to_export = pd.DataFrame()
    if report_type == "Subject Performance":
        df_to_export = get_subject_performance()
    elif report_type == "Attendance vs Performance":
        df_to_export = get_attendance_vs_performance()
    elif report_type == "Overall Trends":
        df_to_export = get_performance_trends()
        
    st.dataframe(df_to_export, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        csv_data = export_to_csv(df_to_export)
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name=f"{report_type.lower().replace(' ', '_')}.csv",
            mime='text/csv'
        )
    
    with col2:
        try:
            pdf_data = export_to_pdf(df_to_export, title=report_type)
            st.download_button(
                label="Download as PDF",
                data=pdf_data,
                file_name=f"{report_type.lower().replace(' ', '_')}.pdf",
                mime='application/pdf'
            )
        except Exception as e:
            st.error(f"Could not generate PDF. Error: {e}")
