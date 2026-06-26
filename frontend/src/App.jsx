import { useState ,useEffect} from "react"; 

const LOADING_STEPS = [
  "🎵 Fetching your songs...",
  "🧠 AI is judging your taste...", 
  "🔥  Generating your roast...",
  "🎭 Calculating your archetype...",
  "⭐ Computing vibe score...",
  "🔥 Generating roast...",
  "✨ Finalizing results..."
]  

function  LoadingMessage() {
    const [step , setStep ] = useState(0) 

    useEffect(() => {
      const interval = setInterval(() =>{
        setStep(prev => (prev + 1) % LOADING_STEPS.length) 
      }, 400) ;
      return () => clearInterval(interval) 
    }, []) ;

    return(
      <p className="text-green-400 text-lg font-semibold animate-pulse">
        {LOADING_STEPS[step]}
      </p>
    );
}

function App() {
  const [result, setResult] = useState(null);
  const [community, setCommunity] = useState([]);
  const [globalStats, setGlobalStats] = useState(null); 
  const [reactions , setReactions] = useState([]);
  const [voteMessage , setVoteMessage] = useState("");
  const [copied , setCopied] = useState(false);
  const[hasVoted , setHasvoted]= useState(false);

  const genres =
  result?.analysis?.map(
    item => item.genre || "unknown"
  ) || [];

const topGenre =
  genres.length > 0
    ? genres
        .sort(
          (a, b) =>
            genres.filter(v => v === a).length -
            genres.filter(v => v === b).length
        )
        .pop()
    : "unknown";

  const dominantEmotion = 
        result?.analysis?.reduce((acc , curr) => {
          acc[curr.emotion] = (acc[curr.emotion] || 0) + 1
          return acc;
        }, {});
  
  const topEmotion =
  dominantEmotion
        ? Object.keys(dominantEmotion).reduce((a,b) => 
            dominantEmotion[a] > dominantEmotion[b]? a:b
      ) 

      : "unknown";

  const [songs, setSongs] = useState([
    "",
    "",
    "",
    "",
    "",
  ]);  

  const [loading , setLoading] = useState(false);  

   const loadCommunityData = async () => {
  try {
    const communityResponse = await fetch(
      "https://vibe-verdict-production.up.railway.app/community"
    );

    const communityData = await communityResponse.json();
    setCommunity(communityData.community);

    const statsResponse = await fetch(
      "https://vibe-verdict-production.up.railway.app/stats"
    );

    const statsData = await statsResponse.json();
    setGlobalStats(statsData);

  } catch (error) {
    console.log(error);
  }
};    

useEffect(() =>{
  loadCommunityData();
  loadReactions();
}, []); 
    const loadReactions = async () => {
  try {
    const response = await fetch(
      "https://vibe-verdict-production.up.railway.app/reactions"
    );

    const data = await response.json();

    setReactions(data.reactions);

  } catch(error) {
    console.log(error);
  }
};
const voteReaction = async (reactionType) => {

  if (hasVoted) {
    setVoteMessage("⚠️ You already voted!");
    return;
  }
  try {

    await fetch(
      `https://vibe-verdict-production.up.railway.app//react/${reactionType}`,
      {
        method: "POST"
      }
    );

    await loadReactions(); 

    setVoteMessage("🔥 Thanks for your feedback!");
    setHasvoted(true);

    setTimeout(() => {
      setVoteMessage(" ");
    }, 3000);

  } catch(error) {
    console.log(error);
    alert("Server error. Please try again.");
  }
};

  const roastPlaylist = async () => {  
    
  if (loading) return;

    setLoading(true); 
    setResult(null); 
  const startTime = Date.now();

    try{
    
      const filteredSongs = songs.filter(
      song => song.trim() !== ""
    ); 
    if(filteredSongs.length == 0) {
      alert("Please enter at least one song.")
      setLoading(false); 
      return;
    }

    const response = await fetch( 
      "https://vibe-verdict-production.up.railway.app/analyze",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          songs: filteredSongs
        })
      }
    );

    const data = await response.json();

 

    const elapsed = Date.now() - startTime ;

    if (elapsed < 5000) {
      await new Promise((resolve) =>
        setTimeout(resolve, 5000 - elapsed)
      );
    }
   setResult(data);

   setTimeout(() =>{
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth"
      
    })
   } ,100);

  } catch(error) {
    console.log(error); 
  } finally {
    setLoading(false)
  } 

};

  return (
    <div className="min-h-screen bg-zinc-950 text-white px-6 py-12">

      {/* Hero */}
      <div className="max-w-3xl mx-auto text-center mb-10">

        <h1 className="text-5xl font-bold text-purple-500 mb-4">
          🎵 Vibe Verdict 
        </h1>

        <p className="text-zinc-400 text-lg">
          Discover your music personality
          Our AI analyzes your favorite songs,
          finds emotional patterns, and roasts you.
        </p>
        <div className="flex flex-wrap justify-center gap-3 mt-6">
          <span className="bg-green-500/10 border border-green-500/20 px-4 py-2 rounded-full text-green-400 hover:-translate-y-1
">
            ⚡ AI Powered
          </span>

          <span className="bg-purple-500/10 border border-purple-500/20 px-4 py-2 rounded-full text-purple-400 hover:-translate-y-1
">
            🎭 Music Archetypes
          </span>

          <span className="bg-orange-500/10 border border-orange-500/20 px-4 py-2 rounded-full text-orange-400  hover:-translate-y-1
">
            🔥 Personalized Roasts
          </span>
        </div>
      </div>    {/* Hero ends here */}

    {/* 3 Column Layout */} 
    <div className="max-w-7xl mx-auto mt-10">
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 items-start">

        {/* LEFT COULMN */} 
        <div className="self-start -translate-y-40 -translate-x-18">

        {/* Community Reactions */} 
        <div className="bg-zinc-900 rounded-3xl p-6 border border-zinc-800">
        <h3 className="text-green-400 font-bold mb-4">
            💬 Community Reactions 
            <p className="text-zinc-400 text-sm mb-4">
  👇 Did the AI get your personality right? Vote below.
</p>
        </h3>
        <div className="space-y-3">
               <div 
               onClick={() => voteReaction("attacked")}
               className="bg-zinc-800 p-3 rounded-xl cursor-pointer hover:bg-zinc-700">
                💀 I Feel Attacked (
                  {reactions.find(r => r.reaction_type === "attacked")?. count || 0}
                ) 
               </div>
               <div
  onClick={() => voteReaction("accurate")}
  className="bg-zinc-800 p-3 rounded-xl cursor-pointer hover:bg-zinc-700"
>
  😂 Accurate (
  {reactions.find(r => r.reaction_type === "accurate")?.count || 0}
  )
</div>

<div
  onClick={() => voteReaction("savage")}
  className="bg-zinc-800 p-3 rounded-xl cursor-pointer hover:bg-zinc-700"
>
  🔥 Savage (
  {reactions.find(r => r.reaction_type === "savage")?.count || 0}
  )
</div>

<div
  onClick={() => voteReaction("lying")}
  className="bg-zinc-800 p-3 rounded-xl cursor-pointer hover:bg-zinc-700"
>
  🤨 AI Is Lying (
  {reactions.find(r => r.reaction_type === "lying")?.count || 0}
  )
</div>
              </div>
     {voteMessage && (
    <div className="mt-4 bg-purple-500/10 border border-purple-500/20 rounded-xl p-3 text-purple-400 text-sm text-center">
      {voteMessage}
    </div>
  )}
            </div>

          </div>

          {/* CENTER COLUMN */}
          <div className="xl:col-span-2">

      {/* Main Card */}
      <div className=" bg-zinc-900 rounded-3xl  p-8  shadow-2xl">

        <h2 className="text-2xl font-semibold mb-2">
          🎵 Your Favorite Songs
        </h2>

        <p className="text-zinc-400 mb-6">
          Enter up to 5 songs you genuinely love.
        </p>

        <div className="space-y-4">

          {songs.map((song, index) => (
            <input
              key={index}
              type="text"
              placeholder={`Favourite Song #${index + 1}`}
              value={song}
              onChange={(e) => {
                const updatedSongs = [...songs];
                updatedSongs[index] = e.target.value;
                setSongs(updatedSongs);
              }}
              className="w-full p-4 rounded-xl bg-zinc-800 border border-zinc-700 focus:outline-none focus:border-green-500 transition duration-300 hover:border-green-400"
            />
          ))}
        </div>

        {/* Tip Card */}
        <div className="mt-6 bg-green-500/10 border border-green-500/20 rounded-xl p-4">

          <p className="text-green-400">
            💡 Tip: Enter songs you genuinely listen to.
            The more personal your playlist, the better the analysis.
          </p>
        </div>

        {/*Button*/}
        <button
          onClick={roastPlaylist}
          className="w-full mt-6 bg-green-500 hover:bg-green-400 text-black font-bold py-4 rounded-xl transition">

         {loading ? "Analyzing...": "🔥 Reveal My Music Personality"}
        </button> 

        {/* Loading */}
        {loading && (
          <div className="mt-10 flex flex-col items-center gap-4 text-center">
          
          {/* Spinner */} 
          <div className="w-12 h-12 border-4 border-green-400 border-t-transparent rounded-full  animate-spin"/> 

          {/* Cycling messages */} 
          <LoadingMessage />
          </div>
        )} 
        

        {result &&  !loading &&(
          <div className="mt-8 bg-zinc-800 rounded-2xl p-6 border border-zinc-700">

            {/* Header */}
            <div className="text-center mb-6">

              <p className="text-zinc-500 uppercase tracking-[0.3em]  text-xs mb-2">
                MUSIC DNA DETECTED
              </p>

              <h2 className="text-4xl font-extrabold text-green-400 mb-4">
                {result.archetype}
              </h2> 

              <p className="itlaic text-zinc-400 mb-4">
                {result.description}
              </p>

              <p className="text-zinc-500 mt-2">
            Your playlist has been classified.
            </p>

            {/* Roast */}
              <div className="bg-zinc-900 border border-green-500/20 rounded-2xl p-5">
              <p className="text-zinc-300 text-lg leading-relaxed">
                {result.roast}
              </p> 

              <button 
              onClick={() => {
                 navigator.clipboard.writeText(result.roast);
                 setCopied(true);

                 setTimeout(() => {
                    setCopied(false);
                 },2000);
              }}

              className="mt-4 px-4 py-2 bg-purple-500 hover:bg-purple-400 text-black rounded-xl font-bold transition"
      disabled={loading}
      className="... disabled:opacity-50 disabled:cursor-not-allowed"        > 
              {copied ? "✅ Copied!" : "📋 Copy Roast"} 
            
              </button>
              </div>  

              
{/* Stats Cards HERE */}
{/* closes text-center section */} 
              <div className={`grid gap-4 mt-6 mb-6 ${
             topGenre !== "unknown" 
             ?"grid-cols-1 md:grid-cols-2 xl:grid-cols-4"
             :"grid-cols-1 md:grid-cols-4"
              }` }
             > 

          {/* Songs */}
  <div className="bg-zinc-900 rounded-2xl p-4 text-center border border-zinc-700 hover:-translate-y-2 hover:shadow-xl transition-all duration-300">
    <div className="text-3xl">🎵</div>
    <div className="text-2xl font-bold">
      {result.analysis.length}
    </div>
    <div className="text-zinc-400 text-sm">
      Songs Analyzed
    </div>
  </div>

   {/* Confidence */}
  <div className="bg-zinc-900 rounded-2xl p-4 text-center border border-zinc-700 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
    <div className="text-3xl">🧠</div>
    <div className="text-2xl font-bold">
      {Math.round(
        result.analysis.reduce(
          (sum, item) => sum + item.confidence,
          0
        ) / result.analysis.length * 100
      )}%
    </div>
    <div className="text-zinc-400 text-sm">
      AI Confidence
    </div>
  </div>

  {/* Emotions */}
  <div className="bg-zinc-900 rounded-2xl p-4 text-center border border-zinc-700 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
    <div className="text-3xl">🎭</div>
    <div className="text-2xl font-bold">
      {new Set(result.analysis.map(item => item.emotion)).size}
    </div>
    <div className="text-zinc-400 text-sm">
      Emotions Found
    </div>
        </div>
{/* Top Genre */}
<div className="bg-zinc-900 rounded-2xl p-4 text-center border border-zinc-700">
  <div className="text-3xl">
    {topGenre !== "unknown" ? "🎵" : "🎭"}
  </div>

  <div className="text-2xl font-bold capitalize">
    {topGenre !== "unknown" ? topGenre : topEmotion}
  </div>

  <div className="text-zinc-400 text-sm">
    {topGenre !== "unknown"
      ? "Top Genre"
      : result.dominant_emotion}
  </div>
</div>
        </div>    
         </div>  
        {result.analysis && (   

          
                            
                <div className="mt-6">

                  <h3 className="text-green-400 font-bold mb-3">
                    📊 Song Breakdown
                  </h3>

                  <div className="space-y-2" >

                    {result.analysis.map((item, index) => (
                      <div
                        key={index}
                        className="flex justify-between bg-zinc-900 p-3 rounded-lg">

                        <span>{item.song}</span>

                        <span className={
                          item.emotion === "joy"
                            ? "text-yellow-400"
                            : item.emotion === "sadness"
                              ? "text-blue-400"
                              : item.emotion === "anger"
                                ? "text-red-400"
                                : item.emotion === "love"
                                  ? "text-pink-400" 
                                  :item.emotion ==="dark"
                                  ? "text-purple-400 font-semibold" 
                                  : item.emotion === "obsession"
                                  ? "text-orange-400 font-semibold"
                                   : item.emotion === "confidence"
                                    ? "text-amber-400 font-semibold"
                                    : item.emotion === "healing"
                                    ? "text-green-400 font-semibold"
                                    : item.emotion === "conflict"
                                     ? "text-rose-400 font-semibold"
                                     : "text-green-400 font-semibold"
                                  

                        }
                        >

                          {item.emotion}
                        </span>
                      </div>

                    ))}

                  </div>

                </div>
       
             )}  
             
             </div> 
             )} 
            
            </div> </div> {/* closes main card */}

              {/* Global stats section */}
{/* RIGHT COLUMN */} 
<div className="space-y-6 self-start -translate-y-48 translate-x-18">
        {globalStats &&(
          <div className=" bg-zinc-900 rounded-2xl p-5 border border-zinc-700 mb-6 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">

            <h3 className=" text-green-400 font-bold mb-4 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                  🌍 Community Stats 
            </h3> 

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center"> 

              <div>
                <div className="text-2xl font-bold text-green-400 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                  {globalStats.total_roasts}
                </div>

                <div>
                <div className="text-zinc-400 text-sm hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                  Total Roasts 
                </div> 
            </div> 
            
              <div className="text-2xl font-bold text-purple-400 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                {globalStats.total_songs}
                </div>  
                <div className="text-zinc-400 text-sm hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                  Songs Analyzed
                </div>
                </div>

              <div>
                <div className="text-xl font-bold text-yellow-400 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                    {globalStats.top_archetype}
                </div>
                <div className="text-zinc-400 text-sm  hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                  Top Archetype
                </div> 
                </div>

                </div>

                </div>
        )} 
        {/* Community Wall */}

        {community.length  > 0 &&(
          <div className=" mb-6">

            <div className="bg-zinc-900 rounded-2xl p-6 border border-zinc-700"> 

              <div className="text-red-400 text-sm font-semibold mb-2 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300">
                  🔴 LIVE COMMUNITY ACTIVITY
</div>
              <h3 className="text-purple-400 font-bold text-xl mb-2 hover:-translate-y-1">
                        🏆 Community Wall

              </h3>

              <p className="text-zinc-500 text-sm mb-5 "> 
                Live archetype rankings 
              </p> 

              {community.map((item, index) => (
            <div 
                key={index}
                className={`flex justify-between items-center p-4 rounded-xl mb-2 hover:-translate-y-1
hover:shadow-xl
transition-all
duration-300
                  ${
                    index === 0
                    ? "bg-yellow-500/10 border border-yellow-500/30"
                    :"bg-zinc-800"
                  }`}
                  > 

                  <div className="flex items-center gap-3"> 

                    <span className="font-bold text-lg">
                      #{index + 1}
                    </span> 

                    <span> 
                      {item.archetype}
                    </span> 
                      
                    </div>
                    <span className="font-bold text-green-400">
                      {item.count} 
                    </span> 

                    </div> 
                    ))} 

                    </div> 

                    </div> 
        )} 
        </div>
        </div>
        
        <footer className="mt-12 text-center text-gray-400 text-sm pb-6">
          © 2026 Vibe Verdict • Created by Aaditya Sonkar
       </footer>
        </div>
    </div>   );
}

export default App;