"""Take snapshots of all sites"""
from differ import tracking
from differ.differ import main as differ_snapshot
from differ.notifier import PushbulletNotifier


def take_all_snapshots():
    """Take snapshots of all sites"""
    sites = tracking.get_sites()
    for site in sites:
        differ_snapshot(
            site.url,
            site.css_selector,
            notif=PushbulletNotifier(1),
        )


if __name__ == "__main__":
    take_all_snapshots()
