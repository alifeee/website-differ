"""Compare the most recent snapshot of a URL with the current version."""
import os
import argparse
from typing import Optional

from playwright.sync_api import sync_playwright

from .snapshots import (
    snapshot_fnames_for_url,
    last_snapshot_fname,
    next_snapshot_fname,
)
from .comparer import html_to_bs4, is_different
from .notifier import NotifierInterface, PrintNotifier

SNAPSHOTS_DIR = "snapshots"


def get_page_html(url: str) -> str:
    """Get the html of a page.
    Uses playwright so that javascript is executed.

    Args:
        url (str): URL of page to get

    Returns:
        str: html of page
    """
    ## with requests
    # response = requests.get(url, timeout=5)
    # return response.text, response.status_code
    ## with playwright
    with sync_playwright() as pwright:
        browser = pwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
    return content


def main(
    url: str,
    css_selector: Optional[str] = None,
    notif: NotifierInterface = PrintNotifier(0),
) -> bool:
    """open old and new files and compare
    returns true if a new file was created
    """
    # main
    #  GET url
    #  is there a historical snapshot?
    #  no
    #   save html content as latest snapshot
    #  yes
    #   load latest snapshot
    #   compare html to snapshot
    #   if different
    #    notify(!)
    #    save new snapshot as latest snapshot
    #   if not different
    #    do nothing
    notif.notify(f"Getting html for {url}", 0)
    html = get_page_html(url)
    soup = html_to_bs4(html, css_selector)
    if soup is None:
        notif.notify(
            f"Could not find element with selector {css_selector} in {url}.", 1
        )
        return False

    all_files = os.listdir(SNAPSHOTS_DIR)
    ss_files = snapshot_fnames_for_url(all_files, url)
    last_ss_fname = last_snapshot_fname(ss_files)
    next_ss_fname = next_snapshot_fname(ss_files, url)

    next_ss_fpath = os.path.join(SNAPSHOTS_DIR, next_ss_fname)

    if last_ss_fname is None:
        notif.notify(f"No snapshot found for {url}. Saving snapshot.", 1)
        with open(next_ss_fpath, "w", encoding="utf-8") as file:
            file.write(str(soup))
        return True

    last_ss_fpath = os.path.join(SNAPSHOTS_DIR, last_ss_fname)
    with open(last_ss_fpath, "r", encoding="utf-8") as file:
        last_snapshot_html = file.read()

    last_snapshot_soup = html_to_bs4(last_snapshot_html, css_selector)

    if is_different(soup, last_snapshot_soup):
        notif.notify(
            f"""New content for {url}! Snapshot saved.
                     View on https://server.alifeee.co.uk:5616/
                     """,
            1,
        )
        with open(next_ss_fpath, "w", encoding="utf-8") as file:
            file.write(str(soup))
        return True

    notif.notify("HTML is the same as last snapshot. Doing nothing.", 0)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare the most recent snapshot of a URL with the current version."
    )
    parser.add_argument("url", help="URL to compare")
    parser.add_argument(
        "--selector",
        "-s",
        help="CSS selector to include in comparison",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase verbosity",
    )

    args = parser.parse_args()
    URL = args.url
    CSS_SELECTOR = args.selector
    VERBOSE = args.verbose

    # example usage:
    # python -m differ.differ https://www.google.com -s "#viewport"

    if VERBOSE == 0:
        notifier = PrintNotifier(1)
    elif VERBOSE == 1:
        notifier = PrintNotifier(0)

    main(URL, CSS_SELECTOR, notifier)
