import sqlite3
import datetime
import zlib


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS queries (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL, datetime DATETIME NOT NULL, snapshot_id INTEGER NOT NULL, FOREIGN KEY (snapshot_id) REFERENCES snapshots(id))"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS snapshots (id INTEGER PRIMARY KEY AUTOINCREMENT, snapshot BLOB NOT NULL)"
        )
        self.conn.commit()

    def _encodeSnapshot(self, snapshot: str):
        """Encode a snapshot string by compressing it using the zlib library.

        Args:
            snapshot (str): A string containing the HTML of a website.

        Returns:
            bytes: A compressed bytes object representing the encoded snapshot.
        """
        snapshot_bytes = snapshot.encode("utf-8")
        snapshot_compressed = zlib.compress(snapshot_bytes)
        return snapshot_compressed

    def _decodeSnapshot(self, snapshot_compressed: bytes):
        """Decode a compressed snapshot bytes object using the zlib library.

        Args:
            snapshot_compressed (bytes): A compressed bytes object representing the encoded snapshot.

        Returns:
            str: A string representing the decoded snapshot.
        """
        snapshot_bytes = zlib.decompress(snapshot_compressed)
        snapshot = snapshot_bytes.decode("utf-8")
        return snapshot
        encoded_snapshot = self._encodeSnapshot(snapshot)
        query = self.cursor.execute(
            "SELECT * FROM snapshots WHERE snapshot=?", (encoded_snapshot,)
        )
        row = query.fetchone()
        if row is None:
            self.cursor.execute(
                "INSERT INTO snapshots (snapshot) VALUES (?)", (encoded_snapshot,)
            )
            self.conn.commit()
            snapshot_id = self.cursor.lastrowid
        else:
            snapshot_id = row[0]
        self.cursor.execute(
            "INSERT INTO queries (url, datetime, snapshot_id) VALUES (?, ?, ?)",
            (url, datetime.datetime.now(), snapshot_id),
        )
        self.conn.commit()

    def getLatestSnapshot(self, url: str):
        query = self.cursor.execute(
            "SELECT * FROM queries WHERE url=? ORDER BY datetime DESC LIMIT 1",
            (url,),
        )
        row = query.fetchone()
        if row is None:
            return (None, None)
        datetime = row[2]
        snapshot_id = row[3]
        query = self.cursor.execute(
            "SELECT * FROM snapshots WHERE id=?", (snapshot_id,)
        )
        row = query.fetchone()
        if row is None:
            raise Exception("Snapshot not found")
        snapshot = self._decodeSnapshot(row[1])
        return (datetime, snapshot)

    def getSnapshot(self, id: int):
        query = self.cursor.execute(
            "SELECT * FROM snapshots WHERE id=?", (id,)
        )
        row = query.fetchone()
        if row is None:
            raise KeyError(f"Snapshot {id} not found")
        return self._decodeSnapshot(row[1])

    def __del__(self):
        self.conn.close()
