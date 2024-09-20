import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()

def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                       )'''
                   )

    # calllogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS calllogs (
                        callId INTEGER PRIMARY KEY,
                        phoneNumber TEXT,
                        startTime INTEGER,
                        endTime INTEGER,
                        direction TEXT,
                        userId INTEGER,
                        FOREIGN KEY (userId) REFERENCES users(userId)
                      )'''
                   )
    

    # Load users and call logs from CSVs and write analytics
    load_and_clean_users("../../resources/users.csv")
    load_and_clean_call_logs("../../resources/callLogs.csv")
    write_user_analytics("../../resources/userAnalytics.csv")
    write_ordered_calls("../../resources/orderedCalls.csv")

    # Close the cursor and connection
    cursor.close()
    conn.close()

# Load users data and clean incomplete records
def load_and_clean_users(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check for missing data
            if row['userId'] and row['firstName'] and row['lastName']:  # Skip rows with missing data
                cursor.execute('''
                    INSERT INTO users (userId, firstName, lastName) VALUES (?, ?, ?)
                ''', (row['userId'], row['firstName'], row['lastName']))
# Load call logs data and clean incomplete records
def load_and_clean_call_logs(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check for missing data
            if row['callId'] and row['phoneNumber'] and row['startTime'] and row['endTime'] and row['direction'] and row['userId']:  # Skip rows with missing data
                cursor.execute('''
                    INSERT INTO calllogs (callId, phoneNumber, startTime, endTime, direction, userId) VALUES (?, ?, ?, ?, ?, ?)
                ''', (row['callId'], row['phoneNumber'], row['startTime'], row['endTime'], row['direction'], row['userId']))

# Write user analytics to CSV
def write_user_analytics(csv_file_path):
    cursor.execute('''
        SELECT userId, AVG(endTime - startTime) AS avgDuration, COUNT(callId) AS numCalls
        FROM calllogs
        GROUP BY userId
    ''')

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['userId', 'avgDuration', 'numCalls'])
        
        # Fetch all rows and write them to the CSV
        for row in cursor:
            writer.writerow(row)

# Write ordered call logs to CSV
def write_ordered_calls(csv_file_path):
    cursor.execute('''
        SELECT * FROM calllogs ORDER BY userId, startTime
    ''')

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['callId', 'phoneNumber', 'startTime', 'endTime', 'direction', 'userId'])
        
        # Fetch all rows and write them to the CSV
        for row in cursor:
            writer.writerow(row)

# Debug/Validation - Uncomment this function in main() to see data in database
# no need to touch this functions below !--------------------------------

def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # New line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("--------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM calllogs''')
    for row in cursor:
        print(row)

# If the script is run directly, call main function
if __name__ == '__main__':
    main()
