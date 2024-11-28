import pymysql

# Replace with your MySQL credentials
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="auto1976bot",
    database="attendance_db"
)

try:
    if connection:
        print("Connected to MySQL server")
        cursor = connection.cursor()


        # Fetch all rows to verify insertion
        cursor.execute("SELECT * FROM attendance")
        rows = cursor.fetchall()

        if not rows:
            print("No data found in the table.")
        else:
            print(f"\n{'Sr. Number':<10} {'Registration Number':<20} {'Full Name':<25} {'Attendance':<10}")
            print("-" * 65)
            for row in rows:
                sr_number, registration_number, full_name, attendance_status = row
                print(f"{sr_number:<10} {registration_number:<20} {full_name:<25} {attendance_status or 'Null':<10}")

except pymysql.Error as error:
    print(f"Error: {error}")

finally:
    if connection:
        cursor.close()
        connection.close()
        print("\nMySQL connection closed.")
