"""Store songs and safely serialize playlists for a small music catalog."""

import json
import secrets
import sqlite3

CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    "CREATE TABLE songs (id INTEGER PRIMARY KEY, title TEXT, "
    "artist TEXT, plays INTEGER)"
)


def add_song(title, artist, plays=0, playlist=None):
    """Insert a song and append its title to the selected playlist."""
    if playlist is None:
        playlist = []
    CONNECTION.execute(
        "INSERT INTO songs (title, artist, plays) VALUES (?, ?, ?)",
        (title, artist, plays),
    )
    playlist.append(title)
    return playlist


def shuffle_pick():
    """Return a random song ID, or None when the catalog is empty."""
    ids = [r[0] for r in CONNECTION.execute("SELECT id FROM songs")]
    return secrets.choice(ids) if ids else None


def popularity(title):
    """Classify a song by its play count."""
    row = CONNECTION.execute(
        "SELECT plays FROM songs WHERE title = ?", (title,)
    ).fetchone()
    if row is None:
        return "unknown"
    return "popular" if row[0] > 100 else "niche"


def save_playlist(playlist):
    """Encode a playlist as UTF-8 JSON bytes."""
    return json.dumps(playlist).encode("utf-8")


def load_playlist(blob):
    """Decode and validate a JSON playlist."""
    playlist = json.loads(blob.decode("utf-8"))
    if not isinstance(playlist, list) or not all(
        isinstance(title, str) for title in playlist
    ):
        raise ValueError("Playlist must be a list of song titles")
    return playlist


def total_plays():
    """Return total plays, including zero for an empty catalog."""
    return CONNECTION.execute(
        "SELECT COALESCE(SUM(plays), 0) FROM songs"
    ).fetchone()[0]


def main():
    """Run a short demonstration."""
    playlist = add_song("Aurora", "Nila", 250)
    add_song("Monsoon", "Kavya", 40, playlist)
    blob = save_playlist(playlist)
    restored_playlist = load_playlist(blob)
    if len(restored_playlist) > 1:
        print("multi-song playlist")
    print(
        popularity("Aurora"), popularity("Monsoon"),
        shuffle_pick(), total_plays(),
    )


if __name__ == "__main__":
    try:
        main()
    finally:
        CONNECTION.close()
