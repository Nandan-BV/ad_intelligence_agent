from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(analysis_data, filename="Competitive_Intelligence_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor("#1E3A8A") # Deep Navy
    accent_color = colors.HexColor("#2563EB")  # Blue
    dark_neutral = colors.HexColor("#0F172A")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=primary_color,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=accent_color,
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=dark_neutral,
        spaceAfter=8,
        leading=14
    )

    story.append(Paragraph("AI Competitive Intelligence & Profit Playbook", title_style))
    story.append(Paragraph("Generated automatically via Local Intelligence Engine", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Core Findings Table / Summary Blocks
    for key, value in analysis_data.items():
        if key == "error":
            continue
        formatted_key = key.replace("_", " ").title()
        story.append(Paragraph(f"<b>{formatted_key}:</b>", heading_style))
        story.append(Paragraph(str(value), body_style))
        story.append(Spacer(1, 4))
        
    doc.build(story)
    return filename
