import sqlite3
import datetime
import zlib

# database class for
# CREATE TABLE queries (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   url TEXT NOT NULL,
#   datetime DATETIME NOT NULL,
#   snapshot_id INTEGER NOT NULL,
#   FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
# );

# CREATE TABLE snapshots (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   snapshot BLOB NOT NULL
# );


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.conn.commit()

    def add(self, url, snapshot_string):
        snapshot_bytes = snapshot_string.encode("utf-8")
        snapshot_compressed = zlib.compress(snapshot_bytes)
        query = self.cursor.execute(
            "SELECT * FROM snapshots WHERE snapshot=?", (snapshot_compressed,)
        )
        row = query.fetchone()
        if row is None:
            self.cursor.execute(
                "INSERT INTO snapshots (snapshot) VALUES (?)", (snapshot_compressed,)
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

    def getLatest(self, url):
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
        snapshot_compressed = row[1]
        snapshot_bytes = zlib.decompress(snapshot_compressed)
        snapshot_string = snapshot_bytes.decode("utf-8")
        return (datetime, snapshot_string)

    def __del__(self):
        self.conn.close()
