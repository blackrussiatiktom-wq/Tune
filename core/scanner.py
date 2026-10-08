"""Tune - поиск музыки"""
import os

MUSIC_DIRS = [
    "/storage/emulated/0/Music",
    "/storage/emulated/0/Download",
    "/storage/emulated/0/Downloads",
]
AUDIO_EXTS = (".mp3", ".flac", ".ogg", ".m4a", ".wav", ".opus", ".aac")


def scan():
    tracks = []
    seen = set()
    for folder in MUSIC_DIRS:
        if not os.path.isdir(folder):
            continue
        try:
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(AUDIO_EXTS):
                        path = os.path.join(root, f)
                        if path not in seen:
                            seen.add(path)
                            tracks.append(path)
        except Exception:
            continue
    return sorted(tracks)
