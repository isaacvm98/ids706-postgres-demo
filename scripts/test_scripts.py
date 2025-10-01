import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

# Load .env if present (does nothing if file not found)
load_dotenv()

DB_NAME = os.getenv("DB_NAME", os.getenv("PGDATABASE", "duke_restaurants"))
DB_USER = os.getenv("DB_USER", os.getenv("PGUSER", "vscode"))
DB_PASSWORD = os.getenv("DB_PASSWORD", os.getenv("PGPASSWORD", "vscode"))
# In devcontainer, host is 'db'; on your laptop use 'localhost'
DB_HOST = os.getenv("DB_HOST", os.getenv("PGHOST", "localhost"))
DB_PORT = os.getenv("DB_PORT", os.getenv("PGPORT", "5432"))

def execute_and_display(cur, query, description):
    """Execute a query and display it with results as a DataFrame"""
    print(f"\n{'='*60}")
    print(f"Query: {description}")
    print(f"{'='*60}")
    print(query.strip())
    print(f"{'-'*60}")
    
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    
    df = pd.DataFrame(rows, columns=columns)
    print(df.to_string(index=False))
    print()

def main():
    print(f"Connecting to {DB_NAME} at {DB_HOST}:{DB_PORT} as {DB_USER} ...\n")
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    # Query 1: Closest restaurants
    execute_and_display(
        cur,
        '''
        SELECT name, distance_miles
        FROM restaurants
        WHERE distance_miles < 2.1
        ORDER BY distance_miles
        ''',
        "Closest restaurants (< 2.1 miles)"
    )

    # Query 2: Top ranked restaurants
    execute_and_display(
        cur,
        '''
        SELECT *
        FROM restaurants
        ORDER BY rating DESC
        LIMIT 3
        ''',
        "Top 3 ranked restaurants"
    )

    # Query 3: Restaurants with tax
    execute_and_display(
        cur,
        '''
        SELECT name, avg_cost * 0.075 as cost_with_tax
        FROM restaurants
        ''',
        "Restaurants with tax (7.5%)"
    )

    # Query 4: Count per cuisine
    execute_and_display(
        cur,
        '''
        SELECT cuisine, COUNT(*) as count_per_cuisine
        FROM restaurants
        GROUP BY cuisine
        ORDER BY count_per_cuisine
        ''',
        "Count per cuisine type"
    )

    # Query 5: All restaurants
    execute_and_display(
        cur,
        '''
        SELECT *
        FROM restaurants
        ''',
        "All restaurants"
    )

    conn.commit()
    cur.close()
    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    main()