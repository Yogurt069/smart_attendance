import pymysql
import os

# Establish MySQL connection using pymysql
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="auto1976bot",
    database="attendance_db"
)
try:
    cursor = conn.cursor()

    # Path to the file containing attendance data
    file_path = 'user_registration.txt'

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the file content
        with open(file_path, 'r') as file:
            attendance_data = file.read()

        # Split the data by lines and process each line
        lines = attendance_data.strip().split('\n')

        for line in lines:
            registration_number, attendance_status = line.split(': ')
            
            # SQL query to update attendance
            sql = "UPDATE attendance SET attendance_status = %s WHERE registration_number = %s"
            cursor.execute(sql, (attendance_status, registration_number))
        
    # Commit the changes to the database
        conn.commit()
        print("Attendance updated successfully.")
    else:
        print(f"The file {file_path} does not exist.")

except pymysql.Error as error:
    print(f"Error: {error}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("\nMySQL connection closed.")
