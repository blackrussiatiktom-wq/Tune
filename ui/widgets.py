"""Tune - кастомные виджеты (упрощённая версия)"""
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, BooleanProperty
)
from kivy.uix.label import Label
from kivy.metrics import dp


class GradientButton(Button):
    grad_start = ListProperty([1, 0.18, 0.74, 1])
    grad_end = ListProperty([0, 0.9, 1, 1])
    radius = NumericProperty(dp(28))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.grad_start)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])


class TrackItem(ButtonBehavior, BoxLayout):
    title = StringProperty("")
    artist = StringProperty("")
    duration = StringProperty("0:00")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(64)
        self.padding = (dp(12), dp(8))
        self.spacing = dp(12)

        # Обложка-заглушка
        try:
            cover = Image(
                source="assets/icon.png",
                size_hint=(None, 1),
                width=dp(48),
            )
            self.add_widget(cover)
        except Exception:
            pass

        # Текст
        text_box = BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.title_label = Label(
            text=self.title,
            font_size=dp(14),
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
        )
        self.title_label.bind(
            size=lambda inst, *_: setattr(inst, "text_size", inst.size)
        )

        self.artist_label = Label(
            text=self.artist,
            font_size=dp(12),
            color=(0.55, 0.55, 0.68, 1),
            halign="left",
            valign="middle",
        )
        self.artist_label.bind(
            size=lambda inst, *_: setattr(inst, "text_size", inst.size)
        )

        text_box.add_widget(self.title_label)
        text_box.add_widget(self.artist_label)
        self.add_widget(text_box)

        # Время
        self.dur_label = Label(
            text=self.duration,
            font_size=dp(12),
            color=(0.55, 0.55, 0.68, 1),
            size_hint=(None, 1),
            width=dp(48),
        )
        self.add_widget(self.dur_label)

        self.bind(title=self._on_title, artist=self._on_artist, duration=self._on_dur)

    def _on_title(self, *args):
        if hasattr(self, "title_label"):
            self.title_label.text = self.title

    def _on_artist(self, *args):
        if hasattr(self, "artist_label"):
            self.artist_label.text = self.artist

    def _on_dur(self, *args):
        if hasattr(self, "dur_label"):
            self.dur_label.text = self.duration
