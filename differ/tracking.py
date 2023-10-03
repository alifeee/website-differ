"""File for adding/removing websites to track"""
import csv
from dataclasses import dataclass

TRACKING_FILE = "sites.csv"


@dataclass
class Site:
    """Dataclass for a tracked site"""

    url: str
    css_selector: str

    def __repr__(self) -> str:
        return f"Site(url={self.url}, css_selector={self.css_selector})"

    def __eq__(self, other) -> bool:
        return self.url == other.url and self.css_selector == other.css_selector

    def __hash__(self) -> int:
        return hash((self.url, self.css_selector))


def get_sites() -> list[Site]:
    """Return a list of sites to track"""
    sites = []
    with open(TRACKING_FILE, "r", encoding="utf-8") as file:
        # with header row
        reader = csv.DictReader(file)
        for row in reader:
            sites.append(Site(url=row["url"], css_selector=row["css_selector"]))
    return sites


def add_site(new_site: Site) -> bool:
    """Add a site to track"""
    with open(TRACKING_FILE, "a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["url", "css_selector"])
        writer.writerow({"url": new_site.url, "css_selector": new_site.css_selector})
    return True


def remove_site(rm_site: Site) -> bool:
    """Remove a site from tracking"""
    sites = get_sites()
    if rm_site not in sites:
        return False

    with open(TRACKING_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["url", "css_selector"])
        writer.writeheader()
        for site in sites:
            if site != rm_site:
                writer.writerow({"url": site.url, "css_selector": site.css_selector})

    return True


if __name__ == "__main__":
    n_site = Site(url="https://www.google.com", css_selector="body")
    # add_site(n_site)
    remove_site(n_site)
    print(get_sites())
