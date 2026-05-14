import streamlit as st
from subjects import subjects_by_major
from pdf_generator import generate_pdf
from config import TOTAL_MAJOR_HOURS

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Academic Advisor System",
    page_icon="🎓",
    layout="centered"
)

# =========================
# SESSION STATE INIT
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1

if "student_data" not in st.session_state:
    st.session_state.student_data = {}

if "selected_subjects" not in st.session_state:
    st.session_state.selected_subjects = []

if "grades" not in st.session_state:
    st.session_state.grades = {}

# =========================
# PREMIUM CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #1b1b24, #0f0f14);
    color: white;
    font-family: 'Arial';
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 16px;
    color: #c7a7b3;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.stButton > button {
    background: linear-gradient(135deg, #c7a7b3, #7a2a3a);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(199,167,179,0.4);
}

label {
    color: #c7a7b3 !important;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<div class='main-title'>🎓 Academic Advisor System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>  </div>", unsafe_allow_html=True)


# =====================================================
# STEP 1: STUDENT INFO + SUBJECT SELECTION
# =====================================================
if st.session_state.step == 1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Student Information")

    student_id = st.text_input("Student ID")
    gpa = st.number_input("GPA", 0.0, 100.0, step=0.1)
    year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])

    # ✅ Major from data مباشرة (no hardcoding)
    major = st.selectbox("Major", list(subjects_by_major.keys()))

    # 🔒 حماية إضافية
    if major not in subjects_by_major:
        st.error("Invalid major selected")
        st.stop()

    # 🔄 reset subjects when major changes
    if "last_major" not in st.session_state:
        st.session_state.last_major = major

    if st.session_state.last_major != major:
        st.session_state.selected_subjects = []
        st.session_state.last_major = major

    st.markdown("</div>", unsafe_allow_html=True)

    # =================================================
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📚 Select Completed Subjects")
    
    major_subjects = subjects_by_major.get(major, {})

    if "Mandatory" not in major_subjects:
    
        selected_subjects = st.multiselect(
            "📚 Choose Completed Subjects:",
            list(major_subjects.keys())
        )
    else:
    
        mandatory_subjects = major_subjects.get("Mandatory", {})
        optional_subjects = major_subjects.get("Optional", {})
    
        selected_mandatory = st.multiselect(
            "✅ Completed Mandatory Subjects:",
            list(mandatory_subjects.keys())
        )
    
        selected_optional = st.multiselect(
            "⭐ Completed Optional Subjects:",
            list(optional_subjects.keys())
        )
    
        selected_subjects = selected_mandatory + selected_optional
    st.markdown("</div>", unsafe_allow_html=True)

    # =================================================
    if st.button("Next ➡️ Enter Grades"):

        if student_id.strip() == "":
            st.error("Please enter Student ID!")

        elif len(selected_subjects) == 0:
            st.error("Please select at least one subject!")

        else:
            st.session_state.student_data = {
                "student_id": student_id,
                "gpa": gpa,
                "year": year,
                "major": major
            }

            st.session_state.selected_subjects = selected_subjects
            st.session_state.step = 2

            st.rerun()
# =====================================================
# STEP 2: ENTER GRADES
# =====================================================
elif st.session_state.step == 2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Enter Grades for Selected Subjects")

    grades = {}

    for subject in st.session_state.selected_subjects:
        grades[subject] = st.number_input(f"{subject} Grade", 0.0, 100.0, step=1.0)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next ➡️ Generate Report"):
            st.session_state.grades = grades
            st.session_state.step = 3
            st.rerun()


# =====================================================
# STEP 3: REPORT + PDF
# =====================================================
elif st.session_state.step == 3:

    data = st.session_state.student_data
    grades = st.session_state.grades

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Final Report")

    st.write("👤 Student ID:", data["student_id"])
    st.write("📚 Major:", data["major"])
    st.write("📈 GPA:", data["gpa"])
    st.write("📌 Year:", data["year"])

    # =========================
    # HOURS CALCULATION
    # =========================

    if len(st.session_state.selected_subjects) == 0:
        st.error("No subjects selected")
        st.stop()

    major_subjects = subjects_by_major[data["major"]]
    mandatory_subjects = major_subjects.get("Mandatory", {})
    optional_subjects = major_subjects.get("Optional", {})

    all_subjects = {**mandatory_subjects, **optional_subjects}

    taken_hours = sum(
        all_subjects[sub]
        for sub in st.session_state.selected_subjects
    )

    remaining_hours = TOTAL_MAJOR_HOURS - taken_hours

    progress = taken_hours / TOTAL_MAJOR_HOURS if TOTAL_MAJOR_HOURS > 0 else 0

    st.markdown("### 🎓 Degree Progress")
    st.write(f"📌 Completed Hours: {taken_hours}")
    st.write(f"📊 Total Required Hours: {TOTAL_MAJOR_HOURS}")
    st.write(f"⏳ Remaining Hours: {remaining_hours}")

    st.progress(progress)
    st.write(f"📈 Progress: {progress*100:.2f}%")
   
    # =========================
    # GRADES
    # =========================
    st.markdown("### ✅ Subjects & Grades")

    total = 0
    count = 0

    for subject, grade in grades.items():
        st.write(f"✔️ {subject} → {grade}")
        total += grade
        count += 1

    avg = total / count if count > 0 else 0
    st.markdown(f"### ⭐ Average Grade: **{avg:.2f}**")

    # =========================
    # RULES
    # =========================
    warnings = []
    recommendations = []

    if data["gpa"] < 60:
        warnings.append("Your GPA is below 60. You are at risk of academic probation.")
        recommendations.append("Meet your academic advisor as soon as possible.")

    if avg < 70:
        warnings.append("Your average grade is below 70. Your performance needs improvement.")
        recommendations.append("Focus on weak subjects and revise weekly.")

    for subject, grade in grades.items():
        if grade < 50:
            warnings.append(f"You failed {subject}.")
            recommendations.append(f"Consider repeating {subject} next semester.")

    if len(warnings) == 0:
        warnings.append("No major warnings detected.")
        recommendations.append("Keep up the good work and maintain your performance.")

    st.markdown("### ⚠️ Warnings")
    for w in warnings:
        st.warning(w)

    st.markdown("### ✅ Recommendations")
    for r in recommendations:
        st.info(r)

    # STATUS
    if avg >= 85:
        st.success("Excellent Performance 🟢")
    elif avg >= 70:
        st.warning("Good Performance 🟡")
    else:
        st.error("At Risk 🔴")

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # SAVE RULES INSIDE PROFILE
    # =========================
    data["rules"] = {
        "warnings": warnings,
        "recommendations": recommendations
    }

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back to Grades"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("📄 Generate PDF Report"):

            weighted = avg
            final_score = (avg + data["gpa"]) / 2

            pdf_file = generate_pdf(data, avg, weighted, final_score)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
