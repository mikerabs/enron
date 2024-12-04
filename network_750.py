import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

csv_file_path = 'enron_emails_550k.csv'

email_df = pd.read_csv(csv_file_path)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for _, row in email_df.iterrows():
    if pd.notna(row['From']) and pd.notna(row['To']):
        sender = row['From']
        recipients = row['To'].split(',')
        for recipient in recipients:
            recipient = recipient.strip()
            if recipient:
                G.add_edge(sender, recipient)

# Filter nodes by degree (keep nodes with degree > 50)
degree_threshold = 750
significant_nodes = [node for node, degree in G.degree() if degree > degree_threshold]
G_filtered = G.subgraph(significant_nodes)

# Plot the filtered network
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G_filtered, k=0.15, iterations=20)
nx.draw_networkx_nodes(G_filtered, pos, node_size=50, alpha=0.7)
nx.draw_networkx_edges(G_filtered, pos, alpha=0.3, arrowsize=10)
nx.draw_networkx_labels(G_filtered, pos, font_size=6, font_family='sans-serif', alpha=0.8)

plt.title("Significant Nodes in Enron Email Network")
plt.axis('off')
plt.savefig('significant_nodes_750.png', bbox_inches='tight')
plt.show()
