from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

OUT = Path(r"C:\Users\dolan\OneDrive - purdue.edu\2026-Fall\FIN-43900 - AI Finance Applications\projects\project-1\recovery\edition-a-20261006\Edition-A-Recovery-Evidence.pdf")
styles = getSampleStyleSheet()
title = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=21, leading=25, alignment=TA_CENTER, textColor=HexColor("#12355B"), spaceAfter=8)
sub = ParagraphStyle("sub", parent=styles["Normal"], fontSize=10, leading=14, alignment=TA_CENTER, textColor=HexColor("#4B5563"), spaceAfter=18)
h = ParagraphStyle("h", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=HexColor("#12355B"), spaceBefore=10, spaceAfter=6)
body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=10)
notice = ParagraphStyle("notice", parent=body, fontName="Helvetica-Bold", textColor=HexColor("#0F766E"), backColor=HexColor("#ECFDF5"), borderColor=HexColor("#99F6E4"), borderWidth=0.5, borderPadding=9, spaceAfter=12)
small = ParagraphStyle("small", parent=styles["Normal"], fontSize=8.8, leading=12, textColor=HexColor("#374151"))

story = [
    Paragraph("Edition A verification", title),
    Paragraph("Oladapo Olaniyan | FIN-43900 Project 1 | Updated October 17, 2026", sub),
    Paragraph("APPROVED FOR USE - Oladapo Olaniyan reports that the TA said the copy used is acceptable as long as the information is the same. This is student-reported verbal guidance; no written TA message is claimed.", notice),
    Paragraph("Verification", h),
    Paragraph("Brightspace receipt 22599005 records the September 1, 2026 submission. The receipt-linked file and receipt are preserved as the original submission evidence. Their SHA-256 record is retained in the project documentation for traceability.", body),
    Paragraph("The working package uses the same information under the TA's reported condition. The project does not represent a different document as the original submitted file.", body),
    Paragraph("Current evidence", h),
]
rows = [
    [Paragraph("Item", small), Paragraph("Status", small), Paragraph("Location", small)],
    [Paragraph("Original submission evidence", small), Paragraph("Preserved", small), Paragraph("Receipt and receipt-linked file", small)],
    [Paragraph("TA guidance", small), Paragraph("Approved use when information is the same", small), Paragraph("Student-reported verbal clarification", small)],
    [Paragraph("Working material", small), Paragraph("Used under the reported condition", small), Paragraph("Edition B research-evolution record", small)],
]
t = Table(rows, colWidths=[1.55*inch, 2.7*inch, 2.65*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), HexColor("#DCEAF7")),
    ("GRID", (0,0), (-1,-1), 0.35, HexColor("#CBD5E1")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story += [t, Spacer(1, 12), Paragraph("This page summarizes the verified submission evidence and the reported TA guidance for the working package.", small)]
doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=0.65*inch, rightMargin=0.65*inch, topMargin=0.55*inch, bottomMargin=0.55*inch, title="Edition A Recovery Evidence - Oladapo Olaniyan")
doc.build(story)
print(OUT)
