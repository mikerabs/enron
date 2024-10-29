import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# directory of the Enron dataset ON YOUR MACHINE
base_dir = "maildir/"

# Connect to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='RabsSQL44', 
            database='enron_emails'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Create tables in the MySQL database
def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Emails (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message_id VARCHAR(255) UNIQUE,
                date VARCHAR(255),
                subject VARCHAR(255),
                mime_version VARCHAR(255),
                content_type VARCHAR(255),
                content_transfer_encoding VARCHAR(255),
                x_folder VARCHAR(255),
                x_origin VARCHAR(255),
                x_filename VARCHAR(255),
                content TEXT
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Senders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_id INT,
                sender VARCHAR(255),
                FOREIGN KEY (email_id) REFERENCES Emails(id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Receivers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_id INT,
                receiver VARCHAR(255),
                FOREIGN KEY (email_id) REFERENCES Emails(id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cc (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_id INT,
                cc VARCHAR(255),
                FOREIGN KEY (email_id) REFERENCES Emails(id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Bcc (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_id INT,
                bcc VARCHAR(255),
                FOREIGN KEY (email_id) REFERENCES Emails(id)
            );
        ''')
        connection.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"Error while creating tables: {e}")

# Insert data into MySQL tables
def insert_data(connection, email_data):
    try:
        cursor = connection.cursor()
        email_query = '''
            INSERT INTO Emails (message_id, date, subject, mime_version, content_type, content_transfer_encoding, x_folder, x_origin, x_filename, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE message_id=message_id;
        '''
        cursor.execute(email_query, (
            email_data['Message-ID'], email_data['Date'], email_data['Subject'], email_data['Mime-Version'],
            email_data['Content-Type'], email_data['Content-Transfer-Encoding'], email_data['X-Folder'],
            email_data['X-Origin'], email_data['X-FileName'], email_data['Content']
        ))
        email_id = cursor.lastrowid
        if email_id == 0:
            cursor.execute('SELECT id FROM Emails WHERE message_id = %s', (email_data['Message-ID'],))
            result = cursor.fetchone()
            email_id = result[0] if result else 0

        if email_data['From']:
            cursor.execute('INSERT INTO Senders (email_id, sender) VALUES (%s, %s)', (email_id, email_data['From']))

        if email_data['To']:
            receivers = email_data['To'].split(',')
            for receiver in receivers:
                cursor.execute('INSERT INTO Receivers (email_id, receiver) VALUES (%s, %s)', (email_id, receiver.strip()))

        if email_data['X-cc']:
            ccs = email_data['X-cc'].split(',')
            for cc in ccs:
                cursor.execute('INSERT INTO Cc (email_id, cc) VALUES (%s, %s)', (email_id, cc.strip()))

        if email_data['X-bcc']:
            bccs = email_data['X-bcc'].split(',')
            for bcc in bccs:
                cursor.execute('INSERT INTO Bcc (email_id, bcc) VALUES (%s, %s)', (email_id, bcc.strip()))

        connection.commit()
    except Error as e:
        print(f"Error while inserting data: {e}")

# Recursive function to traverse folders and parse emails
def process_folder(folder_path, connection):
    print(f"Processing folder: {folder_path}")
    if not os.path.exists(folder_path):
        print(f"Warning: Folder does not exist - {folder_path}")
        return

    for root, _, files in os.walk(folder_path):
        # Filter for relevant email folders only
        if any(folder in root for folder in ["_sent_mail", "inbox", "sent", "sent_items"]):
            for email_file in files:
                email_path = os.path.join(root, email_file)
                if not os.path.isfile(email_path):
                    continue

                print(f"Processing file: {email_file}")
                try:
                    with open(email_path, 'r', encoding='utf-8', errors='replace') as f:
                        lines = f.readlines()
                except UnicodeDecodeError as e:
                    print(f"Error reading file {email_file}: {e}")
                    continue

                # Extract metadata from the email
                message_id = date = sender = receiver = subject = mime_version = content_type = content_transfer_encoding = x_from = x_to = x_cc = x_bcc = x_folder = x_origin = x_filename = content = None
                message_content = []
                content_start = False
                for line in lines:
                    line = line.strip()
                    if line.startswith("Message-ID:"):
                        message_id = line[len("Message-ID:"):].strip()
                    elif line.startswith("Date:"):
                        date = line[len("Date:"):].strip()
                    elif line.startswith("From:"):
                        sender = line[len("From:"):].strip()
                    elif line.startswith("To:"):
                        receiver = line[len("To:"):].strip()
                    elif line.startswith("Subject:"):
                        subject = line[len("Subject:"):].strip()
                    elif line.startswith("Mime-Version:"):
                        mime_version = line[len("Mime-Version:"):].strip()
                    elif line.startswith("Content-Type:"):
                        content_type = line[len("Content-Type:"):].strip()
                    elif line.startswith("Content-Transfer-Encoding:"):
                        content_transfer_encoding = line[len("Content-Transfer-Encoding:"):].strip()
                    elif line.startswith("X-From:"):
                        x_from = line[len("X-From:"):].strip()
                    elif line.startswith("X-To:"):
                        x_to = line[len("X-To:"):].strip()
                    elif line.startswith("X-cc:"):
                        x_cc = line[len("X-cc:"):].strip()
                    elif line.startswith("X-bcc:"):
                        x_bcc = line[len("X-bcc:"):].strip()
                    elif line.startswith("X-Folder:"):
                        x_folder = line[len("X-Folder:"):].strip()
                    elif line.startswith("X-Origin:"):
                        x_origin = line[len("X-Origin:"):].strip()
                    elif line.startswith("X-FileName:"):
                        x_filename = line[len("X-FileName:"):].strip()
                    elif line == "":
                        # Empty line signifies end of headers
                        content_start = True
                    elif content_start:
                        message_content.append(line)

                content = "\n".join(message_content)

                # Check for missing fields
                if not message_id:
                    print(f"Warning: Missing Message-ID for file {email_file}")

                # Create email data dictionary
                email_data = {
                    'Message-ID': message_id,
                    'Date': date,
                    'From': sender,
                    'To': receiver,
                    'Subject': subject,
                    'Mime-Version': mime_version,
                    'Content-Type': content_type,
                    'Content-Transfer-Encoding': content_transfer_encoding,
                    'X-From': x_from,
                    'X-To': x_to,
                    'X-cc': x_cc,
                    'X-bcc': x_bcc,
                    'X-Folder': x_folder,
                    'X-Origin': x_origin,
                    'X-FileName': x_filename,
                    'Content': content
                }

                # Insert data into MySQL
                insert_data(connection, email_data)

# Main 
connection = create_connection()
if connection:
    create_tables(connection)
    process_folder(base_dir, connection)
    connection.close()


