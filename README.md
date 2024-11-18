# enron
Analysis of the Enron Email Network Using Graph-Based Techniques


## Files
- ~/repos/github.com/mikerabs/enron/load_data.py = loads into dataframe, first draft
- ~/repos/github.com/mikerabs/enron/load_database.py = loads into MySQL, but only ones from inbox, sent mail, sent_items, sent, etc.
- ~/repos/github.com/mikerabs/enron/load_database_all.py = Final copy of the loading file into MySQL, gets all files from all folders, includes folders from maildir in folder_path column


## Libraries Used
os
pandas 
email - idt this one anymore 
mysql-connector-python
networkx
matplotlib
scipy
