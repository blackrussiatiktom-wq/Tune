"""Tune v0.3.5 - 3 экрана: splash, home, player"""
import os
import sys
import traceback

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

LOG_FILE = os.path.join(PROJECT_DIR, "tune_log.txt")


def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{msg}\n")
    except Exception:
        pass


try:
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
except Exception:
    pass

log("=== START v0.3.5 ===")
log(f"PROJECT_DIR = {PROJECT_DIR}")

# Kivy
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.image import Image
    from kivy.uix.scrollview import ScrollView
    from kivy.core.window import Window
    from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
    from kivy.clock import Clock
    from kivy.lang import Builder
    from kivy.metrics import dp
    log("Kivy OK")
except Exception as e:
    log(f"KIVY FAIL: {e}\n{traceback.format_exc()}")
    raise

# Core
try:
    from core.scanner import scan
    from core.metadata import read_tags, fmt_time
    from core.player import Player
    from core.theme import Theme
    log("Core OK")
except Exception as e:
    log(f"CORE FAIL: {e}\n{traceback.format_exc()}")
    raise

# UI widgets
try:
    from ui.widgets import TrackItem
    log("Widgets OK")
except Exception as e:
    log(f"WIDGETS FAIL: {e}\n{traceback.format_exc()}")
    # Не падаем — продолжаем без TrackItem
    
    class TrackItem(BoxLayout):
        pass

# Шрифты
try:
    results = Theme.register_fonts()
    log(f"Fonts result: {results}")
except Exception as e:
    log(f"FONTS FAIL: {e}\n{traceback.format_exc()}")

# KV файлы
KV_FILES = ["ui/splash.kv", "ui/home.kv", "ui/player.kv"]
for kv in KV_FILES:
    try:
        path = os.path.join(PROJECT_DIR, kv)
        if os.path.exists(path):
            Builder.load_file(path)
            log(f"KV loaded: {kv}")
        else:
            log(f"KV NOT FOUND: {path}")
    except Exception as e:
        log(f"KV FAIL {kv}: {e}\n{traceback.format_exc()}")


# ========== ЭКРАНЫ ==========

class SplashScreen(Screen):
    def on_enter(self, *args):
        try:
            log("SplashScreen.on_enter")
            Clock.schedule_once(self.go_home, 2.0)
        except Exception as e:
            log(f"SPLASH FAIL: {e}\n{traceback.format_exc()}")

    def go_home(self, *args):
        try:
            App.get_running_app().sm.current = "home"
            log("Splash -> Home")
        except Exception as e:
            log(f"GO_HOME FAIL: {e}\n{traceback.format_exc()}")


class HomeScreen(Screen):
    def on_enter(self, *args):
        try:
            log("HomeScreen.on_enter")
            btn = self.ids.get("load_btn")
            if btn:
                btn.bind(on_release=self.load_tracks)
            btn2 = self.ids.get("go_player_btn")
            if btn2:
                btn2.bind(on_release=self.go_player)
        except Exception as e:
            log(f"HOME INIT FAIL: {e}\n{traceback.format_exc()}")

    def load_tracks(self, *args):
        try:
            log("load_tracks()")
            box = self.ids.get("tracks_box")
            if not box:
                log("tracks_box NOT FOUND")
                return
            box.clear_widgets()
            paths = scan()
            log(f"Найдено: {len(paths)}")
            
            app = App.get_running_app()
            app.tracks = []
            
            for p in paths:
                try:
                    info = read_tags(p)
                    app.tracks.append(info)
                    item = TrackItem(
                        title=info["title"],
                        artist=info["artist"],
                        duration=fmt_time(info["duration"]),
                    )
                    item.bind(on_release=lambda inst, path=p: app.play_track(path))
                    box.add_widget(item)
                except Exception as e:
                    log(f"Track fail: {e}")
            
            log(f"Треков добавлено: {len(app.tracks)}")
        except Exception as e:
            log(f"LOAD FAIL: {e}\n{traceback.format_exc()}")

    def go_player(self, *args):
        try:
            App.get_running_app().sm.current = "player"
        except Exception as e:
            log(f"GO_PLAYER FAIL: {e}")


class PlayerScreen(Screen):
    def on_enter(self, *args):
        try:
            log("PlayerScreen.on_enter")
            app = App.get_running_app()
            if app.current_track:
                title = self.ids.get("player_title")
                artist = self.ids.get("player_artist")
                if title:
                    title.text = app.current_track.get("title", "")
                if artist:
                    artist.text = app.current_track.get("artist", "")
        except Exception as e:
            log(f"PLAYER FAIL: {e}\n{traceback.format_exc()}")

    def toggle_play(self, *args):
        try:
            app = App.get_running_app()
            if app.player:
                app.player.toggle()
        except Exception as e:
            log(f"TOGGLE FAIL: {e}")

    def go_back(self, *args):
        try:
            App.get_running_app().sm.current = "home"
        except Exception as e:
            log(f"BACK FAIL: {e}")


class TuneApp(App):
    def build(self):
        try:
            log("build() start")
            self.title = "Tune"
            Window.clearcolor = (0, 0, 0, 1)
            self.tracks = []
            self.current_track = None
            self.player = Player()
            
            self.sm = ScreenManager(transition=FadeTransition())
            
            log("Adding SplashScreen")
            self.sm.add_widget(SplashScreen(name="splash"))
            
            log("Adding HomeScreen")
            self.sm.add_widget(HomeScreen(name="home"))
            
            log("Adding PlayerScreen")
            self.sm.add_widget(PlayerScreen(name="player"))
            
            log("build() OK")
            return self.sm
        except Exception as e:
            log(f"BUILD FAIL: {e}\n{traceback.format_exc()}")
            raise

    def on_start(self):
        log("App started")

    def play_track(self, path):
        try:
            log(f"play_track: {path}")
            for t in self.tracks:
                if t["path"] == path:
                    self.current_track = t
                    break
            if self.player.play(path):
                self.sm.current = "player"
        except Exception as e:
            log(f"PLAY FAIL: {e}\n{traceback.format_exc()}")


if __name__ == "__main__":
    try:
        TuneApp().run()
    except Exception as e:
        log(f"MAIN FAIL: {e}\n{traceback.format_exc()}")
        raise
