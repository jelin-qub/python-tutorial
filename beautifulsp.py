import requests
from bs4 import BeautifulSoup


import sqlalchemy as db
engine = db.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = db.MetaData()


r=requests.get('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population')
s=BeautifulSoup(r.content,'html.parser')

table=s.find("table",class_='wikitable sortable')
# print(table)

# Extract headers
header_row = table.find("tr", class_='is-sticky')
headers = [header.text.strip().lower() for header in header_row.find_all(["th", "td"])]

titles=header_row.get_text().strip().replace('\n',',')
# print([titles])


#datas of each rows
data=[]
for row in table.find_all("tr")[1:]:
    # Extract text from each cell in the row
    cells = row.find_all(["td", "th"])
    row_data = {header.lower(): cell.get_text(strip=True) for header, cell in zip(headers, cells)}
    data.append(row_data)

# Print the scraped data
for i in data:
    pass
    # print(i)

# Function to store data in a dynamically created table in the SQLite database
def store_to_table(engine,list_of_items,table_name,headers):
    # Create the table dynamically based on headers
    columns = [db.Column(header.lower(), db.String(255)) for header in headers if header.strip()]


    #
    table = db.Table(table_name, metadata, *columns)
    metadata.create_all(engine)

    # Insert data into the tablez
    conn.execute(table.insert(), list_of_items)

store_to_table(engine, data, 'countries_list',headers)


#db

