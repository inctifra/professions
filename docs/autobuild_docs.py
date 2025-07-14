# docs/autobuild_docs.py
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import subprocess
import time
import os

def rebuild_docs():
    print("📄 Rebuilding Sphinx docs...")
    subprocess.run(["sphinx-build", ".", "_build/html"])

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
    print("👀 Watching for changes in .rst files... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
