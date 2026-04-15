# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version loads a catalog of 20 songs from a CSV file and scores each one against a user taste profile using five weighted rules: genre match (0.35), mood match (0.25), and proximity scores for energy, valence, and danceability (0.20 / 0.10 / 0.10). Songs are ranked by total score and the top 5 are returned with a plain-language explanation of why each was recommended.

---

## How The System Works

### Song Features

Each `Song` in the catalog carries ten attributes loaded from `data/songs.csv`:

| Attribute | Type | Description |
|---|---|---|
| `id`, `title`, `artist` | metadata | Identity fields, not used in scoring |
| `genre` | string | Musical category (pop, rock, lofi, jazz, etc.) |
| `mood` | string | Emotional tone (happy, chill, intense, moody, etc.) |
| `energy` | 0.0 – 1.0 | Overall intensity and activity level |
| `tempo_bpm` | float | Beats per minute |
| `valence` | 0.0 – 1.0 | Musical positivity (high = upbeat, low = somber) |
| `danceability` | 0.0 – 1.0 | How suitable the track is for dancing |
| `acousticness` | 0.0 – 1.0 | Likelihood of using physical instruments |

### User Profile

A `UserProfile` stores four preference fields:

- `favorite_genre` — the genre the user most wants to hear
- `favorite_mood` — the emotional tone they are looking for
- `target_energy` — their preferred intensity level (0.0 – 1.0)
- `likes_acoustic` — whether they prefer acoustic or electronic sounds

### Scoring a Song (Strategy A — Genre-First)

Every song is scored against the user profile using five weighted rules. Scores are summed to produce a total between 0.0 and 1.0:

| Rule | Weight | How it works |
|---|---|---|
| Genre match | 0.35 | Full points if `song.genre == user.favorite_genre`, zero otherwise |
| Mood match | 0.25 | Full points if `song.mood == user.favorite_mood`, zero otherwise |
| Energy proximity | 0.20 | `0.20 × (1 - \|song.energy - user.target_energy\|)` — closer = higher |
| Valence proximity | 0.10 | `0.10 × (1 - \|song.valence - user.valence\|)` |
| Danceability proximity | 0.10 | `0.10 × (1 - \|song.danceability - user.danceability\|)` |

Genre and mood are binary — an exact label match earns full weight or nothing. Energy, valence, and danceability are continuous — every song earns partial credit proportional to how close its value is to the user's target.

### Choosing the Top K Songs

After every song in the catalog is scored, the selection is mechanical:

1. Sort all `(song, score, explanation)` tuples by score descending
2. Slice the top `k` (default `k=5`)

The "choosing" happens entirely in the scoring step. By the time we rank, the scores already encode all preference logic. Sorting just surfaces the winners.

### Data Flow

```
User Preferences
      │
      ▼
load_songs("data/songs.csv")  →  list of song dicts
      │
      ▼
FOR each song:
  _score_song(user_prefs, song)
    ├─ Genre match?      → +0.35 or +0.00
    ├─ Mood match?       → +0.25 or +0.00
    ├─ Energy proximity  → +0.00 to +0.20
    ├─ Valence proximity → +0.00 to +0.10
    └─ Danceability      → +0.00 to +0.10
  returns (score, explanation)
      │
      ▼
Sort all scored songs by score descending
      │
      ▼
Return top K  →  (song, score, explanation) × K
```

### Algorithm Recipe

A step-by-step description of exactly what the program does each time it runs:

1. **Load** — Read every row from `data/songs.csv` and cast numeric fields (`energy`, `valence`, `danceability`, `tempo_bpm`, `acousticness`) from strings to floats.
2. **Receive user preferences** — Accept a taste profile with a target genre, mood, energy level, valence, and danceability.
3. **Score every song** — For each song in the catalog, apply five rules in order and sum the results:
   - If the song's genre matches the user's preferred genre → add **0.35**
   - If the song's mood matches the user's preferred mood → add **0.25**
   - Subtract the absolute energy difference from 1.0, multiply by **0.20** → add the result
   - Subtract the absolute valence difference from 1.0, multiply by **0.10** → add the result
   - Subtract the absolute danceability difference from 1.0, multiply by **0.10** → add the result
4. **Build an explanation** — While scoring, record which rules fired so the output can say *why* a song was recommended.
5. **Rank** — Sort all scored songs from highest to lowest score.
6. **Return top K** — Slice the sorted list and return the top `k` results (default 5) as `(song, score, explanation)` tuples.

### Potential Biases

| Bias | Why it happens | What it means in practice |
|---|---|---|
| **Genre over-prioritization** | Genre carries 35% of the total score — the single largest weight | A great mood + energy match in the wrong genre can never outscore a mediocre same-genre song. A jazz fan set to `pop` will never see jazz tracks no matter how perfectly they fit. |
| **Mood rigidity** | Mood is binary (match or no match), worth 25% | Two songs can be sonically identical but one gets 0.25 extra simply because its mood label matches. Labels like "chill" vs. "relaxed" are treated as completely different. |
| **Numeric defaults favor the middle** | Valence and danceability default to `0.5` in the OOP path when not supplied | Songs near the middle of those scales get artificially boosted for users whose real preference may be at either extreme. |
| **Small, homogeneous catalog** | The CSV has ~20 songs with a limited spread of genres and moods | Some genres (e.g., ambient, jazz) have very few entries, so users who prefer them consistently get lower-scoring results — not because the algorithm is wrong, but because there is nothing better to find. |
| **No diversity enforcement** | Top-K is a pure score sort | The system can return five nearly identical songs if they all share the user's genre and mood. There is no mechanism to surface variety. |

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

Three user profiles were tested manually:

1. **Pop / happy / energy 0.8** — Sunrise City scored 1.00 and ranked first. Genre and mood both matched, and energy was nearly identical to the target. Results felt accurate and easy to explain.
2. **Lofi / chill / energy 0.4** — The top two results were both lofi/chill tracks with very similar scores (0.87 and 0.85). The recommendations were reasonable but nearly identical, showing that the system has no mechanism to surface variety.
3. **Rock / intense / energy 0.9** — Only one rock song exists in the catalog (Storm Runner). It ranked first, but the remaining four results came from other genres entirely. This confirmed that a thin catalog is the system's biggest practical weakness.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

The catalog has only 20 songs, so users with niche genre preferences will almost always receive low-scored or off-genre results. Genre carries 35% of the total score, which means a strong genre mismatch can outweigh near-perfect matches on every other feature. Mood labels are binary and exact — "chill" and "relaxed" are treated as completely different, so similar-feeling songs can score zero on mood. The system also ignores lyrics, language, tempo, cultural context, and listener history entirely.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Recommendation is really just ranking. There is no prediction happening — the system applies a fixed set of weighted rules to every song and sorts the results. The "intelligence" lives entirely in the choice of features and weights, not in the code itself. Changing the genre weight from 0.35 to 0.20 would produce meaningfully different recommendations without touching any logic.

Bias does not require intent. This system never set out to underserve jazz or ambient listeners, but because those genres have fewer songs in the catalog, users who prefer them consistently receive worse results. In a real product that gap would compound over time — underrepresented genres get fewer listens, which produces less data, which leads to even weaker recommendations for those users.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

┌─────────────────────────────────────────────────────┐
│  INPUT: User Preferences (taste_profile dict)        │
│                                                      │
│   genre="pop"   mood="happy"   energy=0.8            │
│   valence=0.8   danceability=0.75                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  LOAD: load_songs("data/songs.csv")                  │
│                                                      │
│  CSV rows → list of song dicts                       │
│  (strings cast to floats for numeric fields)         │
└────────────────────┬────────────────────────────────┘
                     │  ~20 songs
                     ▼
┌─────────────────────────────────────────────────────┐
│  PROCESS: The Loop  (inside recommend_songs)         │
│                                                      │
│  FOR each song in songs:                             │
│  │                                                   │
│  │  _score_song(user_prefs, song)                    │
│  │                                                   │
│  │  ┌──────────────────────────────────┐             │
│  │  │  Genre match?   → +0.35 or +0.0  │             │
│  │  │  Mood match?    → +0.25 or +0.0  │             │
│  │  │  Energy gap     → +0.0 to +0.20  │             │
│  │  │  Valence gap    → +0.0 to +0.10  │             │
│  │  │  Danceability   → +0.0 to +0.10  │             │
│  │  └──────────────┬───────────────────┘             │
│  │                 │                                  │
│  └── (song, score, explanation)  ──────────────────► │
│                                                      │
│  Result: list of all scored songs                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  RANK: sort by score descending → slice [:k]         │
│                                                      │
│  #1  Sunrise City    0.99  ← genre + mood + energy   │
│  #2  Gym Hero        0.71  ← genre + energy          │
│  #3  Rooftop Lights  0.63  ← mood + energy           │
│  #4  ...                                             │
│  #5  ...                                             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  OUTPUT: Top K (song, score, explanation) tuples     │
│                                                      │
│  Printed in main.py:                                 │
│  "Sunrise City - Score: 0.99"                        │
│  "Because: matches genre (pop), mood (happy)..."     │
└─────────────────────────────────────────────────────┘

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

The catalog has 20 songs. No songs were added or removed from the starter dataset. Genres include pop, rock, lofi, jazz, synthwave, ambient, hip-hop, classical, country, funk, and reggae. Moods include happy, chill, intense, moody, relaxed, focused, melancholic, uplifting, and energetic. The data skews toward Western popular music styles and likely reflects the taste of a younger English-speaking listener. Genres like classical, reggae, and country have only one song each, so they are significantly underrepresented.

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

The system works best for users who have a clear, dominant genre preference and a well-defined mood. A pop/happy/high-energy profile produced a near-perfect top result with an easily explainable score. Every recommendation comes with a breakdown of exactly which rules fired and how many points each contributed, which makes the output transparent and easy to audit. The scoring logic is also simple enough that you can predict roughly what will happen when you change a weight — there are no hidden layers or black-box behavior.

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

The system ignores tempo, acousticness, lyrics, and cultural context entirely. It treats every user identically — the same five rules and the same weights apply regardless of who is asking. Genre carries the most weight by design, but that means a user whose favorite genre is underrepresented in the catalog (e.g., classical or reggae) will almost always receive worse results than a pop or lofi listener. In a real product this would be unfair — users with less mainstream tastes would consistently get lower-quality recommendations through no fault of their own.

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

Three user profiles were tested manually and the results were compared against intuition. For the pop/happy profile, the top result matched expectations exactly. For the rock/intense profile, the catalog gap became immediately visible — only one rock song existed, so positions 2–5 were filled by unrelated genres. The output was also compared loosely against Spotify's behavior: Spotify would surface more variety and cross-genre discoveries, while this system stays strictly within the user's stated genre unless the catalog forces otherwise.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

1. **Add tempo scoring.** The user profile already stores `tempo_bpm` but the scoring function ignores it. Adding a proximity rule for tempo would give the algorithm a stronger signal, especially for distinguishing workout tracks from study music.
2. **Enforce diversity in the top K.** After ranking, check if more than two results share the same genre and swap in lower-ranked songs from other genres to prevent five nearly identical recommendations.
3. **Expand the catalog.** 20 songs is too small to serve niche preferences. A catalog of 200+ songs spread evenly across genres would make recommendations feel meaningful for any user profile, not just pop and lofi listeners.

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
I wasn't particularly surprised by anything about how the system worked, but ti was interesting to see how recommenders can work behind the scenes and somehow quantify something as subjective as music, which I never thought could really be measured. I still maintain that it can't be measured entirely accurately, but we came a lot closer when building this system. In order to come up with a reasonable scoring system, human input is still needed to determine what needs to be measured in the first place, like tempo or beats per minute. The model itself can't reasonably know what to measure unless it's given those parameters. TO that end, humans also need to decice which factors matter the most when making recommendations for different users. 

