"""Tune - чтение тегов треков через mutagen"""
import os

try:
    from mutagen import File as MutaFile
    from mutagen.id3 import ID3
    MUTAGEN_OK = True
except ImportError:
    MUTAGEN_OK = False


# Скрытые треки (сохраняется в файл)
HIDDEN_FILE = os.path.expanduser("~/.tune_hidden.txt")


def _load_hidden():
    if not os.path.exists(HIDDEN_FILE):
        return set()
    try:
        with open(HIDDEN_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception:
        return set()


def _save_hidden(hidden_set):
    try:
        with open(HIDDEN_FILE, "w") as f:
            for path in hidden_set:
                f.write(path + "\n")
    except Exception:
        pass


def hide_track(path):
    hidden = _load_hidden()
    hidden.add(path)
    _save_hidden(hidden)


def unhide_track(path):
    hidden = _load_hidden()
    hidden.discard(path)
    _save_hidden(hidden)


def is_hidden(path):
    return path in _load_hidden()


def read_tags(path):
    """Читает теги, возвращает dict"""
    info = {
        "path": path,
        "title": os.path.splitext(os.path.basename(path))[0],
        "artist": "Неизвестен",
        "album": "",
        "duration": 0,
        "has_cover": False,
    }

    if not MUTAGEN_OK:
        return info

    try:
        audio = MutaFile(path)
        if audio is None:
            return info

        # Длительность
        if hasattr(audio, "info") and audio.info:
            info["duration"] = int(audio.info.length)

        # Теги
        if audio.tags:
            for key_title in ("TIT2", "title", "\xa9nam"):
                if key_title in audio.tags:
                    info["title"] = str(audio.tags[key_title])
                    break

            for key_artist in ("TPE1", "artist", "\xa9ART"):
                if key_artist in audio.tags:
                    info["artist"] = str(audio.tags[key_artist])
                    break

            for key_album in ("TALB", "album", "\xa9alb"):
                if key_album in audio.tags:
                    info["album"] = str(audio.tags[key_album])
                    break

            # Обложка
            if isinstance(audio.tags, ID3):
                if "APIC:" in str(audio.tags.keys()) or any(
                    k.startswith("APIC") for k in audio.tags.keys()
                ):
                    info["has_cover"] = True

    except Exception:
        pass

    return info


def fmt_time(seconds):
    """Секунды -> 'M:SS'"""
    if not seconds:
        return "0:00"
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"
