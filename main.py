"""Tune — офлайн-плеер. Точка входа."""
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp

from core.theme import Theme
from core.scanner import scan, fmt_time
from core.player import MpvPlayer


MUSIC_DIR = os.path.expanduser("~/storage/music")
if not os.path.isdir(MUSIC_DIR):
    MUSIC_DIR = os.path.expanduser("~/Music")


class RoundedButton(Button):
    """Кнопка с закруглёнными углами и градиентом (упрощённый)."""
    def __init__(self, bg="#1A1A24", radius=16, **kw):
        super().__init__(**kw)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg
        self.radius = radius
        with self.canvas.before:
            self._color = Color(*Theme.DARK["grad"][1:2] and (0.1, 0.1, 0.1, 1))
            # упрощённо: однотонный фон (градиент добавим позже)
            from kivy.graphics import Color as C
        self.bind(pos=self._update, size=self._update)
        self._update()

    def _update(self, *a):
        self.canvas.before.clear()
        from kivy.graphics import Color as C
        hexbg = self.bg_color.lstrip("#")
        rgba = tuple(int(hexbg[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)
        with self.canvas.before:
            C(*rgba)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])


class PlayerScreen(Screen):
    def __init__(self, theme, **kw):
        super().__init__(**kw)
        self.theme = theme
        self.tracks = []
        self.idx = 0
        self.player = MpvPlayer()

        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        # Заголовок
        self.title_lbl = Label(
            text="Tune",
            font_size=dp(32),
            bold=True,
            size_hint=(1, 0.1),
            color=self._rgba(theme.c["text"]),
        )
        root.add_widget(self.title_lbl)

        # Список треков
        scroll = ScrollView(size_hint=(1, 0.65))
        self.list_box = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=dp(6)
        )
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        scroll.add_widget(self.list_box)
        root.add_widget(scroll)

        # Название текущего
        self.now_lbl = Label(
            text="—",
            font_size=dp(16),
            size_hint=(1, 0.08),
            color=self._rgba(theme.c["text2"]),
        )
        root.add_widget(self.now_lbl)

        # Кнопки управления
        controls = BoxLayout(size_hint=(1, 0.17), spacing=dp(10))
        self.prev_btn = RoundedButton(text="⏮", font_size=dp(24), bg=theme.c["card"])
        self.play_btn = RoundedButton(text="▶", font_size=dp(28), bg=theme.c["card"])
        self.next_btn = RoundedButton(text="⏭", font_size=dp(24), bg=theme.c["card"])
        self.theme_btn = RoundedButton(text="☀", font_size=dp(20), bg=theme.c["card"])

        self.play_btn.bind(on_release=self.toggle_play)
        self.prev_btn.bind(on_release=lambda *_: self.play_offset(-1))
        self.next_btn.bind(on_release=lambda *_: self.play_offset(1))
        self.theme_btn.bind(on_release=self.toggle_theme)

        for b in (self.prev_btn, self.play_btn, self.next_btn, self.theme_btn):
            controls.add_widget(b)
        root.add_widget(controls)

        self.add_widget(root)
        Clock.schedule_once(self.load_tracks, 0.1)
        Clock.schedule_interval(self.check_end, 1.0)

    def _rgba(self, hexc):
        h = hexc.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)

    def load_tracks(self, *a):
        self.tracks = scan(MUSIC_DIR)
        self.list_box.clear_widgets()
        if not self.tracks:
            self.list_box.add_widget(Label(
                text=f"Нет музыки в:\n{MUSIC_DIR}",
                color=self._rgba(self.theme.c["text2"]),
                size_hint_y=None, height=dp(80),
            ))
            return
        for i, t in enumerate(self.tracks):
            b = Button(
                text=f"{t['artist']} — {t['title']}",
                size_hint_y=None,
                height=dp(52),
                background_normal="",
                background_color=self._rgba(self.theme.c["card"]),
                color=self._rgba(self.theme.c["text"]),
                halign="left",
                valign="middle",
            )
            b.bind(size=lambda inst, *_: setattr(inst, "text_size", (inst.width - dp(20), inst.height)))
            b.bind(on_release=lambda inst, ix=i: self.play_index(ix))
            self.list_box.add_widget(b)

    def play_index(self, i):
        if not self.tracks:
            return
        self.idx = i % len(self.tracks)
        t = self.tracks[self.idx]
        if self.player.play(t["path"]):
            self.now_lbl.text = f"▶ {t['artist']} — {t['title']}"
            self.play_btn.text = "⏸"

    def play_offset(self, d):
        if self.tracks:
            self.play_index(self.idx + d)

    def toggle_play(self, *a):
        if self.player.is_playing():
            self.player.pause()
            self.play_btn.text = "▶"
        else:
            if self.player.current:
                self.play_index(self.idx)
            else:
                self.play_index(0)

    def toggle_theme(self, *a):
        mode = self.theme.toggle()
        self.apply_theme()

    def apply_theme(self):
        c = self.theme.c
        Window.clearcolor = self._rgba(c["bg"])
        self.title_lbl.color = self._rgba(c["text"])
        self.now_lbl.color = self._rgba(c["text2"])
        for b in (self.prev_btn, self.play_btn, self.next_btn, self.theme_btn):
            b.bg_color = c["card"]
            b.color = self._rgba(c["text"])
            b._update()
        # перерисовать список
        self.load_tracks()

    def check_end(self, *a):
        if self.player.current and not self.player.is_playing():
            # трек закончился — играем следующий
            if self.play_btn.text == "⏸":
                self.play_offset(1)


class TuneApp(App):
    def build(self):
        self.title = "Tune"
        self.theme = Theme("dark")
        Window.clearcolor = (0, 0, 0, 1)
        sm = ScreenManager()
        sm.add_widget(PlayerScreen(self.theme, name="player"))
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    TuneApp().run()
