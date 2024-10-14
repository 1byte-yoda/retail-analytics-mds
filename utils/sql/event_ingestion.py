from .base_queries import EVENTS
import pandas as pd
from sqlalchemy import create_engine
from config.config import host, database, user, password, table_name
from .transformations import fill_customer_country, fill_gender


# Can be Decoupled
def ingest_data():
    '''
    Ingests data into a PostgreSQL database
    '''
    connection_string = f"postgresql://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)

    data = pd.read_csv("data/platform_transactions.csv")
    data = fill_customer_country(data)
    data = fill_gender(data)
    data.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Data saved to {table_name}. The table contains {len(data)} rows.")

    engine.dispose()
