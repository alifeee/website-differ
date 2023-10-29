"""File for adding/removing websites to track"""
import csv
from dataclasses import dataclass
from datetime import datetime
import math
import os
from typing import List, Optional, Union

from differ.snapshots import last_snapshot_fname, snapshot_fnames_for_url

TRACKING_FILE = "sites.csv"


@dataclass
class Snapshot:
    """Dataclass for a snapshot"""

    fname: str
    date_modified: datetime


@dataclass
class Site:
    """Dataclass for a tracked site"""

    id: str
    url: str
    css_selector: str
    total_filesize: Optional[int] = None
    snapshots: Optional[List[Snapshot]] = None

    @property
    def total_filesize_str(self) -> str:
        """Return the total filesize as a human-readable string"""
        if self.total_filesize == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        index = int(math.floor(math.log(self.total_filesize, 1024)))
        power = math.pow(1024, index)
        strong = round(self.total_filesize / power, 2)
        return f"{strong} {size_name[index]}"

    def __repr__(self) -> str:
        return f"Site(url={self.url}, css_selector={self.css_selector})"

    def __eq__(self, other) -> bool:
        return self.url == other.url and self.css_selector == other.css_selector

    def __hash__(self) -> int:
        return hash((self.url, self.css_selector))


def get_sites() -> list[Site]:
    """Return a list of sites to track"""
    sites = []
    # if file does not exist, make it
    if not os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "url", "css_selector"])
            writer.writeheader()
        return sites
    with open(TRACKING_FILE, "r", encoding="utf-8") as file:
        # with header row
        reader = csv.DictReader(file)
        for row in reader:
            sites.append(
                Site(id=row["id"], url=row["url"], css_selector=row["css_selector"])
            )
    return sites


def add_site(url: str, css_selector: str) -> Site:
    """Add a site to track"""
    sites = get_sites()

    # new id
    if len(sites) == 0:
        _id = "1"
    else:
        _id = str(max(int(site.id) for site in sites) + 1)

    with open(TRACKING_FILE, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "url", "css_selector"])
        writer.writerow({"id": _id, "url": url, "css_selector": css_selector})
    return Site(id=_id, url=url, css_selector=css_selector)


def remove_site(_id: str) -> bool:
    """Remove a site from tracking"""
    sites = get_sites()

    if not any(site.id == _id for site in sites):
        return False

    with open(TRACKING_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "url", "css_selector"])
        writer.writeheader()
        for site in sites:
            if site.id != _id:
                writer.writerow(
                    {"id": site.id, "url": site.url, "css_selector": site.css_selector}
                )

    return True


### SIDE EFFECTS
def populate_sites_with_more_info(sites: List[Site], snapshot_directory: str):
    """Populate sites with more info from the filesystem

    Args:
        sites (List[Site]): Sites to populate
        snapshot_directory (str): Directory to look for snapshots in
    """
    if not os.path.exists(snapshot_directory):
        os.mkdir(snapshot_directory)
    all_fnames = os.listdir(snapshot_directory)

    for site in sites:
        url = site.url
        # get all snapshots for this site
        ss_fnames = snapshot_fnames_for_url(all_fnames, url)

        # compute storage of all files
        storage = 0
        for fname in ss_fnames:
            fpath = os.path.join(snapshot_directory, fname)
            storage += os.path.getsize(fpath)

        # snapshot date modified
        def last_modified(fname: str) -> datetime:
            fpath = os.path.join(snapshot_directory, fname)
            return datetime.fromtimestamp(os.path.getmtime(fpath))

        snapshots = [
            Snapshot(fname=fname, date_modified=last_modified(fname))
            for fname in ss_fnames
        ]

        site.snapshots = snapshots
        site.total_filesize = storage


if __name__ == "__main__":
    # n_site = Site(url="https://www.google.com", css_selector="body")
    # add_site(n_site)
    # remove_site(n_site)
    print(get_sites())
