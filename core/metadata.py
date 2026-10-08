"""Tune - чтение тегов"""
import os
try:
    from mutagen import File as MutaFile
    OK = True
except ImportError:
    OK = False


def read_tags(path):
    info = {
        "path": path,
        "title": os.path.splitext(os.path.basename(path))[0],
        "artist": "Неизвестен",
        "duration": 0,
    }
    if not OK:
        return info
    try:
        audio = MutaFile(path)
        if audio is None:
            return info
        if hasattr(audio, "info") and audio.info:
            info["duration"] = int(audio.info.length)
        if audio.tags:
            for k in ("TIT2", "title", "\xa9nam"):
                if k in audio.tags:
                    info["title"] = str(audio.tags[k])
                    break
            for k in ("TPE1", "artist", "\xa9ART"):
                if k in audio.tags:
                    info["artist"] = str(audio.tags[k])
                    break
    except Exception:
        pass
    return info


def fmt_time(sec):
    if not sec:
        return "0:00"
    m, s = divmod(int(sec), 60)
    return f"{m}:{s:02d}"
