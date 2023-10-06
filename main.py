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
        try:
            metadata.create_all(engine)
        except Exception as e:
            print(f"An error occurred while creating the table {table_name}: {e}")
    else:
        print(table_name + ' ' + "exist")

# Parsing table from URL which will return the parsed table as an array of rows
def parse_table(url):
    try:
            r = requests.get(url)
            s = BeautifulSoup(r.content, 'html.parser')
            table = s.find("table", class_='wikitable sortable')

            # Extract headers
            header_row = table.find("tr", class_='is-sticky')
            if header_row:
                headers = [header.text.strip().lower() for header in header_row.find_all(["th", "td"])]
                print(headers)
                titles = header_row.get_text().strip().replace('\n', ',')
                print(titles)

                # Datas of each row
                data = []
                for row in table.find_all("tr")[1:]:
                    # Extract text from each cell in the row
                    cells = row.find_all(["td", "th"])
                    row_data = {header.lower(): cell.get_text(strip=True) for header, cell in zip(headers, cells)}
                    data.append(row_data)
                for row in data:
                    country = row.get('country / dependency')  # Adapt to the actual headers in your table
                    population = row.get('population')
                    print(f'Country: {country},   Population: {population}')

                return headers, data
            else:
                raise ValueError("Header row not found in the table.")
    except Exception as e:
        print(f"An error occurred while parsing the table: {e}")

    # Return None if an error occurred
    return None, None


# Function to store data in a dynamically created table in the SQLite database
def storing_to_table(engine, data, table_name, headers):
    try:
        # Extract 'Country' and 'Population' from each row
        country_population_data = [{'country': row.get('country / dependency'), 'population': row.get('population')} for row in data]

        # Create the table dynamically based on headers
        columns = [db.Column(header.lower(), db.String(255)) for header in headers if header.strip()]
        table = db.Table(table_name, metadata, *columns)
        metadata.create_all(engine)

        # Insert data into the table
        conn.execute(table.insert(), country_population_data)
        print("Data inserted into table '{table_name}' successfully.")
    except Exception as e:
        print(f"An error occurred while storing data to the table: {e}")
# Ensure the table exists in the database
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
headers, data = parse_table(url)
ensure_table(engine, 'countries_list', headers)

# Store data in the database table
storing_to_table(engine, data, 'countries_list',headers)
