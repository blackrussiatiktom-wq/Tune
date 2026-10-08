"""Tune - кастомные виджеты"""
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp

from core.theme import Theme


class GradientButton(Button):
    """Кнопка с градиентным фоном"""
    grad_start = ListProperty([1, 0.18, 0.74, 1])   # фуксия
    grad_end = ListProperty([0, 0.9, 1, 1])          # циан
    radius = NumericProperty(dp(28))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.font_name = Theme.FONT_SEMIBOLD
        self.font_size = Theme.SIZE_BUTTON
        self.color = (1, 1, 1, 1)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Упрощённый градиент (в Kivy нельзя напрямую, используем два прямоугольника)
            Color(*self.grad_start)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])


class RoundedCard(BoxLayout):
    """Скруглённая карточка"""
    bg_color = ListProperty([0.04, 0.04, 0.07, 1])
    radius = NumericProperty(dp(16))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])


class IconButton(ButtonBehavior, Image):
    """Кнопка-иконка"""
    pass


class ProgressSlider(BoxLayout):
    """Прогресс-бар для трека"""
    value = NumericProperty(0)       # 0.0 - 1.0
    fill_color = ListProperty([0.48, 0.24, 1, 1])  # фиолет
    bg_color = ListProperty([0.15, 0.15, 0.2, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(20)
        self.bind(pos=self._update, size=self._update, value=self._update)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Фон
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=(self.width, dp(3)))

            # Заполнение
            Color(*self.fill_color)
            fill_w = self.width * max(0.0, min(1.0, self.value))
            Rectangle(pos=self.pos, size=(fill_w, dp(3)))

            # Кружок-маркер
            from kivy.graphics import Ellipse
            Color(*self.fill_color)
            Ellipse(
                pos=(self.x + fill_w - dp(7), self.y + dp(1.5) - dp(7)),
                size=(dp(14), dp(14))
            )


class TrackItem(ButtonBehavior, BoxLayout):
    """Элемент списка треков"""
    title = StringProperty("")
    artist = StringProperty("")
    duration = StringProperty("0:00")
    is_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(64)
        self.padding = (dp(12), dp(8))
        self.spacing = dp(12)

        from kivy.uix.label import Label
        from kivy.uix.image import Image as KivyImage

        # Обложка-заглушка
        cover = KivyImage(
            source="assets/icon.png",
            size_hint=(None, 1),
            width=dp(48),
        )
        self.add_widget(cover)

        # Текст
        text_box = BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.title_label = Label(
            text=self.title,
            font_name=Theme.FONT_SEMIBOLD,
            font_size=Theme.SIZE_BODY,
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
        )
        self.title_label.bind(size=lambda *_: setattr(self.title_label, "text_size", self.title_label.size))

        self.artist_label = Label(
            text=self.artist,
            font_name=Theme.FONT_REGULAR,
            font_size=Theme.SIZE_SMALL,
            color=(0.55, 0.55, 0.68, 1),
            halign="left",
            valign="middle",
        )
        self.artist_label.bind(size=lambda *_: setattr(self.artist_label, "text_size", self.artist_label.size))

        text_box.add_widget(self.title_label)
        text_box.add_widget(self.artist_label)
        self.add_widget(text_box)

        # Время
        self.dur_label = Label(
            text=self.duration,
            font_name=Theme.FONT_MEDIUM,
            font_size=Theme.SIZE_SMALL,
            color=(0.55, 0.55, 0.68, 1),
            size_hint=(None, 1),
            width=dp(48),
        )
        self.add_widget(self.dur_label)

        self.bind(title=self._on_title, artist=self._on_artist, duration=self._on_duration)

    def _on_title(self, *args):
        if hasattr(self, "title_label"):
            self.title_label.text = self.title

    def _on_artist(self, *args):
        if hasattr(self, "artist_label"):
            self.artist_label.text = self.artist

    def _on_duration(self, *args):
        if hasattr(self, "dur_label"):
            self.dur_label.text = self.duration
