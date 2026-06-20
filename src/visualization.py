import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def set_style():
    """Set professional styling for all plots."""
    plt.style.use('ggplot')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12

def plot_attendance_vs_performance(df):
    """Create a scatter plot of attendance vs average score."""
    set_style()
    fig, ax = plt.subplots()
    
    scatter = ax.scatter(df['attendance_percentage'], df['average_score'], 
                         c=df['average_score'], cmap='viridis', alpha=0.7)
    
    ax.set_title('Attendance vs Performance Correlation')
    ax.set_xlabel('Attendance Percentage (%)')
    ax.set_ylabel('Average Score')
    
    # Add a trendline
    z = np.polyfit(df['attendance_percentage'], df['average_score'], 1)
    p = np.poly1d(z)
    ax.plot(df['attendance_percentage'], p(df['attendance_percentage']), "r--", alpha=0.8)
    
    fig.colorbar(scatter, ax=ax, label='Average Score')
    plt.tight_layout()
    return fig

def plot_subject_performance(df):
    """Create a bar chart showing subject-wise performance."""
    set_style()
    fig, ax = plt.subplots()
    
    x = np.arange(len(df['subject']))
    width = 0.35
    
    # Plotting Average and Max Scores side by side
    ax.bar(x - width/2, df['average_score'], width, label='Average Score', color='#3498db')
    ax.bar(x + width/2, df['max_score'], width, label='Max Score', color='#2ecc71')
    
    ax.set_ylabel('Score')
    ax.set_title('Subject-wise Performance Overview')
    ax.set_xticks(x)
    ax.set_xticklabels(df['subject'], rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    return fig

def plot_performance_trends(df):
    """Create a line chart tracking performance trends over terms."""
    set_style()
    fig, ax = plt.subplots()
    
    ax.plot(df['term'], df['average_term_score'], marker='o', linestyle='-', color='#e74c3c', linewidth=2, markersize=8)
    
    ax.set_title('Overall Performance Trends Over Time')
    ax.set_xlabel('Academic Term')
    ax.set_ylabel('Average Class Score')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adding data labels
    for i, txt in enumerate(df['average_term_score']):
        ax.annotate(f"{txt:.1f}", (df['term'].iloc[i], df['average_term_score'].iloc[i]), 
                    textcoords="offset points", xytext=(0,10), ha='center')
                    
    plt.tight_layout()
    return fig
