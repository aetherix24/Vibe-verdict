import random 

ARCHETYPE_ROASTS ={
    "The Fame Monster 👑":[
        "You treat fame like a personality trait.",
        "Your playlist wants attention and it gets it.",
        "Lady Gaga would probably approve."
    ],
    "The Villain Arc 🖤": [
        "Your playlist sounds like a final boss introduction.",
        "You don't enter rooms. You make entrances."
    ],

    "The Spotlight Chaser ✨": [
        "Your playlist behaves like every day is an award show.",
        "Your songs already wrote an acceptance speech."
    ],

    "The Heartbroken Poet 🌹": [
        "Your playlist has written more love letters than Shakespeare.",
        "You romanticize pain professionally."
    ],

    "The Survivor 💚": [
        "Your playlist fell down seven times and got up eight.",
        "Emotional damage couldn't stop you."
    ]
}
def generate_roast(archetype, analysis):  

    if not analysis:
        return "No songs detected."

    #Average confidence 
    avg_confidence = sum(
        item["confidence"] for item in analysis 

    ) / len(analysis) 

    #Count emotions 
    emotion_counts = {} 

    for item in analysis:

        emotion = item["emotion"] 

        emotion_counts[emotion] = (
            emotion_counts.get(emotion,0) + 1 
        )
    
    dominant_emotion = max(
        emotion_counts, 
        key=emotion_counts.get 
    ) 

    songs_text = " ".join( 
        item["song"].lower()
        for item in analysis
    )  

    if archetype in ARCHETYPE_ROASTS:

        roast = random.choice(
            ARCHETYPE_ROASTS[archetype]
        )

        return(
            f"{random.choice(openers)}"
            f"{roast}"
            f"{random.choice(closers)}"
        )

    # Dynamic sentence pools 

    openers = [
        "After a deep AI investigation...",
        "Our emotion engine has finished judging you.",
        "Analysis complete.",
        "The playlist scanner has returned a verdict.",
        "After carefully reviewing the evidence..."
    ] 

    closers = [
        "Please use this information responsibly.",
        "Your headphones deserve a raise.",
        "Spotify is taking notes.",
        "The AI is mildly concerned.",
        "No further questions."
    ] 
    
    # Song-specific roasts 
    if "numb" in songs_text: 
        roast = random.choice([
          "At this point your playlist needs a hug more than an equalizer 💀",
            "You treat emotional damage like a music genre 😭",
            "Your playlist has entered the sadness hall of fame."  
        ])

        return f"{random.choice(openers)} {roast} {random.choice(closers)}"
    
    if "another love" in songs_text:
        roast = random.choice([
            "You replay heartbreak like it's a subscription service 😭",
            "Your playlist has experienced more breakups than reality TV.",
            "You and emotional damage seem very familiar with each other."
        ])

        return f"{random.choice(openers)} {roast} {random.choice(closers)}"
    
    # Emotion-based roasts 
    if dominant_emotion == "sadness": 

        if avg_confidence > 0.75: 

            roast = random.choice([
                "Your playlist isn't sad. It's an emotional support animal 💀",
                "Your songs sound like rainy windows and unresolved feelings.",
                "Even the AI wants to check if you're okay."
            ]) 
        else:
             
             roast = random.choice([
                 "You collect heartbreak songs like rare Pokémon cards 😭",
                "Your playlist could power an entire breakup montage.",
                "You seem emotionally sponsored by sadness."
             ]) 

        return f"{random.choice(openers)} {roast} {random.choice(closers)}" 
        
    elif dominant_emotion == "joy": 

           roast = random.choice([
            "Your playlist has enough energy to power a music festival 🎉",
            "You treat every day like a celebration.",
            "Your songs are basically caffeine in audio form." 
           ])

           return f"{random.choice(openers)} {roast} {random.choice(closers)}" 
    
    elif dominant_emotion == "anger":

     roast = random.choice([
        "Your headphones are basically battle armor 😤",
        "Your playlist sounds ready for a boss fight.",
        "You don't listen to music. You prepare for war."
    ]) 
     return f"{random.choice(openers)} {roast} {random.choice(closers)}"
    elif dominant_emotion == "love": 
         
          roast = random.choice([
            "Cupid personally curates your playlist 💘",
            "Your songs contain enough romance for three movies.",
            "Your playlist has a stronger love life than most people."
          ]) 

          return f"{random.choice(openers)} {roast} {random.choice(closers)}" 
    

    elif dominant_emotion == "obsession":

     roast = random.choice([
        "Your playlist screams main-character energy and future fame. ⭐",
        "You're not listening to music, you're preparing for your acceptance speech.",
        "Every song sounds like a step toward world domination.",
        "Your playlist has more ambition than most startup founders.",
        "You don't chase dreams — you put them on repeat.",
        "Some people enjoy music. You seem to be building a legacy."
    ]) 

     return f"{random.choice(openers)} {roast} {random.choice(closers)}" 
    
    elif dominant_emotion == "dark":

      roast = random.choice([
        "Your playlist belongs in a haunted cathedral at midnight. 🕯️",
        "Even the shadows find your music unsettling.",
        "Your songs could make a funeral feel like a party by comparison.",
        "Dracula called — he wants his soundtrack back. 🦇",
        "Your playlist doesn't have listeners, it has victims.",
        "The void looked into your music and flinched."
    ])

      return f"{random.choice(openers)} {roast} {random.choice(closers)}"  
    
    elif dominant_emotion == "confidence":

        roast = random.choice([
        "Your playlist walks into a room before you do. 😎",
        "Your songs have enough confidence to intimidate a mirror.",
        "Every track sounds like a personal victory lap.",
        "Your playlist doesn't ask for attention — it demands it.",
        "Even your headphones think they're famous.",
        "You treat every day like it's your movie trailer."
    ])

        return f"{random.choice(openers)} {roast} {random.choice(closers)}"  

    elif dominant_emotion == "healing":

     roast = random.choice([
        "Your playlist feels like emotional therapy with a soundtrack. 🌈",
        "These songs didn't break you — they rebuilt you.",
        "Your music taste radiates growth and second chances.",
        "Your playlist has survived things it refuses to talk about.",
        "Every song sounds like a comeback story in progress.",
        "Your headphones deserve a counseling license."
    ])
        
     return f"{random.choice(openers)} {roast} {random.choice(closers)}"   
    
    elif dominant_emotion == "conflict":

     roast = random.choice([
        "Your playlist has more red flags than a Formula 1 race. 🚩",
        "Every song sounds like a bad decision with great background music.",
        "Your music taste thrives on chaos and questionable choices.",
        "Your playlist could start an argument in an empty room.",
        "These songs feel like emotional damage with premium audio quality.",
        "Your headphones witness more drama than reality television."
    ])
     
     return f"{random.choice(openers)} {roast} {random.choice(closers)}" 
       
    return (
         f"{random.choice(openers)}" 
         f"Your music taste remains a mystery to science :)" 
         f"{random.choice(closers)}"
    )