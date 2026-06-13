import psycopg2 
import json 
 
conn = psycopg2.connect(
    dbname="musicpersonality_roaster",
    user="atherix" ,
    password="24281",
    host="localhost",
    port="5432"  
) 

def save_roast(songs , archetype, roast):
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