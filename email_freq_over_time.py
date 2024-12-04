import pandas as pd
import matplotlib.pyplot as plt

# Load the email data from CSV
csv_file_path = 'enron_emails_550k.csv'
email_df = pd.read_csv(csv_file_path)

# Convert the 'Date' column to datetime format, using utc=True to handle mixed timezones
email_df['Date'] = pd.to_datetime(email_df['Date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)

# Drop rows with invalid dates
email_df = email_df.dropna(subset=['Date'])

# Extract year and month for grouping
email_df['YearMonth'] = email_df['Date'].dt.to_period('M')

# Group emails by month and count the number of emails sent per month
email_frequency = email_df['YearMonth'].value_counts().sort_index()

# Plot the email frequency over time as a histogram
plt.figure(figsize=(15, 8))
#plt.hist(email_df['YearMonth'].astype(str), bins=len(email_frequency.index), color='blue', alpha=0.7)
#plt.hist(email_df['YearMonth'].dt.strftime('%Y-%m'), bins=len(email_frequency.index), color='blue', alpha=0.7)
plt.bar(email_frequency.index.astype(str), email_frequency.values, color='blue', alpha=0.7)
plt.xlabel('Month')
plt.ylabel('Number of Emails Sent')
plt.title('Email Frequency Over Time in Enron Dataset')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('enron_email_frequency.png', bbox_inches='tight')
plt.show()

