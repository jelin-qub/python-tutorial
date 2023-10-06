import sqlalchemy as db
engine = db.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = db.MetaData()

import requests
from bs4 import BeautifulSoup

# beautifulsoup scrapping table -----
r=requests.get('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population')
s=BeautifulSoup(r.content,'html.parser')

table=s.find("table",class_='wikitable sortable')
# print(table)

# Extract headers
header_row = table.find("tr", class_='is-sticky')
headers = [header.text.strip().lower() for header in header_row.find_all(["th", "td"])]
titles = header_row.get_text().strip().replace('\n', ',')
# datas of each rows
data = []
for row in table.find_all("tr")[1:]:
    # Extract text from each cell in the row
    cells = row.find_all(["td", "th"])
    row_data = {header.lower(): cell.get_text(strip=True) for header, cell in zip(headers, cells)}
    data.append(row_data)


#parsing table from url which will return the parsed table as array of rows
def parse_table(table):
    titles = header_row.get_text().strip().replace('\n', ',')
    print([titles])
    #datas of each rows
    data=[]
    for row in table.find_all("tr")[1:]:
        # Extract text from each cell in the row
        cells = row.find_all(["td", "th"])
        row_data = {header.lower(): cell.get_text(strip=True) for header, cell in zip(headers, cells)}
        data.append(row_data)
    for i in data:
        print(i)

table = s.find("table", class_='wikitable sortable')
parse_table(table)


# Function to store data in a dynamically created table in the SQLite database
def storing_to_table(engine,list_of_items,table_name,headers):
    # Create the table dynamically based on headers
    columns = [db.Column(header.lower(), db.String(255)) for header in headers if header.strip()]

    table = db.Table(table_name, metadata, *columns)
    metadata.create_all(engine)

    # Insert data into the tablez
    conn.execute(table.insert(), list_of_items)

storing_to_table(engine, data, 'countries_list',headers)




def ensure_table(engine,table_name):
    inspector = db.inspect(engine)

    if not inspector.has_table(table_name):
        metadata = db.MetaData()
        columns = [db.Column(header.lower(), db.String(255)) for header in headers if header.strip()]
        table = db.Table(table_name, metadata, *columns)
        metadata.create_all(engine)
    else:
        print(table_name + ' ' + "exist")

ensure_table(engine,'countries_list')
