"""Server for the web differ
Allowing user to view files, edit tracked websites, and view diffs
"""
import sys
import os

from waitress import serve
from flask import Flask, render_template, request, send_file

import differ.tracking as tracking
from differ.differ import SNAPSHOTS_DIR

app = Flask(__name__)


@app.route("/alive")
def alive():
    """Simple endpoint to check if the server is alive"""
    return "alive"


@app.route("/")
def index():
    """Serve the index page"""
    return send_file("static/index.html")


@app.route("/<path:filename>")
def static_files(filename):
    """Serve static files"""
    return send_file(os.path.join("static", filename))


@app.route("/snapshots/<path:filename>")
def snapshots(filename):
    """Serve a snapshot file"""
    return send_file(os.path.join(SNAPSHOTS_DIR, filename))


@app.get("/websites")
def tracked_sites():
    """Return a list of tracked sites"""
    sites = tracking.get_sites()
    tracking.populate_sites_with_more_info(
        snapshot_directory=SNAPSHOTS_DIR, sites=sites
    )

    return render_template(
        "tablerows.html",
        sites=sites,
        SNAPSHOTS_DIR=SNAPSHOTS_DIR,
    )


@app.post("/add_site")
def add_site():
    """Add a site to track"""
    url = request.form["url"]
    css_selector = request.form["css_selector"]
    new_site = tracking.add_site(url, css_selector)
    tracking.populate_sites_with_more_info(
        snapshot_directory=SNAPSHOTS_DIR, sites=[new_site]
    )
    return render_template(
        "tablerows.html",
        sites=[new_site],
        SNAPSHOTS_DIR=SNAPSHOTS_DIR,
    )


@app.delete("/remove_site/<_id>")
def remove_site(_id):
    """Remove a site from tracking"""
    print("\n", _id)
    success = tracking.remove_site(_id)
    if success is True:
        return """<span _='init wait 2s 
        then transition opacity to 0 
        then remove the closest parent <tr/>
        '>Deleted!</span>"""
    elif success is False:
        return "Failed to delete! Refresh page..."


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app.run(debug=True, host="0.0.0.0")
    else:
        serve(app, host="0.0.0.0", port=5616)
