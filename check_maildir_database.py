import os
file_count = 0

def process_folder(folder_path):
    global file_count
    print(f"Processing folder: {folder_path}")
    if not os.path.exists(folder_path):
        print(f"Warning: Folder does not exist - {folder_path}")
        return

    for root, _, files in os.walk(folder_path):
        # Filter for relevant email folders only
        if any(folder in root for folder in ["_sent_mail", "inbox", "sent", "sent_items"]):
            for email_file in files:
                file_count += 1  

process_folder("./maildir")
print(f"File count:\t{file_count}")
