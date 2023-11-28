from scripts.sql_connection import Conn, engine
import pandas as pd

# SQL Query
def SQL_query(query):
    result_proxy = Conn.execute(query)
    result_df = pd.DataFrame(result_proxy.fetchall(), columns=result_proxy.keys())
    engine.dispose
    return result_df

# Count Query
def count_recipes(result_df):
    recipe_count = len(result_df)
    return recipe_count