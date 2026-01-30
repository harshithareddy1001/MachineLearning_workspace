import pandas as pd
from sqlalchemy import create_engine#A library to interact with databases. create_engine is used to connect Python to a database (SQLite in this case).

# Create SQLite engine
engine = create_engine('sqlite:///loan_applications.db', echo=False)

def save_application(df: pd.DataFrame):
    """
    Save loan application to database
    """
    df.to_sql('loan_applications', con=engine, if_exists='append', index=False)

def load_applications():
    """
    Load all applications from database
    """
    try:
        df = pd.read_sql('loan_applications', con=engine)
        return df
    except Exception:
        return pd.DataFrame()  # return empty if DB not exists
