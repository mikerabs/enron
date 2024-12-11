import csv
import sys
csv.field_size_limit(sys.maxsize)

# List of names to find emails for
names = [
    #"Kenneth Lay",
    #"klay"
    #"Jeffrey Skilling",
    #"Raymond Bowen",
    #"Michael Brown",
    #"Richard Buy",
    #"Richard Causey",
    #"Dave Delainey",
    #"James Derrick",
    #"Andrew Fastow",
    #"Mark Frevert",
    #"Ben Glisan",
    #"Stanley Horton",
    #"Louise Kitchen",
    #"Mark Koenig",
    #"John Lavorato",
    #"Daniel Leff",
    #"Danny McCarty",
    #"Mike McConnell",
    #"Rebecca McDonald",
    #"Jeffrey McMahon",
    #"J. Mark Metts",
   # "Greg Piper",
    #"Kenneth Rice",
    #"Jeffrey Shankman",
    #"Jeffrey Sherrick",
    #"John Sherriff"
    "Vincent Kaminski",
    "Vince Kaminski"
]

# Create a dictionary to store emails linked to these names
emails_dict = {name: set() for name in names}

# Open the CSV file and read its content
with open('enron_emails_550k.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        # Check if the sender matches the names we're interested in
        from_name = row['X-From'].strip().replace('"', '')
        for name in names:
            if name == from_name:
                emails_dict[name].add(row['From'])
                break

        # Check if any of the recipients match the names we're interested in
        to_names = row['X-To'].strip().replace('"', '').split(',')
        for to_name in to_names:
            to_name = to_name.strip()
            for name in names:
                if name == to_name:
                    emails_dict[name].add(row['To'])
                    break

# Print the emails for each of the names
for name, emails in emails_dict.items():
    print(f"{name}:")
    for email in emails:
        print(f"- {email}")
    print("\n")
