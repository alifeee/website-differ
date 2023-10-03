"""Functions for comparing webpages (html strings)"""
from typing import Optional
from bs4 import BeautifulSoup


def is_different(
    soup1: BeautifulSoup,
    soup2: BeautifulSoup,
) -> bool:
    """Compare two html

    Args:
        soup1 (BeautifulSoup): html of first page (BeautifulSoup)
        soup2 (BeautifulSoup): html of second page (BeautifulSoup)

    Returns:
        bool: True if different, False if same
    """
    return soup1 != soup2


def html_to_bs4(html: str, css_selector: Optional[str] = None):
    """Convert html to BeautifulSoup object

    Args:
        html (str): html to convert
        css_selector (Optional[str], optional): CSS selector to use to select a subset of the html.
            Defaults to None.

    Returns:
        BeautifulSoup:
    """
    soup = BeautifulSoup(html, "html.parser")
    if css_selector is not None:
        soup = soup.select_one(css_selector)
    return soup
