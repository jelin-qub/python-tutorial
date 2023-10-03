import sqlalchemy as db
engine = db.create_engine('sqlite:///datacamp.sqlite')
conn = engine.connect()
metadata = db.MetaData()

l1=[{'country':'india','population':50000},{'country':'nepal','population':40000}]
def store_to_table(engine,list_of_items,table_name):
    table_name = db.Table(table_name, metadata,
                         db.Column('country', db.String(255), primary_key=True),
                         db.Column('population', db.Integer(), nullable=False)
                         )
    metadata.create_all(engine)

    for i in list_of_items:
        query = db.insert(table_name).values(country=i['country'], population=i['population'])
        conn.execute(query)
    select_query = table_name.select()
    result = conn.execute(select_query).fetchall()
    print(result)
    conn.close()
store_to_table(engine,l1,'countries')

def ensure_table(engine,table_name):
    inspector = db.inspect(engine)

    if not inspector.has_table(table_name):
        metadata = db.MetaData()
        table = db.Table(table_name, metadata,
                         db.Column('country', db.String(255), primary_key=True),
                         db.Column('population', db.Integer(), nullable=False)
                         )
        metadata.create_all(engine)
    else:
        print(table_name + ' ' + "exist")

ensure_table(engine,'countries1')
ensure_table(engine,'countries')
ensure_table(engine,'apple')