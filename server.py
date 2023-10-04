"""Server for the web differ
Allowing user to view files, edit tracked websites, and view diffs
"""
from datetime import datetime
import difflib
import sys
import os

from waitress import serve
from flask import Flask, render_template, request, send_file, abort
from differ.snapshots import filename_to_version, snapshot_fnames_for_url

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
    desired_file = os.path.join("static", filename)
    if os.path.isfile(desired_file):
        return send_file(desired_file)
    else:
        abort(404)


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


@app.get("/urls")
def urls():
    """Return a list of tracked sites"""
    all_urls = [site.url for site in tracking.get_sites()]
    return render_template(
        "options.html",
        options=zip(all_urls, all_urls),
        include_empty=True,
    )


@app.get("/versions_selects")
def versions_selects():
    """Return two selects for version"""
    url = request.args.get("url")
    if url == "":
        return ""
    all_snapshots = os.listdir(SNAPSHOTS_DIR)
    url_snapshots = snapshot_fnames_for_url(all_snapshots, url)

    url_modified_times_timestamp = [
        os.path.getmtime(os.path.join(SNAPSHOTS_DIR, fname)) for fname in url_snapshots
    ]
    url_modified_times = [
        datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        for timestamp in url_modified_times_timestamp
    ]

    select1 = "<select id='form_from' name='from' _='on change log 1'>"
    select1 += render_template(
        "options.html",
        options=zip(url_snapshots, url_modified_times),
        selected_value=url_snapshots[-2] if len(url_snapshots) > 1 else None,
    )
    select1 += "</select>"
    select2 = "<select id='form_to' name='to'>"
    select2 += render_template(
        "options.html",
        options=zip(url_snapshots, url_modified_times),
        selected_value=url_snapshots[-1] if len(url_snapshots) > 0 else None,
    )
    select2 += "</select>"
    return select1 + " to " + select2


@app.get("/compare")
def compare():
    """Compare two snapshots"""
    # url = request.args.get("url")
    fromfname = request.args.get("from")
    tofname = request.args.get("to")
    colwidth = int(request.args.get("colwidth"))

    if fromfname is None or tofname is None:
        return "Please select two snapshots to compare"
    elif fromfname == tofname:
        return "Snapshots are the same!"

    fromfile = os.path.join(SNAPSHOTS_DIR, fromfname)
    tofile = os.path.join(SNAPSHOTS_DIR, tofname)

    with open(fromfile, "r", encoding="utf-8") as file:
        fromlines = file.readlines()
    with open(tofile, "r", encoding="utf-8") as file:
        tolines = file.readlines()

    diff = difflib.HtmlDiff(wrapcolumn=colwidth).make_file(
        fromlines, tolines, fromfile, tofile
    )
    return diff


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
