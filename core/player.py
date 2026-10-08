"""Tune - воспроизведение через Kivy Audio"""
from kivy.core.audio import SoundLoader


class Player:
    def __init__(self):
        self.sound = None
        self.current_path = None
        self.is_playing = False

    def play(self, path):
        try:
            self.stop()
            self.sound = SoundLoader.load(path)
            if self.sound:
                self.sound.play()
                self.current_path = path
                self.is_playing = True
                return True
        except Exception as e:
            print(f"Player error: {e}")
        return False

    def toggle(self):
        if self.sound and self.is_playing:
            try:
                self.sound.stop()
                self.is_playing = False
            except Exception:
                pass
            return False
        elif self.sound:
            try:
                self.sound.play()
                self.is_playing = True
            except Exception:
                pass
            return True
        return False

    def stop(self):
        try:
            if self.sound:
                self.sound.stop()
                self.sound.unload()
        except Exception:
            pass
        self.sound = None
        self.is_playing = False
