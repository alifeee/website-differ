"""Functions for saving and loading snapshots of webpages."""
import os
from typing import List, Optional
import math


def canonicalize_url(url: str) -> str:
    """Transform the URL into a valid filename.

    Args:
        url (str): URL to canonicalize

    Returns:
        str: canonicalized URL
    """
    return url.replace("://", "----").replace("/", "---")


def uncanonicalize_url(url: str) -> str:
    """Transform the canonicalized URL back into a valid URL.

    Args:
        url (str): canonicalized URL to uncanonicalize

    Returns:
        str: uncanonicalized URL
    """
    return url.replace("----", "://").replace("---", "/")


def url_to_filename(url: str, version: int) -> str:
    """Convert a URL to a versioned filename.

    Args:
        url (str): URL to convert
        version (int): version number

    Returns:
        str: filename
    """
    return f"{canonicalize_url(url)}_{version}.html"


def filename_to_version(filename: str) -> int:
    """Extract the version number from a filename.

    Args:
        filename (str): filename to extract version from

    Returns:
        int: version number
    """
    return int(filename.split("_")[-1].split(".")[0])


def filename_to_url(filename: str) -> str:
    """Extract the URL from a filename.

    Args:
        filename (str): filename to extract URL from

    Returns:
        str: URL
    """
    return uncanonicalize_url(filename.split("_")[0])


def snapshot_fnames_for_url(files: List[str], url: str) -> List[str]:
    """Return a list of all snapshot filenames for a URL...
    from a list of files in the filesystem

    Args:
        files (List[str]): list of filenames in the snapshots directory
        url (str): URL to get snapshots for

    Returns:
        List[str]: list of filenames
    """
    # filter files to only those that start with url
    files = [f for f in files if f.startswith(canonicalize_url(url))]
    # sort files by number after url
    files.sort(key=filename_to_version)
    return files


def last_snapshot_fname(snapshot_fnames: List[str]) -> Optional[str]:
    """Return the latest snapshot filename from a list of filenames.

    Args:
        snapshot_fnames (List[str]): list of filenames

    Returns:
        Optional[str]: latest snapshot filename
    """
    if len(snapshot_fnames) == 0:
        return None
    snapshot_fnames.sort(key=filename_to_version)
    return snapshot_fnames[-1]


def next_snapshot_fname(files: List[str], url: str) -> str:
    """Return the next snapshot filename from a list of filenames.

    Args:
        snapshot_fnames (List[str]): list of filenames
        url (str): URL to get next snapshot for

    Returns:
        Optional[str]: next snapshot filename
    """
    relevant_fnames = snapshot_fnames_for_url(files, url)
    if len(relevant_fnames) == 0:
        return url_to_filename(url, 0)
    latest_fname = last_snapshot_fname(relevant_fnames)
    latest_version = filename_to_version(latest_fname)
    return url_to_filename(url, latest_version + 1)
