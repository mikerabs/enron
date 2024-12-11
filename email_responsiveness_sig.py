import csv
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import networkx as nx
csv.field_size_limit(sys.maxsize)

# Define the list of emails of interest
emails_of_interest = [
    "kenneth.lay@enron.com",
    "Kenneth Lay/Corp/Enron@ENRON",
    "Kenneth Lay@ENRON_DEVELOPMENT",
    "jeffrey.skilling@enron.com",
    "raymond.bowen@enron.com",
    "michael.brown@enron.com",
    "richard.causey@enron.com",
    "Richard Causey/Corp/Enron@ENRON",
    "dave.delainey@enron.com",
    "james.derrick@enron.com",
    "Andrew S Fastow/Enron@EnronXGate",
    "mark.frevert@enron.com",
    "Mark Frevert@Enron",
    "Mark Frevert/NA/Enron@Enron",
    "ben.glisan@enron.com",
    "Ben Glisan/HOU/ECT@ECT",
    "stanley.horton@enron.com",
    "Stanley Horton/Corp/Enron@ENRON",
    "louise.kitchen@enron.com",
    "Louise Kitchen/LON/ECT@ECT",
    "mark.koenig@enron.com",
    "john.lavorato@enron.co",
    "danny.mccarty@enron.com",
    "Danny McCarty/ET&S/Enron@Enron",
    "mike.mcconnell@enron.com",
    "Mike McConnell/HOU/ECT@ECT",
    "rebecca.mcdonald@enron.com",
    "jeffrey.mcmahon@enron.com",
    "greg.piper@enron.com",
    "Greg Piper/Corp/Enron@Enron",
    "Ken Rice/Enron Communications",
    "jeffrey.shankman@enron.com",
    "Jeffrey A Shankman/ENRON@enronXgate",
    "jeffrey.sherrick@enron.com",
    "John Sherriff/LON/ECT@ECT",
    "vince.kaminski@enron.com",
    "Vince J Kaminski/HOU/ECT@ECT"
]

# Load the email data from CSV
csv_file_path = 'enron_emails_550k.csv'
email_df = pd.read_csv(csv_file_path)

# Convert the 'Date' column to datetime format
email_df['Date'] = pd.to_datetime(email_df['Date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)

# Drop rows with invalid dates
email_df = email_df.dropna(subset=['Date'])

# Create a dictionary to store response times
response_times = {}

# Iterate through the emails to calculate response times
for _, row in email_df.iterrows():
    if pd.notna(row['From']) and pd.notna(row['To']) and pd.notna(row['Date']):
        sender = row['From']
        recipients = [email.strip() for email in row['To'].split(',') if email.strip()]
        email_date = row['Date']

        # Check if any recipient or the sender is in the list of significant emails
        involved_significant = sender in emails_of_interest or any(recipient in emails_of_interest for recipient in recipients)

        if involved_significant:
            for recipient in recipients:
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

# Sort by average response time
avg_response_times_sorted = sorted(avg_response_times, key=lambda x: x[1])

# Print the results
print("Ranked Response Times:")
for rank, (pair, avg_time, count) in enumerate(avg_response_times_sorted, 1):
    sender, recipient = pair
    print(f"{rank}. Pair: {sender} <-> {recipient}, Avg. Response Time: {avg_time:.2f} hours, Emails Exchanged: {count}")
