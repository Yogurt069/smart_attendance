import os
import pymysql

# Database connection setup
connection = pymysql.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="auto1976bot",  # Replace with your MySQL password
    database="attendance_db"  # Replace with your database name
)

# Path to the file
file_path = "students.txt"  # Make sure the path is correct

try:
    # Check if the file exists
    if os.path.exists(file_path):
        print(f"File found: {file_path}")

        # Open the file for reading
        with open(file_path, "r") as file:
            lines = file.readlines()

        print("Reading file:")
        # Process each line and insert into MySQL
        cursor = connection.cursor()

        for line in lines:
            line = line.strip()  # Remove extra spaces or newlines
            if ":" in line:  # Ensure line contains the ":" separator
                reg_num, full_name = line.split(":", 1)
                reg_num = reg_num.strip()
                full_name = full_name.strip()
                
                # Insert data into MySQL
                try:
                    insert_query = """
                        INSERT INTO attendance (registration_number, full_name)
                        VALUES (%s, %s)
                    """
                    cursor.execute(insert_query, (reg_num, full_name))
                    print(f"Inserted: {reg_num} - {full_name}")
                except pymysql.MySQLError as e:
                    print(f"Error inserting : Duplicate entry")

        # Commit the transaction
        connection.commit()
        print("\nData population complete.")
    
    else:
        print(f"Error: File not found at {file_path}")

except pymysql.MySQLError as error:
    print(f"Error: {error}")
finally:
    if connection:
        connection.close()
        print("\nMySQL connection closed.")
