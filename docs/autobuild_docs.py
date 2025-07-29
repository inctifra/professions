import logging
import subprocess
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


def rebuild_docs():
    logger.info("📄 Rebuilding Sphinx docs...")
    subprocess.run(["sphinx-build", ".", "_build/html"], check=False)  # noqa: S607


class RebuildHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        rebuild_docs()


if __name__ == "__main__":
    rebuild_docs()
    path = "."
    event_handler = RebuildHandler(patterns=["*.rst"])
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
