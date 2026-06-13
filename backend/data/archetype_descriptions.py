ARCHETYPE_DESCRIPTIONS = {

    "The Fame Monster 👑":
        "You thrive on ambition, attention and larger-than-life energy.",

    "The Villain Arc 🖤":
        "You love mystery, darkness and powerful aesthetics.",

    "The Spotlight Chaser ✨":
        "Confidence and excitement define your music taste.",

    "The Heartbroken Poet 🌹":
        "You turn emotions and memories into art.",

    "The Survivor 💚":
        "Your playlist reflects healing, growth and resilience.",

    "The Gothic Dreamer 🖤":
        "You find beauty in darkness and emotion.",

    "The Future Star ⭐":
        "You dream big and never stop chasing greatness.",

    "The Main Character 🎬":
        "Your life already feels like a movie soundtrack.",

    "The Party Animal 🎉":
        "You bring energy wherever you go.",

    "The 3AM Overthinker 🌙":
        "You spend more time thinking than sleeping.",

      "The Hopeless Romantic 💘":
        "You see love stories everywhere and feel every lyric deeply.",

    "The Walking Red Flag 🚩":
        "Your playlist survives entirely on chaos, drama and questionable decisions.",

    "The Rage Monster 😤":
        "You channel intensity, passion and raw emotion through music.",

    "The Chill Observer 😎":
        "You stay calm, relaxed and let life unfold around you.",

    "The Midnight Thinker 🌌":
        "Your thoughts become louder after midnight and your playlist knows it.",

    "The Chaos Explorer 🎭":
        "You enjoy unpredictability and never stay in one emotional lane.",

    "The Unfiltered Critic 🧐":
        "You have strong opinions and your playlist isn't afraid to show them."
    
    
} 
def get_archetype_description(archetype):
    return ARCHETYPE_DESCRIPTIONS.get(
        archetype,
        "A unique music listener."
    )