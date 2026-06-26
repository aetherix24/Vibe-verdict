from fastapi import FastAPI 
from pydantic import BaseModel   
from fastapi.middleware.cors import CORSMiddleware

from services.nlp_service  import analyze_songs 
from services.archetype_engine import predict_archetype
from services.roast_generator import generate_roast 
from database import save_roast 
import psycopg2 
from data.archetype_descriptions import( 
    ARCHETYPE_DESCRIPTIONS , get_archetype_description
) 
from dotenv import load_dotenv 
import os 
load_dotenv()

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins =[
    "https://vibeverdict.netlify.app"
    ], 
    allow_credentials = True ,
    allow_methods = ["*"],
    allow_headers=["*"],
) 

def get_db_connection():
    return psycopg2.connect(
        os.getenv("DB_HOST"),
        sslmode="require"
    
    )

@app.get("/community")
def get_community():
    conn= get_db_connection()
    cur = conn.cursor() 

    cur.execute(""" 
             SELECT archetype, COUNT(*)
                FROM roast_history
                Group by archetype
                ORDER BY COUNT(*) DESC;
                """)
    
    rows = cur.fetchall() 

    cur.close()
    conn.close() 

    return {
        "community":[
            {
                "rank": idx + 1,
                "archetype": row[0], 
                "count": row[1]}
            for idx, row in enumerate(rows)
        ]
    } 
@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()

    # Total roasts
    cur.execute(
        "SELECT COUNT(*) FROM roast_history"
    )
    total_roasts = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(
                SUM(jsonb_array_length(songs)),
                0
                )
                FROM roast_history
                """) 
    total_songs = cur.fetchone()[0]

    # Top archetype
    cur.execute("""
        SELECT archetype, COUNT(*)
        FROM roast_history
        GROUP BY archetype
        ORDER BY COUNT(*) DESC
        LIMIT 1 
    """)
    top_row = cur.fetchone()

    top_archetype = (
        top_row[0] if top_row else "None Yet"
    )

    cur.close()
    conn.close() 

    return {
        "total_roasts": total_roasts,
        "total_songs": total_songs,
        "top_archetype": top_archetype
    }
@app.get("/health")
def health():
    return{"status":"ok"}

@app.post("/react/{reaction_type}")
def react(reaction_type: str): 
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
            UPDATE myapp.reactions
            SET count = count + 1
            WHERE reaction_type = %s
                """, (reaction_type,)) 
    
    conn.commit() 

    cur.close()
    conn.close()

    return {"success": True} 

@app.get("/reactions")
def get_reactions():
    conn = get_db_connection()
    cur = conn.cursor() 

    cur.execute("""
            SELECT reaction_type , count 
                from myapp.reactions
                order by count DESC
        """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return{
        "reactions": [
            {
                "reaction_type": row[0],
                "count":row[1]
            }
            for row in rows 
        ]
    } 

class SongRequest(BaseModel):
    songs: list[str] 

@app.get("/") 
def home(): 
    return {
        "message"  : "Spotify Roaster API 🔥" 
    } 
@app.post("/analyze")
def analyze_music(data: SongRequest):

    songs = data.songs 

    if len(songs) == 0:
        return {
            "error": "Please enter at least one song."
        }
    if len(songs) > 5:
        return {
            "error": "Maximum 5 songs allowed."
        }
    # NLP analysis 
    analysis = analyze_songs(songs) 

    # Archetype prediction 
    archetype = predict_archetype(analysis) 

    description = get_archetype_description(
        archetype,
    )
    

    # Roast generation 
    roast = generate_roast(archetype, analysis)
    
    save_roast(
        songs,
        archetype,
        roast
    )
    
    emotion_scores = {}

    for item in analysis:
        emotion =item["emotion"]
        confidence = item["confidence"]

        emotion_scores[emotion] =(
            emotion_scores.get(emotion ,0)
            + confidence
        )
    
    dominant_emotion = max(
        emotion_scores,
        key=emotion_scores.get
    )
    return {
     "songs_received": songs ,
      "analysis": analysis ,
        "archetype": archetype ,
        "description": description,
        "dominant_emotion": dominant_emotion,
        "roast": roast

}



    