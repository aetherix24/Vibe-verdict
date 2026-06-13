from transformers import pipeline 
from sentence_transformers import SentenceTransformer 
from data.song_database import SONG_DATABASE
 
# Emotion classification model 
emotion_classifier = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base"
) 

# Embedding model 
embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
) 

# Music -aware emotion themes 
sad_themes = [
    "numb",
     "alone",
    "lonely",
    "broken",
    "cry",
    "tears",
    "goodbye",
    "dark",
    "hurt",
    "ghost",
    "another love",
    "someone like you"
]

happy_themes = [
    "happy",
    "party",
    "dance",
    "celebrate",
    "fun",
    "shine",
    "smile",
    "dynamite",
    "heal",
    "healer"
]
anger_themes = [
    "rage",
    "monster",
    "enemy",
    "kill",
    "war",
    "pain"
]

love_themes = [
    "love",
    "heart",
    "romance",
    "kiss",
    "forever"
]

def analyze_songs(song_list):

    results = [] 

    for song in song_list:  

        lower_song = song.lower()

           # Check song database first
        song_info = SONG_DATABASE.get(lower_song)

        if song_info: 
         emotion = song_info["emotion"]
         confidence = 1.0

        else:

            # Emotion prediction (Base AI production)
            emotion_result = emotion_classifier(song)[0]

            emotion = emotion_result["label"]
            confidence = round(emotion_result["score"],2)  

        # Music Enhancement Layer 

        if any(theme in lower_song for theme in sad_themes):
            emotion = "sadness"  
            confidence = max(confidence,0.90)
        
        elif any(theme in lower_song for theme in happy_themes):
            emotion = "joy" 
            confidence = max(confidence,0.90)
        elif any(theme in lower_song for theme in anger_themes): 
            emotion = "anger" 
            confidence = max(confidence,0.90)
        elif any(theme in lower_song for theme in love_themes): 
            emotion = "love"
            confidence = max(confidence,0.90)
        # Embedding generation 
        embedding = embedding_model.encode(song).tolist()

        results.append({
        "song": song ,
        "emotion": emotion ,
        "genre":(
            song_info["genre"]
            if song_info 
            else "unknown"
        ),
        "source": "database" if song_info else "ai",
        "confidence": confidence ,
        "embedding_dimension":len(embedding)
    })

    return results 