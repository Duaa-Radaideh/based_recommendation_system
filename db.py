import sqlite3

# =========================
# CONNECTION
# =========================
conn = sqlite3.connect("advisor.db", check_same_thread=False)
cursor = conn.cursor()

# =========================
# HELPERS
# =========================
def table_exists(table_name):
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (table_name,))
    return cursor.fetchone() is not None


def get_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [col[1] for col in cursor.fetchall()]


def column_exists(table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns


# =========================
# MIGRATION
# =========================
def migrate_database():

    cursor.execute("PRAGMA foreign_keys = ON;")
    conn.commit()

    # -------------------------
    # STUDENTS TABLE
    # -------------------------
    if not table_exists("students"):
        cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE,
            gpa REAL,
            year TEXT,
            major TEXT,
            completed_hours INTEGER DEFAULT 0
        )
        """)
        conn.commit()
    else:
        if not column_exists("students", "completed_hours"):
            cursor.execute("ALTER TABLE students ADD COLUMN completed_hours INTEGER DEFAULT 0")
        if not column_exists("students", "major"):
            cursor.execute("ALTER TABLE students ADD COLUMN major TEXT")
        if not column_exists("students", "year"):
            cursor.execute("ALTER TABLE students ADD COLUMN year TEXT")
        if not column_exists("students", "gpa"):
            cursor.execute("ALTER TABLE students ADD COLUMN gpa REAL")

        conn.commit()

    # -------------------------
    # GRADES TABLE
    # -------------------------
    if not table_exists("grades"):
        cursor.execute("""
        CREATE TABLE grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            subject TEXT,
            mark REAL,
            hours INTEGER,
            UNIQUE(student_id, subject),
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
        """)
        conn.commit()
    else:
        if not column_exists("grades", "hours"):
            cursor.execute("ALTER TABLE grades ADD COLUMN hours INTEGER DEFAULT 3")
        if not column_exists("grades", "mark"):
            cursor.execute("ALTER TABLE grades ADD COLUMN mark REAL")
        if not column_exists("grades", "subject"):
            cursor.execute("ALTER TABLE grades ADD COLUMN subject TEXT")

        conn.commit()


# =========================
# CRUD FUNCTIONS
# =========================
def add_student(student_id, gpa, year, major, completed_hours):

    cursor.execute("""
    INSERT OR REPLACE INTO students (student_id, gpa, year, major, completed_hours)
    VALUES (?, ?, ?, ?, ?)
    """, (student_id, gpa, year, major, completed_hours))

    conn.commit()


def add_grade(student_id, subject, mark, hours):

    cursor.execute("""
    INSERT OR REPLACE INTO grades (student_id, subject, mark, hours)
    VALUES (?, ?, ?, ?)
    """, (student_id, subject, mark, hours))

    conn.commit()


def get_average(student_id):

    cursor.execute("""
    SELECT AVG(mark) FROM grades WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()[0]
    return result if result else 0


def get_all_grades(student_id):

    cursor.execute("""
    SELECT subject, mark, hours FROM grades WHERE student_id = ?
    """, (student_id,))

    return cursor.fetchall()
