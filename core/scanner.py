"""Tune - поиск музыки на устройстве"""
import os


# Все папки где искать музыку
MUSIC_DIRS = [
    "/storage/emulated/0/Music",
    "/storage/emulated/0/Download",
    "/storage/emulated/0/Downloads",
    "/sdcard/Music",
    "/sdcard/Download",
]

AUDIO_EXTS = (".mp3", ".flac", ".ogg", ".m4a", ".wav", ".opus", ".aac", ".wma")


def get_music_dirs():
    """Возвращает существующие папки"""
    return [d for d in MUSIC_DIRS if os.path.isdir(d)]


def scan():
    """Сканирует все папки и возвращает список путей к трекам"""
    tracks = []
    seen = set()

    for folder in get_music_dirs():
        try:
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(AUDIO_EXTS):
                        path = os.path.join(root, f)
                        if path not in seen:
                            seen.add(path)
                            tracks.append(path)
        except (PermissionError, OSError):
            continue

    return sorted(tracks)


def filename_only(path):
    """Возвращает имя файла без расширения"""
    return os.path.splitext(os.path.basename(path))[0]
