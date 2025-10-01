import psycopg2
from dotenv import load_dotenv
import os

# Load .env if present (does nothing if file not found)
load_dotenv()

DB_NAME = os.getenv("DB_NAME", os.getenv("PGDATABASE", "duke_restaurants"))
DB_USER = os.getenv("DB_USER", os.getenv("PGUSER", "vscode"))
DB_PASSWORD = os.getenv("DB_PASSWORD", os.getenv("PGPASSWORD", "vscode"))
# In devcontainer, host is 'db'; on your laptop use 'localhost'
DB_HOST = os.getenv("DB_HOST", os.getenv("PGHOST", "localhost"))
DB_PORT = os.getenv("DB_PORT", os.getenv("PGPORT", "5432"))
def main():
    print(f"Connecting to {DB_NAME} at {DB_HOST}:{DB_PORT} as {DB_USER} ...")
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute('''
    SELECT name, distance_miles
    FROM restaurants
    WHERE distance_miles < 2.1
    ORDER BY distance_miles
    ''')
    print("Closest restaurants:", cur.fetchall())

    cur.execute('''
    SELECT *
    FROM restaurants
    ORDER BY rating DESC
    LIMIT 3;
    ''')
    print("Top ranked restaurants:", cur.fetchall())
    cur.execute('''
    SELECT name, avg_cost * .075 as cost_with_tax
    FROM restaurants
    ''')
    print("Restaurants with tax:", cur.fetchall())
    cur.execute('''
    SELECT cuisine , COUNT(*) as count_per_cuisine
    FROM restaurants
    GROUP BY cuisine
    ORDER BY count_per_cuisine
    ''')
    print("Count per cuisine:", cur.fetchall())

    cur.execute('''
    SELECT *
    FROM restaurants
    ''')
    print("All restaurants:", cur.fetchall())
    conn.commit()
    cur.close()
    conn.close()
    print("\nDone.")

if __name__ == "__main__":
    main()