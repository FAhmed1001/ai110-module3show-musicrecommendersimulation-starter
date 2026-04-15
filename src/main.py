"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, UserProfile


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )

    taste_profile = {
        "genre":         "pop",   # preferred genre
        "mood":          "happy", # preferred mood
        "energy":        0.8,     # target energy level (0.0 - 1.0)
        "tempo_bpm":     120,     # target beats per minute
        "valence":       0.8,     # target positivity (0.0 - 1.0)
        "danceability":  0.75,    # target danceability (0.0 - 1.0)
        "acousticness":  0.2,     # target acousticness (0.0 - 1.0)
    }

    recommendations = recommend_songs(taste_profile, songs, k=5)

    print("\nTop recommendations:\n")
    print("-" * 40)
    for i, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"#{i} {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   :")
        for reason in reasons:
            print(f"      - {reason}")
        print("-" * 40)


if __name__ == "__main__":
    main()
