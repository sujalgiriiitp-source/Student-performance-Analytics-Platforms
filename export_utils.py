import pandas as pd
from fpdf import FPDF
import tempfile
import os

def export_to_csv(df, filename="report.csv"):
    """Export dataframe to a CSV string for Streamlit download."""
    return df.to_csv(index=False).encode('utf-8')

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Student Performance Analytics Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def export_to_pdf(df, title="Analytics Data"):
    """Export dataframe to a PDF file and return the bytes for downloading."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    
    # Calculate column widths (simple dynamic allocation)
    col_width = pdf.epw / len(df.columns)
    line_height = pdf.font_size * 2
    
    # Header
    pdf.set_font("Arial", "B", 10)
    for col_name in df.columns:
        pdf.cell(col_width, line_height, str(col_name), border=1)
    pdf.ln(line_height)
    
    # Rows
    pdf.set_font("Arial", size=10)
    for row_index, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, line_height, str(item)[:20], border=1) # Truncate to avoid overflow
        pdf.ln(line_height)
    
    # Create temporary file to save PDF bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        temp_path = tmp.name
        
    pdf.output(temp_path)
    
    with open(temp_path, "rb") as f:
        pdf_bytes = f.read()
        
    os.remove(temp_path)
    return pdf_bytes
