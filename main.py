"""Tune v0.3 - офлайн музыкальный плеер"""
import os
import sys

# Добавляем путь проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp

from core.theme import Theme
from core.scanner import scan, filename_only
from core.metadata import read_tags, fmt_time, is_hidden
from core.player import Player
from ui.widgets import TrackItem


# Подключаем .kv файлы
KV_FILES = [
    "ui/splash.kv",
    "ui/home.kv",
    "ui/player.kv",
]
for kv in KV_FILES:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), kv)
    if os.path.exists(path):
        Builder.load_file(path)
    else:
        Builder.load_file(kv)


class SplashScreen(Screen):
    def start_loading(self):
        """Анимация прогресс-бара + загрузка треков"""
        progress_fill = self.ids.get("progress_fill")
        if not progress_fill:
            return

        # Анимация 0 -> 1 за 2.5 сек
        steps = [i / 50.0 for i in range(51)]

        def animate(dt, step=0):
            if step < len(steps):
                progress_fill.size_hint_x = max(0.01, steps[step])
                Clock.schedule_once(lambda d: animate(d, step + 1), 0.05)
            else:
                # Готово - переходим на главный
                Clock.schedule_once(lambda d: self.go_home(), 0.2)

        animate(0)

    def go_home(self):
        app = App.get_running_app()
        app.sm.current = "home"


class HomeScreen(Screen):
    def on_enter(self, *args):
        """Загружаем список треков"""
        Clock.schedule_once(self.load_tracks, 0.1)

    def load_tracks(self, *args):
        tracks_box = self.ids.get("tracks_box")
        if not tracks_box:
            return
        tracks_box.clear_widgets()

        paths = scan()
        app = App.get_running_app()
        app.tracks = []

        for path in paths:
            if is_hidden(path):
                continue
            info = read_tags(path)
            app.tracks.append(info)

            item = TrackItem(
                title=info["title"],
                artist=info["artist"],
                duration=fmt_time(info["duration"]),
            )
            item.bind(on_release=lambda inst, p=path: app.play_track(p))
            tracks_box.add_widget(item)

        # Обновляем mini-player
        mini_title = self.ids.get("mini_title")
        if mini_title:
            if app.tracks:
                mini_title.text = f"Найдено {len(app.tracks)} треков"
            else:
                mini_title.text = "Треки не найдены"

    def toggle_play(self, *args):
        """Play/Pause из мини-плеера"""
        app = App.get_running_app()
        if app.player.current_path:
            playing = app.player.toggle()
            btn = self.ids.get("mini_play_btn")
            if btn:
                btn.text = "⏸" if playing else "▶"


class PlayerScreen(Screen):
    progress = 0.0

    def on_enter(self, *args):
        """Обновляем UI плеера"""
        self.update_ui()
        # Таймер обновления прогресса
        Clock.schedule_interval(self.update_progress, 0.5)

    def on_leave(self, *args):
        Clock.unschedule(self.update_progress)

    def update_ui(self):
        app = App.get_running_app()
        info = app.current_track
        if not info:
            return

        title = self.ids.get("player_title")
        artist = self.ids.get("player_artist")
        total = self.ids.get("time_total")

        if title:
            title.text = info.get("title", "Без названия")
        if artist:
            artist.text = info.get("artist", "Неизвестен")
        if total:
            total.text = fmt_time(info.get("duration", 0))

        # Кнопка Play/Pause
        play_btn = self.ids.get("play_btn")
        if play_btn:
            play_btn.text = "⏸" if app.player.is_playing else "▶"

    def update_progress(self, dt):
        """Обновляет прогресс-бар"""
        app = App.get_running_app()
        if not app.player.sound:
            return

        pos = app.player.get_position()
        dur = app.player.get_duration()

        if dur > 0:
            self.progress = pos / dur
        else:
            self.progress = 0

        time_cur = self.ids.get("time_current")
        if time_cur:
            time_cur.text = fmt_time(pos)

    def toggle_play(self, *args):
        app = App.get_running_app()
        playing = app.player.toggle()
        play_btn = self.ids.get("play_btn")
        if play_btn:
            play_btn.text = "⏸" if playing else "▶"

    def next_track(self, *args):
        App.get_running_app().play_next()

    def prev_track(self, *args):
        App.get_running_app().play_prev()

    def go_back(self, *args):
        App.get_running_app().sm.current = "home"


class TuneApp(App):
    def build(self):
        # Регистрируем шрифты
        Theme.register_fonts()

        # Чёрный фон окна
        Window.clearcolor = (0, 0, 0, 1)

        self.title = "Tune"
        self.tracks = []
        self.current_index = -1
        self.current_track = None
        self.player = Player()

        # ScreenManager
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(SplashScreen(name="splash"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(PlayerScreen(name="player"))

        # После сборки - стартуем загрузку
        Clock.schedule_once(lambda dt: self.sm.get_screen("splash").start_loading(), 0.5)

        return self.sm

    def play_track(self, path):
        """Воспроизвести трек"""
        # Находим индекс
        for i, t in enumerate(self.tracks):
            if t["path"] == path:
                self.current_index = i
                self.current_track = t
                break

        if self.player.play(path):
            self.player.set_on_finish(self._on_track_finish)
            # Обновляем мини-плеер
            mini_title = self.sm.get_screen("home").ids.get("mini_title")
            mini_artist = self.sm.get_screen("home").ids.get("mini_artist")
            mini_btn = self.sm.get_screen("home").ids.get("mini_play_btn")
            if mini_title:
                mini_title.text = self.current_track.get("title", "")
            if mini_artist:
                mini_artist.text = self.current_track.get("artist", "")
            if mini_btn:
                mini_btn.text = "⏸"

            # Переходим на экран плеера
            self.sm.current = "player"

    def play_next(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play_track(self.tracks[self.current_index]["path"])

    def play_prev(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play_track(self.tracks[self.current_index]["path"])

    def _on_track_finish(self):
        Clock.schedule_once(lambda dt: self.play_next(), 0.5)


if __name__ == "__main__":
    TuneApp().run()
