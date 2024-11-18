import os
import csv

# Define the base directory of the Enron dataset
base_dir = 'maildir/'

# Define the CSV file to save the data
csv_file_path = 'enron_emails_100k.csv'

# Define the columns for the CSV file
columns = [
    'Message-ID', 'Date', 'From', 'To', 'Subject', 'Mime-Version', 'Content-Type',
    'Content-Transfer-Encoding', 'X-From', 'X-To', 'X-cc', 'X-bcc', 'X-Folder',
    'X-Origin', 'X-FileName', 'Folder-Path', 'Content'
]

# Recursive function to traverse folders and parse emails
def process_folder(folder_path):
    data = []
    email_count = 0
    email_thresh = 100000
    for root, _, files in os.walk(folder_path):
        folder_path_relative = os.path.relpath(root, base_dir)
        for email_file in files:
            if email_count >= email_thresh:
                return data

            email_path = os.path.join(root, email_file)
            if not os.path.isfile(email_path):
                continue

            print(f"Processing file: {email_file}")
            print(f"File path: {email_path}")
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
                'Folder-Path': folder_path_relative,
                'Content': content
            }

            # Skip rows where most fields are empty
            if any(email_data[col] for col in columns[:-2]):  # Exclude 'Folder-Path' and 'Content'
                # Append email data to list
                data.append(email_data)
                email_count += 1

    return data

# Main script
def main():
    # Traverse the maildir folder and parse the first 5 emails
    email_data_list = process_folder(base_dir)

    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(email_data_list)

    print(f"Email data successfully written to {csv_file_path}")

if __name__ == "__main__":
    main()

