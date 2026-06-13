import psycopg2 
import json 
import os 
from dotenv import load_dotenv 

 
def get_db_connection(): 
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
def save_roast(songs , archetype, roast):
    conn =get_db_connection()
    try:
        cur = conn.cursor() 
           
        cur.execute(
                 """ 
        INSERT INTO roast_history (songs, archetype ,roast)
        values ( %s , %s , %s)
        """,
        (
              json.dumps(songs),
              archetype,
              roast
        )
    )

        conn.commit() 
        cur.close() 
    
    except Exception  as e: 
        conn.rollback()
        print("Database Error:",e)