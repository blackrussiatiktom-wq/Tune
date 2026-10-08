"""Tune - воспроизведение через Kivy Audio"""
from kivy.core.audio import SoundLoader


class Player:
    def __init__(self):
        self.sound = None
        self.current_path = None
        self.is_playing = False
        self.on_finish_callback = None

    def load(self, path):
        """Загружает трек"""
        self.stop()
        try:
            self.sound = SoundLoader.load(path)
            if self.sound:
                self.current_path = path
                self.sound.bind(on_stop=self._on_finish)
                return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
        return False

    def play(self, path=None):
        """Запускает воспроизведение"""
        if path and path != self.current_path:
            if not self.load(path):
                return False

        if self.sound:
            try:
                self.sound.play()
                self.is_playing = True
                return True
            except Exception as e:
                print(f"Ошибка воспроизведения: {e}")
        return False

    def pause(self):
        if self.sound and self.is_playing:
            self.sound.stop()
            self.is_playing = False

    def toggle(self):
        """Play/Pause"""
        if self.is_playing:
            self.pause()
            return False
        else:
            return self.play()

    def stop(self):
        if self.sound:
            try:
                self.sound.stop()
                self.sound.unload()
            except Exception:
                pass
        self.sound = None
        self.is_playing = False

    def seek(self, position):
        """Перемотка (ограничение Kivy)"""
        if self.sound and hasattr(self.sound, "seek"):
            try:
                self.sound.seek(position)
            except Exception:
                pass

    def get_position(self):
        if self.sound and hasattr(self.sound, "get_pos"):
            try:
                return self.sound.get_pos()
            except Exception:
                return 0
        return 0

    def get_duration(self):
        if self.sound and hasattr(self.sound, "length"):
            try:
                return self.sound.length
            except Exception:
                return 0
        return 0

    def set_on_finish(self, callback):
        self.on_finish_callback = callback

    def _on_finish(self, *args):
        self.is_playing = False
        if self.on_finish_callback:
            self.on_finish_callback()
