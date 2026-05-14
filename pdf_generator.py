from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


# =========================
# PDF GENERATOR
# =========================
def generate_pdf(profile, avg, weighted, final_score):

    file_name = f"{profile.get('student_id', 'unknown')}_report.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)

    styles = getSampleStyleSheet()
    content = []

    # =========================
    # TITLE
    # =========================
    content.append(Paragraph("🎓 Academic Advisor Report", styles["Title"]))
    content.append(Spacer(1, 12))

    # =========================
    # STUDENT INFO
    # =========================
    content.append(Paragraph(f"<b>Student ID:</b> {profile.get('student_id','N/A')}", styles["Normal"]))
    content.append(Paragraph(f"<b>Major:</b> {profile.get('major','N/A')}", styles["Normal"]))
    content.append(Paragraph(f"<b>Year:</b> {profile.get('year','N/A')}", styles["Normal"]))

    content.append(Spacer(1, 12))

    # =========================
    # SCORES
    # =========================
    content.append(Paragraph(f"<b>GPA:</b> {profile.get('gpa','N/A')}", styles["Normal"]))
    content.append(Paragraph(f"<b>Average:</b> {round(avg, 2) if avg else 0}", styles["Normal"]))
    content.append(Paragraph(f"<b>Weighted Average:</b> {round(weighted, 2) if weighted else 0}", styles["Normal"]))
    content.append(Paragraph(f"<b>Final Score:</b> {round(final_score, 2) if final_score else 0}", styles["Normal"]))

    content.append(Spacer(1, 12))

    # =========================
    # WARNINGS
    # =========================
    content.append(Paragraph("⚠️ Warnings:", styles["Heading2"]))

    warnings = profile.get("rules", {}).get("warnings", [])

    if not warnings:
        content.append(Paragraph("- No warnings detected", styles["Normal"]))
    else:
        for w in warnings:
            content.append(Paragraph(f"- {w}", styles["Normal"]))

    content.append(Spacer(1, 12))

    # =========================
    # RECOMMENDATIONS
    # =========================
    content.append(Paragraph("✅ Recommendations:", styles["Heading2"]))

    recommendations = profile.get("rules", {}).get("recommendations", [])

    if not recommendations:
        content.append(Paragraph("- No recommendations", styles["Normal"]))
    else:
        for r in recommendations:
            content.append(Paragraph(f"- {r}", styles["Normal"]))

    # =========================
    # BUILD PDF
    # =========================
    doc.build(content)

    return file_name
