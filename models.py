# =========================
# FEATURE ENGINEERING
# =========================
def extract_features(gpa, weighted_avg, completed_hours):

    gpa_level = "High" if gpa >= 85 else "Medium" if gpa >= 70 else "Low"
    performance = "Excellent" if weighted_avg >= 85 else "Good" if weighted_avg >= 70 else "Weak"

    progress = min((completed_hours / 140) * 100, 100)

    return {
        "gpa_level": gpa_level,
        "performance": performance,
        "progress_percent": round(progress, 2)
    }


# =========================
# RULES ENGINE
# =========================
def apply_rules(gpa, weighted_avg, completed_hours, failed_subjects):

    warnings = []
    recommendations = []

    if gpa < 60:
        warnings.append("Student is at academic risk")

    if weighted_avg < 65:
        warnings.append("Low academic performance detected")

    if completed_hours < 30:
        recommendations.append("Focus on foundation subjects")

    if failed_subjects:
        recommendations.append("Retake failed subjects first")

    return {
        "warnings": warnings,
        "recommendations": recommendations
    }


# =========================
# WEIGHTED AVERAGE
# =========================
def get_weighted_average(grades):

    if not grades:
        return 0

    total = sum(mark * hours for _, mark, hours in grades)
    hours = sum(hours for _, mark, hours in grades)

    return total / hours if hours else 0


# =========================
# STUDENT PROFILE BUILDER
# =========================
def build_student_profile(student_id, student_row, grades):

    # student_row = (id, student_id, gpa, year, major, completed_hours)

    gpa = student_row[2]
    year = student_row[3]
    major = student_row[4]
    completed_hours = student_row[5]

    weighted_avg = get_weighted_average(grades)

    failed_subjects = [s for s, m, h in grades if m < 60]

    features = extract_features(gpa, weighted_avg, completed_hours)
    rules_output = apply_rules(gpa, weighted_avg, completed_hours, failed_subjects)

    return {
        "student_id": student_id,
        "gpa": gpa,
        "year": year,
        "major": major,
        "completed_hours": completed_hours,
        "weighted_avg": weighted_avg,
        "failed_subjects": failed_subjects,
        "features": features,
        "rules": rules_output
    }