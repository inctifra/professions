from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
from tqdm import tqdm


class Command(CollectStaticCommand):
    def handle(self, **options):
        print("Hello")
        return super().handle(**options)

    # def collect(self):
    #     # Count files first
    #     self.total_count = sum(1 for _ in self.storage.listdir('')[1])
    #     return super().collect()

    # def copy_file(self, path, prefixed_path, source_storage):
    #     if not hasattr(self, "_progress"):
    #         # Fallback if we couldn’t count properly
    #         self._progress = tqdm(desc="Collectstatic", unit="files")

    #     result = super().copy_file(path, prefixed_path, source_storage)
    #     self._progress.update(1)
    #     return result
