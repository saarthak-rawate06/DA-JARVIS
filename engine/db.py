import sqlite3
import csv

con = sqlite3.connect("jarvis.db") 
cursor = con.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'canva', 'https://www.canva.com/')"
# cursor.execute(query)
# con.commit()

# Create a table with the desired columns
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 20]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
    
#     for row_number, row in enumerate(csvreader, start=1):
#         if len(row) <= max(desired_columns_indices):  # Ensure row has enough columns
        #     print(f"⚠️ Skipping row {row_number}: {row} (Length: {len(row)})")
        #     continue  # Skip rows that are too short

        # selected_data = [row[i] for i in desired_columns_indices]

        # Corrected SQL syntax (column names without quotes)
        # cursor.execute("INSERT INTO contacts (id, name, mobile_no) VALUES (null, ?, ?);", tuple(selected_data))

# Commit changes and close connection
# con.commit()
# con.close()

#searching the name in the database
# query = 'pops'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()

# if results:
#     print(results[0][0])
# else:
#     print("No matching records found.")


#To delete a table
# cursor.execute('''DROP TABLE IF EXISTS contacts''')
# con.commit()
# con.close()
