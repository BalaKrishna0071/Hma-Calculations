from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Float, MetaData, Table
import os

# Loading environment variables
load_dotenv()
hostname = os.getenv('HOSTNAME')
dbname = os.getenv('DNAME')
username = os.getenv('UNAME')
password = os.getenv('PASSWORD')

# Creating engine
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{hostname}/{dbname}",
    isolation_level="AUTOCOMMIT"
)

metadata_obj = MetaData()

data = Table(
    "data",
    metadata_obj,
    Column("input", Float),
    Column("change", Float),
    Column("gain", Float),
    Column("loss", Float),
    Column("avg_gain", Float),
    Column("avg_loss", Float),
    Column("hm", Float),
    Column("hma", Float),
)

metadata_obj.create_all(engine)

# Inserting Data into DB
def insert_data(input_data):
    with engine.connect() as conn:
        try:
            if isinstance(input_data, list):
                conn.execute(data.insert(), input_data)
            elif isinstance(input_data, dict):
                conn.execute(data.insert(), [input_data])
            else:
                 print("Input data must be a dictionary or list of dictionaries")
        except Exception as e:
            print(f"Error inserting data: {e}")
