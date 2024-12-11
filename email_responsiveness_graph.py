import csv
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
csv.field_size_limit(sys.maxsize)

# Load the email data from CSV
csv_file_path = 'enron_emails_550k.csv'
email_df = pd.read_csv(csv_file_path)

# Convert the 'Date' column to datetime format
email_df['Date'] = pd.to_datetime(email_df['Date'], format='%a, %d %b %Y %H:%M:%S %z', errors='coerce', utc=True)

# Drop rows with invalid dates
email_df = email_df.dropna(subset=['Date'])

# Create a graph
G = nx.DiGraph()

# Create a dictionary to store response times
response_times = {}

# Iterate through the emails to calculate response times
for _, row in email_df.iterrows():
    if pd.notna(row['From']) and pd.notna(row['To']) and pd.notna(row['Date']):
        sender = row['From']
        recipients = [email.strip() for email in row['To'].split(',') if email.strip()]
        email_date = row['Date']

        for recipient in recipients:
            pair = tuple(sorted([sender, recipient]))

            if pair not in response_times:
                response_times[pair] = []

            response_times[pair].append(email_date)

# Add edges to the graph with weights as average response times
for pair, dates in response_times.items():
    if len(dates) > 1:
        # Sort dates to calculate time differences
        sorted_dates = sorted(dates)
        diffs = [
            (sorted_dates[i + 1] - sorted_dates[i]).total_seconds() / 3600  # Difference in hours
            for i in range(len(sorted_dates) - 1)
        ]
        avg_response_time = np.mean(diffs)
        sender, recipient = pair
        G.add_edge(sender, recipient, weight=avg_response_time)

# Filter nodes by degree threshold
degree_threshold = 5
filtered_nodes = [node for node, degree in G.degree() if degree > degree_threshold]
G_filtered = G.subgraph(filtered_nodes)

# Draw the graph
pos = nx.spring_layout(G_filtered, k=0.5, iterations=50)
plt.figure(figsize=(15, 15))
nx.draw_networkx_nodes(G_filtered, pos, node_size=50, alpha=0.9)
nx.draw_networkx_edges(G_filtered, pos, alpha=0.3, edge_color='blue')
nx.draw_networkx_labels(G_filtered, pos, font_size=6, font_family='sans-serif')

# Draw edge labels with weights
edge_labels = nx.get_edge_attributes(G_filtered, 'weight')
nx.draw_networkx_edge_labels(G_filtered, pos, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()}, font_size=5)

plt.title("Email Response Times Graph")
plt.axis('off')
plt.savefig('email_response_graph.png', bbox_inches='tight')
plt.show()
