"""Server for the web differ
Allowing user to view files, edit tracked websites, and view diffs
"""
import sys
import os
from waitress import serve
from flask import Flask, request, send_file
from differ.snapshots import SNAPSHOTS_DIR, filename_to_url

app = Flask(__name__)


@app.route("/alive")
def alive():
    """Simple endpoint to check if the server is alive"""
    return "alive"


@app.get("/tracked_sites")
def tracked_sites():
    """Return a list of tracked sites"""
    all_files = os.listdir(SNAPSHOTS_DIR)
    tracked_sites = set()
    for fname in all_files:
        tracked_sites.add(filename_to_url(fname))
    return {"tracked_sites": list(tracked_sites)}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app.run(debug=True, host="0.0.0.0")
    else:
        serve(app, host="0.0.0.0", port=5616)
