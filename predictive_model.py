import pandas as pd
import numpy as np
from src.analytics import get_attendance_vs_performance

def train_topper_model():
    """
    Train a simple linear regression model to predict average score based on attendance
    using pure numpy (to avoid heavy scikit-learn/scipy dependencies that require compilation).
    """
    df = get_attendance_vs_performance()
    
    if df.empty:
        return None, None
        
    X = df['attendance_percentage'].values
    y = df['average_score'].values
    
    # Calculate simple linear regression coefficients (y = mx + c)
    # using numpy's polyfit (degree 1)
    coefficients = np.polyfit(X, y, 1)
    
    # Calculate a simple R^2 score for validation
    p = np.poly1d(coefficients)
    y_pred = p(X)
    
    # Calculate R-squared
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2_score = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return coefficients, r2_score

def predict_future_toppers(current_attendance_df, top_n=5):
    """
    Predict future toppers based on their current attendance using the trained numpy model.
    """
    coefficients, r2 = train_topper_model()
    
    if coefficients is None or current_attendance_df.empty:
        return pd.DataFrame()
        
    X_pred = current_attendance_df['attendance_percentage'].values
    
    # Predict scores (y = mx + c)
    p = np.poly1d(coefficients)
    predicted_scores = p(X_pred)
    
    # Add predictions to dataframe
    results_df = current_attendance_df.copy()
    results_df['predicted_score'] = predicted_scores
    
    # Sort to find toppers
    toppers = results_df.sort_values(by='predicted_score', ascending=False).head(top_n)
    
    return toppers
