# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

**VibeFinder 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeFinder suggests songs from a small catalog based on a user's taste profile. It assumes the user can describe their preferences as a single genre, mood, and energy level. It is built for classroom exploration only — it should not be used as a substitute for real music apps like Spotify or Apple Music.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song gets a score between 0 and 1. The score comes from five rules: if the genre matches the user's preference it gets 0.35 points, if the mood matches it gets 0.25 points, and the remaining 0.40 points are split across energy, valence, and danceability — each one gives partial credit based on how close the song's value is to the user's target. After every song is scored, the list is sorted and the top 5 are returned. Genre carries the most weight on purpose because it is usually the strongest signal of what a listener wants.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 20 songs loaded from `data/songs.csv`. Genres include pop, rock, lofi, jazz, synthwave, ambient, hip-hop, classical, country, funk, and reggae. Moods include happy, chill, intense, moody, relaxed, focused, melancholic, uplifting, and energetic. No songs were added or removed. Missing from the data: lyrics, language, cultural context, release year, and listener play history.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

Works well for users with a clear, dominant genre preference. A pop fan set to high energy and happy mood got a near-perfect top result (Sunrise City scored 1.00). The scoring is also fully transparent — every recommendation shows exactly which rules fired and how many points each one added, which makes it easy to understand and trust the output.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Genre dominates: a song in the wrong genre can never beat a mediocre same-genre match even if everything else aligns. Mood labels are rigid — "chill" and "relaxed" are treated as completely different, so similar-feeling songs can score zero on mood. Some genres (ambient, classical, country) only have one or two songs, so users who prefer them almost always get low-scored results. The top 5 can also be nearly identical songs with no variety, since there is no mechanism to surface diverse options.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Three profiles were tested manually. A pop / happy / high energy profile gave accurate results — Sunrise City ranked first with a perfect score. A lofi / chill / low energy profile returned reasonable results but had two nearly identical lofi tracks in the top 3. A rock / intense / high energy profile exposed the catalog's limits — only one rock song exists, so the remaining four results all came from other genres.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. Add a diversity rule — if the top 5 all share the same genre, swap in a lower-ranked song from a different genre to add variety.
2. Score tempo proximity — the user profile already stores `tempo_bpm` but the scoring function ignores it. Adding a proximity rule for it would give the algorithm a stronger signal.
3. Expand the catalog — 20 songs is too small. A catalog of 200+ songs spread across all genres would make recommendations feel meaningful for any user profile.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building this made it clear that recommendation is just ranking — there is no magic, just weighted rules applied consistently to every option. The interesting part is deciding which features matter and how much. Changing the genre weight alone would completely change which songs surface for most users, even though the code stays the same. It also showed how bias creeps in quietly: the system never intended to underserve jazz or ambient fans, but the small catalog made that outcome inevitable. Real recommenders face the same problem at scale — underrepresented genres get fewer listens, which means less data, which means worse recommendations.
