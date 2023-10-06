import sqlalchemy as db
import requests
from bs4 import BeautifulSoup

engine = db.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = db.MetaData()

def ensure_table(engine, table_name, headers):
    inspector = db.inspect(engine)

    if not inspector.has_table(table_name):
        metadata = db.MetaData()
        columns = [db.Column(header.lower(), db.String(255)) for header in headers if header.strip()]
        table = db.Table(table_name, metadata, *columns)
        metadata.create_all(engine)
    else:
        print(table_name + ' ' + "exist")

# Parsing table from URL which will return the parsed table as an array of rows
def parse_table(url):
    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html.parser')
    table = s.find("table", class_='wikitable sortable')

    # Extract headers
    header_row = table.find("tr", class_='is-sticky')
    headers = [header.text.strip().lower() for header in header_row.find_all(["th", "td"])]
    titles = header_row.get_text().strip().replace('\n', ',')

    # Datas of each row
    data = []
    for row in table.find_all("tr")[1:]:
        # Extract text from each cell in the row
        cells = row.find_all(["td", "th"])
        row_data = {header.lower(): cell.get_text(strip=True) for header, cell in zip(headers, cells)}
        data.append(row_data)
        for i in data:
            print(i)

    return headers, data

# Function to store data in a dynamically created table in the SQLite database
def storing_to_table(engine, list_of_items, table_name, headers):
    # Create the table dynamically based on headers
    columns = [db.Column(header.lower(), db.String(255)) for header in headers if header.strip()]

    table = db.Table(table_name, metadata, *columns)
    metadata.create_all(engine)

    # Insert data into the table
    conn.execute(table.insert(), list_of_items)

# Ensure the table exists in the database
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
headers, data = parse_table(url)
ensure_table(engine, 'countries_list', headers)

# Store data in the database table
storing_to_table(engine, data, 'countries_list', headers)
