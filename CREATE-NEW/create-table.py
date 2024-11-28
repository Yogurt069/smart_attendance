import pymysql

# Replace with your MySQL credentials
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="auto1976bot"
)


if connection:
    print("Connected to MySQL server")
    cursor = connection.cursor()

    # Step 1: Create the Database and Table
    cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_db")
    cursor.execute("USE attendance_db")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            sr_number INT AUTO_INCREMENT PRIMARY KEY,
            registration_number VARCHAR(20) UNIQUE NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            attendance_status VARCHAR(20) DEFAULT "Absent"
        )
    """)
    print("Database and table created successfully.")