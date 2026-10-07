"""Поиск музыки на устройстве."""
import os
from mutagen import File as MutaFile

AUDIO_EXTS = (".mp3", ".flac", ".ogg", ".m4a", ".wav", ".opus", ".aac")

def scan(music_dir):
    """Возвращает список треков: [{'path':..., 'title':..., 'artist':...}]"""
    tracks = []
    if not os.path.isdir(music_dir):
        return tracks

    for root, _, files in os.walk(music_dir):
        for f in files:
            if f.lower().endswith(AUDIO_EXTS):
                path = os.path.join(root, f)
                tracks.append(read_tags(path))

    return sorted(tracks, key=lambda t: t["title"].lower())

def read_tags(path):
    """Читает теги трека, возвращает dict."""
    info = {
        "path":   path,
        "title":  os.path.splitext(os.path.basename(path))[0],
        "artist": "Unknown",
        "album":  "",
        "dur":    0,
    }
    try:
        audio = MutaFile(path)
        if audio is None:
            return info
        if audio.tags:
            t = audio.tags.get("TIT2") or audio.tags.get("title")
            a = audio.tags.get("TPE1") or audio.tags.get("artist")
            al = audio.tags.get("TALB") or audio.tags.get("album")
            if t:  info["title"]  = str(t)
            if a:  info["artist"] = str(a)
            if al: info["album"]  = str(al)
        if audio.info:
            info["dur"] = int(audio.info.length)
    except Exception:
        pass
    return info

def fmt_time(sec):
    """Секунды → 'M:SS'."""
    m, s = divmod(int(sec), 60)
    return f"{m}:{s:02d}"
