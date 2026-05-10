from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


# =========================
# PDF GENERATOR
# =========================
def generate_pdf(profile, avg, weighted, final_score):

    file_name = f"{profile['student_id']}_report.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)

    styles = getSampleStyleSheet()
    content = []

    # =========================
    # TITLE
    # =========================
    content.append(Paragraph("Academic Advisor Report :)", styles["Title"]))
    content.append(Spacer(1, 12))

    # =========================
    # STUDENT INFO
    # =========================
    content.append(Paragraph(f"Student ID: {profile['student_id']}", styles["Normal"]))
    content.append(Paragraph(f"Major: {profile['major']}", styles["Normal"]))
    content.append(Paragraph(f"Year: {profile['year']}", styles["Normal"]))

    content.append(Spacer(1, 12))

    # =========================
    # SCORES
    # =========================
    content.append(Paragraph(f"GPA: {profile['gpa']}", styles["Normal"]))
    content.append(Paragraph(f"Average: {round(avg, 2)}", styles["Normal"]))
    content.append(Paragraph(f"Weighted Average: {round(weighted, 2)}", styles["Normal"]))
    content.append(Paragraph(f"Final Score: {round(final_score, 2)}", styles["Normal"]))

    content.append(Spacer(1, 12))

    # =========================
    # WARNINGS
    # =========================
    content.append(Paragraph("Warnings:", styles["Heading2"]))
    for w in profile.get("rules", {}).get("warnings", []):
        content.append(Paragraph(f"- {w}", styles["Normal"]))

    content.append(Spacer(1, 12))

    # =========================
    # RECOMMENDATIONS
    # =========================
    content.append(Paragraph("Recommendations:", styles["Heading2"]))
    for r in profile.get("rules", {}).get("recommendations", []):
        content.append(Paragraph(f"- {r}", styles["Normal"]))

    # =========================
    # BUILD PDF
    # =========================
    doc.build(content)

    return file_name