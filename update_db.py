import sqlite3

conn = sqlite3.connect("data/db/productivity.db")
cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN reminder_24h_sent BOOLEAN DEFAULT 0"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN reminder_2h_sent BOOLEAN DEFAULT 0"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN reminder_30m_sent BOOLEAN DEFAULT 0"
    )
except:
    pass

conn.commit()
conn.close()

print("✅ Database updated successfully.")