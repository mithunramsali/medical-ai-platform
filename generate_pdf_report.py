from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_pdf_report(filename="Medical_AI_Platform_Project_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor("#1E3A8A"))
    h2_style = ParagraphStyle('Heading2', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor("#1D4ED8"))
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14)

    # Title Banner
    story.append(Paragraph("Advanced AI Medical Intelligence Platform", title_style))
    story.append(Paragraph("Project Technical Evaluation & Architecture Documentation", ParagraphStyle('Sub', fontSize=12, textColor=colors.gray)))
    story.append(Spacer(1, 15))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h2_style))
    story.append(Paragraph(
        "This project presents an enterprise-grade medical imaging diagnostic solution combining Deep Learning, "
        "Explainable AI (Grad-CAM), Database Persistence, and LLM-assisted report generation into a unified web engine.",
        body_style
    ))
    story.append(Spacer(1, 12))

    # Tech Stack Table
    story.append(Paragraph("2. System Architecture & Tech Stack", h2_style))
    table_data = [
        ["Component", "Technology", "Description"],
        ["Deep Learning", "PyTorch / ResNet-18", "Pre-trained CNN fine-tuned for classification."],
        ["Explainable AI", "Grad-CAM", "Visual heatmap projection layer targeting feature maps."],
        ["Backend API", "FastAPI / SQLite", "Asynchronous API endpoints with database audit logs."],
        ["Frontend UI", "Streamlit", "User-friendly web dashboard for clinicians."]
    ]
    t = Table(table_data, colWidths=[110, 130, 270])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # XAI & LLM Integration
    story.append(Paragraph("3. Explainable AI & Clinical Decision Support", h2_style))
    story.append(Paragraph(
        "To satisfy medical transparency criteria, Grad-CAM overlays highlight key regions contributing to model prediction. "
        "An LLM pipeline ingests numerical confidence metrics and classification labels to construct structured diagnostic summaries.",
        body_style
    ))
    story.append(Spacer(1, 15))

    # Evaluation Conclusion
    story.append(Paragraph("4. Software Quality & Deliverables", h2_style))
    story.append(Paragraph(
        "The application includes automated unit testing hooks, SQLite audit history tracking, "
        "and containerized Docker execution scripts suitable for cloud deployment.",
        body_style
    ))

    doc.build(story)
    print(f"Project Report successfully generated: '{filename}'")

if __name__ == "__main__":
    build_pdf_report()