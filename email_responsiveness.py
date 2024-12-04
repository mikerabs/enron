import pandas as pd
import numpy as np
from datetime import datetime

# Load the email data from CSV
csv_file_path = 'enron_emails_550k.csv'
email_df = pd.read_csv(csv_file_path)

# Convert the 'Date' column to datetime format, using utc=True to handle mixed timezones
email_df['Date'] = pd.to_datetime(email_df['Date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)

# Drop rows with invalid dates
email_df = email_df.dropna(subset=['Date'])

# Filter by date range (July 2000 to July 2001)
start_date = '2000-07-01'
end_date = '2001-07-31'
filtered_df = email_df[(email_df['Date'] >= start_date) & (email_df['Date'] <= end_date)]

# Create a dictionary to store response times
response_times = {}

# Iterate through the filtered emails to calculate response times
for _, row in filtered_df.iterrows():
    if pd.notna(row['From']) and pd.notna(row['To']) and pd.notna(row['Date']):
        sender = row['From']
        recipients = row['To'].split(',')
        email_date = row['Date']
        
        for recipient in recipients:
            recipient = recipient.strip()
            if recipient and sender != recipient:  # Exclude self-referential emails
                pair = tuple(sorted([sender, recipient]))
                
                if pair not in response_times:
                    response_times[pair] = []
                
                response_times[pair].append(email_date)

# Calculate average response times for each communication pair
avg_response_times = []

for pair, dates in response_times.items():
    if len(dates) > 1:
        # Sort dates to calculate time differences
        sorted_dates = sorted(dates)
        diffs = [
            (sorted_dates[i + 1] - sorted_dates[i]).total_seconds() / 3600  # Difference in hours
            for i in range(len(sorted_dates) - 1)
        ]
        avg_response_time = np.mean(diffs)
        avg_response_times.append((pair, avg_response_time, len(dates)))

# Filter pairs with at least x number of emails exchanged (e.g., 50 emails)
x = 10
significant_pairs = [pair for pair in avg_response_times if pair[2] >= x]

# Sort by average response time
significant_pairs_sorted = sorted(significant_pairs, key=lambda x: x[1])

# Print the results
print("Significant Communication Pairs (at least {} emails exchanged):\n".format(x))
for pair, avg_time, count in significant_pairs_sorted:
    sender, recipient = pair
    print(f"Pair: {sender} <-> {recipient}, Avg. Response Time: {avg_time:.2f} hours, Emails Exchanged: {count}")

