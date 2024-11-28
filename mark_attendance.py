import pymysql
import os

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="auto1976bot",
    database="attendance_db"
)
try:
    cursor = conn.cursor()

    file_path = 'user_registration.txt'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            attendance_data = file.read()

        
        lines = attendance_data.strip().split('\n')

        for line in lines:
            registration_number, attendance_status = line.split(': ')
            
            sql = "UPDATE attendance SET attendance_status = %s WHERE registration_number = %s"
            cursor.execute(sql, (attendance_status, registration_number))
        
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
