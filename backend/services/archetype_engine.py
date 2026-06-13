def predict_archetype(results): 

   if not results:
        return "The Balanced Listener 🎧"

   emotion_scores = {}

   for item in results:

        emotion = item["emotion"].lower()
        confidence = item["confidence"]

        emotion_scores[emotion] = (
            emotion_scores.get(emotion, 0)
            + confidence
        )

   sorted_emotions = sorted(
       emotion_scores.items(),
       key=lambda x: x[1],
       reverse=True 
   )

   primary = sorted_emotions[0][0]

   secondary =(
       sorted_emotions[1][0]
       if len(sorted_emotions) > 1
       else None

   )

   archetypes = {
        "sadness": "The 3AM Overthinker 🌙",
        "joy": "The Party Animal 🎉",
        "anger": "The Rage Monster 😤",
        "love": "The Hopeless Romantic 💘",
        "fear": "The Midnight Thinker 🌌",
        "neutral": "The Chill Observer 😎",
        "surprise": "The Chaos Explorer 🎭",
        "disgust": "The Unfiltered Critic 🧐" ,
        "dark": "The Gothic Dreamer 🖤" ,
       "obsession": "The Future Star ⭐",
     "confidence": "The Main Character 🎬",
       "healing": "The Survivor 💚",
     "conflict": "The Walking Red Flag 🚩",
     "surprise": "The Chaos Explorer 🎭",
     "disgust": "The Unfiltered Critic 🧐", 
   } 

   if primary == "dark" and secondary == "obessison":
       return "The Fame Monster 👑"
   
   if primary == "confidence" and secondary == "joy":
    return "The Spotlight Chaser ✨"

   if primary == "love" and secondary == "sadness":
    return "The Heartbroken Poet 🌹"

   if primary == "dark" and secondary == "confidence":
    return "The Villain Arc 🖤"

   if primary == "healing" and secondary == "sadness":
    return "The Survivor 💚"

   return archetypes.get(
        primary,
        "The Balanced Listener 🎧"
    )