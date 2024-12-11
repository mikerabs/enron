import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain  # Import Louvain community detection

# Load the email data from CSV
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

# Calculate top in-degree and out-degree nodes
in_degree_top = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)[:10]
out_degree_top = sorted(G.out_degree(), key=lambda x: x[1], reverse=True)[:10]

print("Top 10 In-Degree Nodes:")
for node, degree in in_degree_top:
    print(f"Node: {node}, In-Degree: {degree}")

print("\nTop 10 Out-Degree Nodes:")
for node, degree in out_degree_top:
    print(f"Node: {node}, Out-Degree: {degree}")

# Convert the directed graph to an undirected graph for community detection
G_undirected = G.to_undirected()

# Filter nodes by degree (keep nodes with degree > 50)
degree_threshold = 400
#250 = 0.35
#100 = 0.43
#150 = 0.38
#350 = 0.31
#400 = 0.32
significant_nodes = [node for node, degree in G_undirected.degree() if degree > degree_threshold]
G_filtered = G_undirected.subgraph(significant_nodes)

# Apply Louvain community detection
communities = community_louvain.best_partition(G_filtered)

# Add modularity calculation
modularity_score = community_louvain.modularity(communities, G_filtered)

# Print the modularity score
print(f"Modularity Score: {modularity_score:.2f}")

# Extract unique communities and assign a color to each node based on its community
num_communities = len(set(communities.values()))
colors = [communities[node] for node in G_filtered.nodes()]

# Plot the filtered network with community coloring
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G_filtered, k=0.5, iterations=50)
nx.draw_networkx_nodes(G_filtered, pos, node_size=50, alpha=0.9, node_color=colors, cmap=plt.cm.rainbow)
nx.draw_networkx_edges(G_filtered, pos, alpha=0.3, arrows=False)
nx.draw_networkx_labels(G_filtered, pos, font_size=6, font_family='sans-serif', alpha=0.8)

plt.title("Communities in Enron Email Network")
plt.axis('off')
plt.savefig('enron_communities.png', bbox_inches='tight')
plt.show()

# Print a summary of communities
community_summary = {}
for node, community in communities.items():
    if community not in community_summary:
        community_summary[community] = []
    community_summary[community].append(node)

for community, members in community_summary.items():
    print(f"Community {community} has {len(members)} members")
    print("Members:")
    for member in members:
        if G.has_edge(member, member):
            print(f"{member} *")  # Mark self-referential members with a star
        else:
            print(member)
    print()
