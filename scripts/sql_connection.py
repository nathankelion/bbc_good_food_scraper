# Code for establishing a connection to SQL database
import os
from sqlalchemy import create_engine

# Check if running in GitHub Actions environment
if 'GITHUB_ACTIONS' in os.environ:
    # Access repository secrets directly
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
else:
    # Load database variables from .env file
    from dotenv import load_dotenv
    load_dotenv()

    # Access database variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

# Create a SQLAlchemy engine
connection_string = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server&fast_executemany=True"
engine = create_engine(connection_string)

# Create a connection object
Conn = engine.connect()