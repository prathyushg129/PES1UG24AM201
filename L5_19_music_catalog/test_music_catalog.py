"""Regression checks for the catalog fixes."""
import json
import unittest

import music_catalog as catalog


class CatalogTests(unittest.TestCase):
    """Verify behavior that static analysis cannot establish."""

    def setUp(self):
        catalog.CONNECTION.execute("DELETE FROM songs")

    def test_independent_default_playlists(self):
        first = catalog.add_song("First", "Artist")
        second = catalog.add_song("Second", "Artist")
        self.assertEqual(first, ["First"])
        self.assertEqual(second, ["Second"])
        self.assertIsNot(first, second)

    def test_explicit_playlist_is_shared(self):
        playlist = []
        self.assertIs(catalog.add_song("Song", "Artist", 2, playlist),
                      playlist)
        self.assertEqual(playlist, ["Song"])

    def test_sql_input_is_data(self):
        title = "Song'); DROP TABLE songs; --"
        catalog.add_song(title, "O'Connor", 150)
        self.assertEqual(catalog.popularity(title), "popular")
        self.assertEqual(catalog.total_plays(), 150)

    def test_empty_catalog(self):
        self.assertEqual(catalog.total_plays(), 0)
        self.assertIsNone(catalog.shuffle_pick())
        self.assertEqual(catalog.popularity("Absent"), "unknown")

    def test_popularity_boundaries(self):
        catalog.add_song("At threshold", "Artist", 100)
        catalog.add_song("Above threshold", "Artist", 101)
        self.assertEqual(catalog.popularity("At threshold"), "niche")
        self.assertEqual(catalog.popularity("Above threshold"), "popular")
        self.assertEqual(catalog.total_plays(), 201)

    def test_json_round_trip(self):
        playlist = ["Aurora", "Monsoon", "Caf\u00e9"]
        self.assertEqual(
            catalog.load_playlist(catalog.save_playlist(playlist)), playlist
        )

    def test_reject_invalid_playlists(self):
        for blob in (b'{}', b'[1]', b'null'):
            with self.subTest(blob=blob):
                with self.assertRaises(ValueError):
                    catalog.load_playlist(blob)
        with self.assertRaises(json.JSONDecodeError):
            catalog.load_playlist(b'not json')

    def test_random_pick_is_existing_id(self):
        catalog.add_song("Song", "Artist")
        song_id = catalog.CONNECTION.execute(
            "SELECT id FROM songs"
        ).fetchone()[0]
        self.assertEqual(catalog.shuffle_pick(), song_id)


if __name__ == "__main__":
    unittest.main()
