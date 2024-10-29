import os
import pandas as pd

# Define the base directory of the Enron dataset
base_dir = 'maildir/'

# Initialize an empty DataFrame to store email data
columns = ['Message-ID', 'Date', 'From', 'To', 'Subject', 'Mime-Version', 'Content-Type', 'Content-Transfer-Encoding', 'X-From', 'X-To', 'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName', 'Content']
df = pd.DataFrame(columns=columns)

# Recursive function to traverse folders and parse emails
for folder_path, _, files in os.walk(base_dir):
    print(f"Processing folder: {folder_path}")
    if not os.path.exists(folder_path):
        print(f"Warning: Folder does not exist - {folder_path}")
        continue

    # Filter for relevant email folders only
    if any(folder in folder_path for folder in ["_sent_mail", "inbox", "sent", "sent_items"]):
        for email_file in files:
            email_path = os.path.join(folder_path, email_file)
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

            df = pd.concat([df, pd.DataFrame([{
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
            }])], ignore_index=True)

print(df.head())

