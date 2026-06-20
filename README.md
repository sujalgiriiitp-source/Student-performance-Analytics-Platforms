# 🎓 Student Performance Analytics Platform

A professional, portfolio-quality Student Performance Analytics Platform built to analyze, visualize, and predict student performance using a modern Python data stack.

## 🚀 Features

1. **Student Dataset Management**: SQLite database integration with mock data generation (100+ realistic student profiles, attendance, and scores).
2. **Attendance Analysis**: Correlate attendance percentages with average grades to highlight the impact of class participation.
3. **Subject-wise Performance**: Statistical overview of scores across different subjects (Mathematics, Physics, Literature, etc.).
4. **Topper Prediction**: Integrated Machine Learning (Linear Regression) to predict future toppers based on current attendance patterns.
5. **Performance Trends**: Time-series analysis of average scores across different academic terms.
6. **Interactive Dashboard**: A fully responsive web interface built with **Streamlit** for seamless data exploration.
7. **Export Reports**: Generate and download datasets in **CSV** and **PDF** formats instantly.

## 🛠️ Technology Stack

- **Core**: Python 3
- **Data Manipulation**: Pandas, NumPy
- **Database**: SQLite3 (Standard Library)
- **Machine Learning**: Scikit-Learn
- **Visualization**: Matplotlib
- **Web Dashboard**: Streamlit
- **PDF Generation**: FPDF2

## 📁 Project Structure

```text
student-performance-platform/
├── data/
│   └── database.db              # SQLite Database (generated)
├── src/
│   ├── __init__.py
│   ├── db_setup.py              # Script to initialize DB and generate mock data
│   ├── analytics.py             # Pandas queries and metrics calculation
│   ├── visualization.py         # Matplotlib chart generation
│   ├── predictive_model.py      # ML logic for topper prediction
│   └── export_utils.py          # CSV/PDF export functionality
├── app.py                       # Main Streamlit dashboard application
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## ⚙️ Installation & Setup

1. **Clone the repository** (or download the source code):
   ```bash
   git clone <repository-url>
   cd "Student Performance"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**:
   Run the setup script to create the SQLite database and generate mock data.
   ```bash
   python src/db_setup.py
   ```

## 🖥️ Running the Application

Launch the interactive dashboard using Streamlit:

```bash
streamlit run app.py
```

The application will open in your default web browser (typically at `http://localhost:8501`).

## 📊 Modules Overview

- **Dashboard Overview**: Get a bird's-eye view of attendance correlation, subject averages, and term-over-term trends.
- **Student Directory**: Search for individual students and view their specific attendance and subject scores.
- **Topper Prediction**: Utilizes `scikit-learn` to predict future student performance and identify potential top performers.
- **Detailed Reports**: Export raw data into easily shareable CSVs or professional PDF reports.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
# Student-performance-Analytics-Platforms
