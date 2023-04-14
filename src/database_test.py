import sqlite3
import zlib
import unittest
import time
from .database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create an in-memory database for testing
        self.db = Database(":memory:")

    def test_encode_snapshot(self):
        # Arrage
        snapshot = "This is a test snapshot"
        encoded = zlib.compress(snapshot.encode("utf-8"))

        # Act
        encoded_snapshot = self.db._encodeSnapshot(snapshot)

        # Assert
        self.assertEqual(encoded_snapshot, encoded)

    def test_decode_snapshot(self):
        # Arrage
        snapshot = "This is a test snapshot"
        encoded = zlib.compress(snapshot.encode("utf-8"))

        # Act
        decoded_snapshot = self.db._decodeSnapshot(encoded)

        self.assertEqual(decoded_snapshot, snapshot)

    def test_recordSnapshot(self):
        # Arrange
        url = "https://www.uniquelink45784515132.com"
        snapshot = "Wow, look at this website"

        query = self.db.cursor.execute(
            "SELECT * FROM snapshots WHERE snapshot=?", (self.db._encodeSnapshot(
                snapshot),)
        )
        row = query.fetchone()
        self.assertIsNone(row)

        query = self.db.cursor.execute(
            "SELECT * FROM queries WHERE url=?", (url,)
        )
        row = query.fetchone()
        self.assertIsNone(row)

        # Act
        self.db.recordSnapshot(url, snapshot)

        # Assert
        query = self.db.cursor.execute(
            "SELECT * FROM snapshots WHERE snapshot=?", (self.db._encodeSnapshot(
                snapshot),)
        )
        row = query.fetchone()
        self.assertIsNotNone(row)

        query = self.db.cursor.execute(
            "SELECT * FROM queries WHERE url=?", (url,)
        )
        row = query.fetchone()
        self.assertIsNotNone(row)

    def test_getLatestSnapshot(self):
        # Arrange
        url = "https://www.uniquelink54564515132.com"
        snapshot1 = "Wow, look at this website"
        snapshot2 = "Wow, look at this website again"

        # Act
        self.db.recordSnapshot(url, snapshot1)
        time.sleep(0.01)
        self.db.recordSnapshot(url, snapshot2)

        # Assert
        ss_date, latest_snapshot = self.db.getLatestSnapshot(url)
        self.assertEqual(latest_snapshot, snapshot2)

    def test_getSnapshot(self):
        # Arrange
        url = "https://www.uniquelink4577787875132.com"
        snapshot1 = "Here is a single website"
        snapshot2 = "Here is a single website. Edit"
        self.db.recordSnapshot(url, snapshot1)
        time.sleep(0.01)
        self.db.recordSnapshot(url, snapshot2)

        # Act
        ss1 = self.db.getSnapshot(1)
        ss2 = self.db.getSnapshot(2)

        # Assert
        self.assertEqual(ss1, snapshot1)
        self.assertEqual(ss2, snapshot2)

    def test_addWebsite(self):
        # Arrange
        url = "https://www.uniquelink4577781235135.com"

        # Act
        self.db.addWebsite(url)

        # Assert
        query = self.db.cursor.execute(
            "SELECT * FROM websites WHERE url=?", (url,)
        )
        row = query.fetchone()
        self.assertIsNotNone(row)

    def test_getWebsites(self):
        # Arrange
        url1 = "https://www.uniquelink45777818723.com"
        url2 = "https://www.uniquelink4519274871.com/2"
        self.db.addWebsite(url1)
        self.db.addWebsite(url2)

        # Act
        websites = self.db.getWebsites()

        # Assert
        self.assertEqual(websites, [(1, url1), (2, url2)])

    def test_removeWebsite(self):
        # Arrange
        url1 = "https://www.uniquelink908190589416.com"
        url2 = "https://www.uniquelink45731867856.com/2"
        self.db.addWebsite(url1)
        self.db.addWebsite(url2)

        # Act
        self.db.removeWebsite(1)

        # Assert
        websites = self.db.getWebsites()
        self.assertEqual(websites, [(2, url2)])
