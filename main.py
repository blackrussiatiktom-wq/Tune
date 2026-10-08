"""Tune v0.3 - офлайн музыкальный плеер"""
import os
import sys
import traceback
from datetime import datetime

# Путь проекта
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# Файл логов на телефоне
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tune_crash.log")


def log(msg):
    """Пишет в файл лога на телефоне"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {msg}\n")
    except Exception:
        pass


def log_exception(where):
    """Логирует исключение"""
    log(f"\n=== ОШИБКА в {where} ===\n{traceback.format_exc()}\n")


# Логируем старт
try:
    os.remove(LOG_FILE)
except Exception:
    pass
log("=== ЗАПУСК TUNE v0.3 ===")
log(f"PROJECT_DIR = {PROJECT_DIR}")
log(f"sys.path = {sys.path[:3]}")

# Импортируем Kivy
try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.lang import Builder
    from kivy.metrics import dp
    log("Kivy импортирован OK")
except Exception:
    log_exception("import kivy")
    raise

# Импортируем наши модули
try:
    from core.theme import Theme
    from core.scanner import scan, filename_only
    from core.metadata import read_tags, fmt_time, is_hidden
    from core.player import Player
    from ui.widgets import TrackItem
    log("Наши модули импортированы OK")
except Exception:
    log_exception("import core/ui")
    raise


# Регистрируем шрифты СРАЗУ
try:
    Theme.register_fonts()
    log("Шрифты Inter зарегистрированы")
except Exception:
    log_exception("register_fonts")


# Загружаем .kv файлы
KV_FILES = ["ui/splash.kv", "ui/home.kv", "ui/player.kv"]
for kv in KV_FILES:
    try:
        path = os.path.join(PROJECT_DIR, kv)
        if os.path.exists(path):
            Builder.load_file(path)
            log(f"KV загружен: {kv}")
        else:
            log(f"KV НЕ НАЙДЕН: {path}")
    except Exception:
        log_exception(f"load {kv}")


class SplashScreen(Screen):
    def start_loading(self):
        try:
            progress_fill = self.ids.get("progress_fill")
            if not progress_fill:
                log("progress_fill не найден — пропускаем анимацию")
                Clock.schedule_once(lambda d: self.go_home(), 2.0)
                return

            steps = [i / 50.0 for i in range(51)]

            def animate(dt, step=0):
                if step < len(steps):
                    progress_fill.size_hint_x = max(0.01, steps[step])
                    Clock.schedule_once(lambda d: animate(d, step + 1), 0.05)
                else:
                    Clock.schedule_once(lambda d: self.go_home(), 0.2)

            animate(0)
        except Exception:
            log_exception("SplashScreen.start_loading")
            Clock.schedule_once(lambda d: self.go_home(), 1.0)

    def go_home(self):
        try:
            app = App.get_running_app()
            app.sm.current = "home"
        except Exception:
            log_exception("go_home")


class HomeScreen(Screen):
    def on_enter(self, *args):
        try:
            Clock.schedule_once(self.load_tracks, 0.1)
        except Exception:
            log_exception("HomeScreen.on_enter")

    def load_tracks(self, *args):
        try:
            log("Начинаем загрузку треков...")
            tracks_box = self.ids.get("tracks_box")
            if not tracks_box:
                log("tracks_box не найден!")
                return

            tracks_box.clear_widgets()
            paths = scan()
            log(f"Найдено файлов: {len(paths)}")

            app = App.get_running_app()
            app.tracks = []

            for i, path in enumerate(paths):
                try:
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
                except Exception:
                    log_exception(f"load track #{i}: {path}")

            log(f"Треков добавлено: {len(app.tracks)}")

            mini_title = self.ids.get("mini_title")
            if mini_title:
                if app.tracks:
                    mini_title.text = f"Найдено {len(app.tracks)} треков"
                else:
                    mini_title.text = "Треки не найдены"
        except Exception:
            log_exception("HomeScreen.load_tracks")

    def toggle_play(self, *args):
        try:
            app = App.get_running_app()
            if app.player.current_path:
                playing = app.player.toggle()
                btn = self.ids.get("mini_play_btn")
                if btn:
                    btn.text = "⏸" if playing else "▶"
        except Exception:
            log_exception("toggle_play")


class PlayerScreen(Screen):
    progress = 0.0

    def on_enter(self, *args):
        try:
            self.update_ui()
            Clock.schedule_interval(self.update_progress, 0.5)
        except Exception:
            log_exception("PlayerScreen.on_enter")

    def on_leave(self, *args):
        try:
            Clock.unschedule(self.update_progress)
        except Exception:
            pass

    def update_ui(self):
        try:
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
            play_btn = self.ids.get("play_btn")
            if play_btn:
                play_btn.text = "⏸" if app.player.is_playing else "▶"
        except Exception:
            log_exception("PlayerScreen.update_ui")

    def update_progress(self, dt):
        try:
            app = App.get_running_app()
            if not app.player.sound:
                return
            pos = app.player.get_position()
            dur = app.player.get_duration()
            if dur > 0:
                self.progress = pos / dur
            time_cur = self.ids.get("time_current")
            if time_cur:
                time_cur.text = fmt_time(pos)
        except Exception:
            pass

    def toggle_play(self, *args):
        try:
            app = App.get_running_app()
            playing = app.player.toggle()
            play_btn = self.ids.get("play_btn")
            if play_btn:
                play_btn.text = "⏸" if playing else "▶"
        except Exception:
            log_exception("PlayerScreen.toggle_play")

    def next_track(self, *args):
        try:
            App.get_running_app().play_next()
        except Exception:
            log_exception("next_track")

    def prev_track(self, *args):
        try:
            App.get_running_app().play_prev()
        except Exception:
            log_exception("prev_track")

    def go_back(self, *args):
        try:
            App.get_running_app().sm.current = "home"
        except Exception:
            log_exception("go_back")


class TuneApp(App):
    def build(self):
        try:
            log("TuneApp.build() начался")
            Window.clearcolor = (0, 0, 0, 1)
            self.title = "Tune"
            self.tracks = []
            self.current_index = -1
            self.current_track = None
            self.player = Player()

            log("Создаём ScreenManager")
            self.sm = ScreenManager(transition=FadeTransition())
            self.sm.add_widget(SplashScreen(name="splash"))
            self.sm.add_widget(HomeScreen(name="home"))
            self.sm.add_widget(PlayerScreen(name="player"))

            log("ScreenManager готов")
            Clock.schedule_once(
                lambda dt: self.sm.get_screen("splash").start_loading(), 0.5
            )
            log("TuneApp.build() завершён OK")
            return self.sm
        except Exception:
            log_exception("TuneApp.build")
            raise

    def on_start(self):
        log("TuneApp.on_start() — приложение запущено")

    def play_track(self, path):
        try:
            log(f"play_track: {path}")
            for i, t in enumerate(self.tracks):
                if t["path"] == path:
                    self.current_index = i
                    self.current_track = t
                    break
            if self.player.play(path):
                self.player.set_on_finish(self._on_track_finish)
                self.sm.current = "player"
        except Exception:
            log_exception("play_track")

    def play_next(self):
        try:
            if not self.tracks:
                return
            self.current_index = (self.current_index + 1) % len(self.tracks)
            self.play_track(self.tracks[self.current_index]["path"])
        except Exception:
            log_exception("play_next")

    def play_prev(self):
        try:
            if not self.tracks:
                return
            self.current_index = (self.current_index - 1) % len(self.tracks)
            self.play_track(self.tracks[self.current_index]["path"])
        except Exception:
            log_exception("play_prev")

    def _on_track_finish(self):
        try:
            Clock.schedule_once(lambda dt: self.play_next(), 0.5)
        except Exception:
            pass


if __name__ == "__main__":
    try:
        TuneApp().run()
    except Exception:
        log_exception("MAIN")
        raise
