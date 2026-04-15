# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


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

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

