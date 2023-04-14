from .database import Database
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python database.py <queries|snapshots|websites>")
        sys.exit(1)
    db = Database("websites.db")
    command = sys.argv[1]
    if command == "queries":
        print("Usage: python database.py queries [id]")
        if len(sys.argv) >= 3:
            id = int(sys.argv[2])
            url, datetime, snapshot_id = db.getQuery(id)
            print(f"URL: {url}")
            print(f"Date/Time: {datetime}")
            print(f"Snapshot ID: {snapshot_id}")
        else:
            query = db.cursor.execute("SELECT * FROM queries")
            rows = query.fetchall()
            for row in rows:
                print(f"Query {row[0]}:")
                print(f"URL: {row[1]}")
                print(f"Date/Time: {row[2]}")
                print(f"Snapshot ID: {row[3]}")
    elif command == "snapshots":
        print("Usage: python database.py snapshots [id] [filename]")
        if len(sys.argv) >= 3:
            id = int(sys.argv[2])
        else:
            id = None
        if id is None:
            query = db.cursor.execute("SELECT * FROM snapshots")
            rows = query.fetchall()
            for row in rows:
                print(f"{row[0]}")
            print("Use the snapshot ID to see the snapshot")
        else:
            if len(sys.argv) >= 4:
                filename = sys.argv[3]
                snapshot = db.getSnapshot(id)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(snapshot)
            else:
                print(
                    "Cowardly refusing to print snapshot to stdout. Please specify a filename as the third argument.")
                sys.exit(1)
    elif command == "websites":
        print("Usage: python database.py websites [view|add|remove] [url]")
        if len(sys.argv) >= 3:
            subcommand = sys.argv[2]
            if subcommand == "view":
                rows = db.getWebsites()
                if len(rows) == 0:
                    print("-- No websites found --")
                for row in rows:
                    print(f"{row[0]}: {row[1]}")
            elif subcommand == "add":
                if len(sys.argv) >= 4:
                    url = sys.argv[3]
                    db.addWebsite(url)
                else:
                    print("Please specify a URL to add")
                    sys.exit(1)
            elif subcommand == "remove":
                if len(sys.argv) >= 4:
                    id = int(sys.argv[3])
                    db.removeWebsite(id)
                else:
                    print("Please specify a website ID to remove")
                    sys.exit(1)
            else:
                print(f"Invalid subcommand: {subcommand}")
                sys.exit(1)
    else:
        print(f"Invalid command: {command}")
        sys.exit(1)
