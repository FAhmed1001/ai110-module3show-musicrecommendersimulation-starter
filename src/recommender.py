from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user profile."""
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "valence":      0.5,
            "danceability": 0.5,
        }
        scored = sorted(
            self.songs,
            key=lambda s: _score_song(user_prefs, {
                "genre":        s.genre,
                "mood":         s.mood,
                "energy":       s.energy,
                "valence":      s.valence,
                "danceability": s.danceability,
            })[0],  # index 0 is the numeric score
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended to the user."""
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "valence":      0.5,
            "danceability": 0.5,
        }
        song_dict = {
            "genre":        song.genre,
            "mood":         song.mood,
            "energy":       song.energy,
            "valence":      song.valence,
            "danceability": song.danceability,
        }
        _, _, explanation = _score_song(user_prefs, song_dict)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def _score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str], str]:
    """
    Strategy A — Genre-First scoring.
    Returns (total_score, reasons_list, explanation_string).
    """
    score = 0.0
    reasons = []

    # Genre match: 0.35
    if song["genre"] == user_prefs["genre"]:
        score += 0.35
        reasons.append(f"genre match (+0.35)")

    # Mood match: 0.25
    if song["mood"] == user_prefs["mood"]:
        score += 0.25
        reasons.append(f"mood match (+0.25)")

    # Energy proximity: 0.20
    energy_score = round(0.20 * (1 - abs(song["energy"] - user_prefs["energy"])), 2)
    score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    # Valence proximity: 0.10
    valence_score = round(0.10 * (1 - abs(song["valence"] - user_prefs["valence"])), 2)
    score += valence_score
    reasons.append(f"valence proximity (+{valence_score})")

    # Danceability proximity: 0.10
    dance_score = round(0.10 * (1 - abs(song["danceability"] - user_prefs["danceability"])), 2)
    score += dance_score
    reasons.append(f"danceability proximity (+{dance_score})")

    explanation = ", ".join(reasons)
    return round(score, 4), reasons, explanation


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons, _ = _score_song(user_prefs, song)
        scored.append((song, score, reasons))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
