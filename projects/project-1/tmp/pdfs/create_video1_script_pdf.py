from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

OUT = Path(r"C:\Users\dolan\OneDrive - purdue.edu\2026-Fall\FIN-43900 - AI Finance Applications\projects\project-1\videos\video-1\Video-1-Script-Oladapo-Olaniyan.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=21, textColor=HexColor("#12355B"), alignment=TA_CENTER, spaceAfter=6)
subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=HexColor("#4B5563"), spaceAfter=10)
h = ParagraphStyle("Heading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=14, textColor=HexColor("#12355B"), spaceBefore=6, spaceAfter=4)
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
cue = ParagraphStyle("Cue", parent=body, fontName="Helvetica-Bold", textColor=HexColor("#0F766E"), backColor=HexColor("#ECFDF5"), borderColor=HexColor("#99F6E4"), borderWidth=0.5, borderPadding=5, spaceBefore=3, spaceAfter=6)
small = ParagraphStyle("Small", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=9.5, textColor=HexColor("#4B5563"))

story = [
    Paragraph("Video 1: Research Evolution and AI Check", title),
    Paragraph("Oladapo Olaniyan | FIN-43900 Project 1 | Recording target: 2:30-2:50", subtitle),
    Paragraph("Use this on your phone while recording. Start on the research-evolution page, read one short block, then follow the green switch cue. Show only the project files on your computer.", cue),
    Paragraph("Before you start", h),
]

rows = [
    [Paragraph("Order", small), Paragraph("Show on your computer", small), Paragraph("What to say", small)],
    [Paragraph("1", small), Paragraph("02-research-evolution.md", small), Paragraph("Research changes and capex correction", small)],
    [Paragraph("2", small), Paragraph("03-validation-and-ai-use.md", small), Paragraph("AI use, ROIC test, and limitations", small)],
]
table = Table(rows, colWidths=[0.45*inch, 2.25*inch, 3.95*inch])
table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), HexColor("#DCEAF7")),
    ("GRID", (0,0), (-1,-1), 0.35, HexColor("#CBD5E1")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
]))
story += [table, Spacer(1, 7), Paragraph("Script", h)]

parts = [
    ("SHOW 1 - 02-research-evolution.md", "Hi, I am Oladapo Olaniyan. This is my PepsiCo research-evolution review. My current recommendation is watch and defer, rather than buy now. The goal of this work was to rebuild the valuation using more current financial information and then decide whether the evidence supports buying at the market price."),
    ("STAY ON 02-research-evolution.md", "For Edition B, I used PepsiCo's FY2025 filing and the latest interim bridge in my model. One important correction involved capital spending. Consolidated capex is $4.415 billion. It includes $4.192 billion from the segments and $223 million of corporate capex."),
    ("STAY ON 02-research-evolution.md", "This correction matters because capital spending is cash the company must invest to keep operating and growing. If I used only the segment figure, I would understate PepsiCo's total investment and overstate the cash that is available to investors. That would make the valuation look stronger than it should."),
    ("SWITCH 2 - 03-validation-and-ai-use.md", "AI helped organize sources, build the model code, and prepare documentation. I recorded that use and checked key values against primary-source arithmetic. I also ran validation checks to make sure the forecast statements, cash flow, and valuation bridge work together. Those checks confirm the model calculations run as intended; they do not prove that every financial assumption is correct."),
    ("STAY ON 03-validation-and-ai-use.md", "For the changed-input test, I lowered terminal ROIC, or return on invested capital, from 15 percent to 12 percent. A lower ROIC means more of the company's future profit must be reinvested to support the same growth. The estimated value per share fell from $117.29 to $111.41, a $5.88 decline. That matched my recorded prediction and shows that the valuation is sensitive to long-run profitability assumptions."),
    ("STAY ON 03-validation-and-ai-use.md - CLOSE", "Overall, I recommend watch and defer. The remaining issues are the current-date bridge, peer comparability, working-capital reconciliation, and final student judgment. I would monitor revenue growth, operating margins, cash conversion, and debt after future releases. Until those uncertainties are better supported, I would monitor PepsiCo rather than recommend an immediate purchase."),
]
for label, text in parts:
    story.append(Paragraph(label, cue))
    story.append(Paragraph(text, body))

story += [Spacer(1, 3), Paragraph("After recording", h), Paragraph("Watch the recording once. Make a transcript from what you actually said, then correct only substantive finance terms, names, and numbers before saving it as the Video 1 transcript.", body)]

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=0.55*inch, leftMargin=0.55*inch, topMargin=0.42*inch, bottomMargin=0.42*inch, title="Video 1 Script - Oladapo Olaniyan")
doc.build(story)
print(OUT)
