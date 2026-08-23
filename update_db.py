import sqlite3

DB_PATH = "data/db/productivity.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def column_exists(table_name, column_name):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    return any(
        column[1] == column_name
        for column in columns
    )


def add_column(table_name, column_name, column_definition):

    if not column_exists(table_name, column_name):

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_definition}
            """
        )

        print(
            f"✅ Added {table_name}.{column_name}"
        )

    else:

        print(
            f"ℹ️ {table_name}.{column_name} already exists"
        )


# ============================================================
# TASK COLUMNS
# ============================================================

add_column(
    "tasks",
    "reminder_24h_sent",
    "BOOLEAN DEFAULT 0"
)

add_column(
    "tasks",
    "reminder_2h_sent",
    "BOOLEAN DEFAULT 0"
)

add_column(
    "tasks",
    "reminder_30m_sent",
    "BOOLEAN DEFAULT 0"
)


# ============================================================
# NEW CAREER TABLES
# ============================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS internships (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        company_name TEXT NOT NULL,

        role TEXT NOT NULL,

        description TEXT,

        location TEXT,

        work_mode TEXT,

        skills TEXT,

        application_deadline DATE,

        interview_date DATE,

        application_url TEXT,

        status TEXT DEFAULT 'Saved',

        FOREIGN KEY(user_id)
            REFERENCES users(id)
    )
    """
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS internship_applications (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        internship_id INTEGER NOT NULL,

        applied_date DATE,

        status TEXT DEFAULT 'Applied',

        interview_date DATE,

        notes TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(id),

        FOREIGN KEY(internship_id)
            REFERENCES internships(id)
    )
    """
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS preparation_tasks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        internship_id INTEGER NOT NULL,

        title TEXT NOT NULL,

        description TEXT,

        category TEXT,

        priority TEXT DEFAULT 'Medium',

        duration INTEGER DEFAULT 30,

        preparation_date DATE,

        completed BOOLEAN DEFAULT 0,

        FOREIGN KEY(user_id)
            REFERENCES users(id),

        FOREIGN KEY(internship_id)
            REFERENCES internships(id)
    )
    """
)


# ============================================================
# REWARDS
# ============================================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS rewards (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        points INTEGER DEFAULT 0,

        reason TEXT NOT NULL,

        created_at DATE,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
    )
    """
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS user_rewards (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE NOT NULL,

        total_points INTEGER DEFAULT 0,

        current_streak INTEGER DEFAULT 0,

        longest_streak INTEGER DEFAULT 0,

        FOREIGN KEY(user_id)
            REFERENCES users(id)
    )
    """
)


conn.commit()

conn.close()

print()
print("======================================")
print("✅ Database updated successfully")
print("======================================")