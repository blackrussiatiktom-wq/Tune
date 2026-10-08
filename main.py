"""Tune v0.3.6 - MINIMAL: только 1 экран с треками"""
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

log("=== START v0.3.6 ===")

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.image import Image
    from kivy.uix.scrollview import ScrollView
    from kivy.core.window import Window
    from kivy.metrics import dp
    log("Kivy OK")
except Exception as e:
    log(f"KIVY FAIL: {e}\n{traceback.format_exc()}")
    raise

try:
    from core.scanner import scan
    from core.metadata import read_tags, fmt_time
    log("core OK")
except Exception as e:
    log(f"CORE FAIL: {e}\n{traceback.format_exc()}")
    raise


class TuneRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log("TuneRoot init")
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(12)

        # Заголовок
        try:
            title = Label(
                text="Tune",
                font_size=dp(36),
                color=(1, 1, 1, 1),
                size_hint=(1, 0.15),
            )
            self.add_widget(title)
            log("Title added")
        except Exception as e:
            log(f"Title fail: {e}")

        # Статус
        self.status = Label(
            text="Нажми кнопку",
            font_size=dp(14),
            color=(0.7, 0.7, 0.8, 1),
            size_hint=(1, 0.08),
        )
        self.add_widget(self.status)

        # Скролл
        try:
            scroll = ScrollView(size_hint=(1, 0.65))
            self.list_box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                spacing=dp(2),
            )
            self.list_box.bind(minimum_height=self.list_box.setter("height"))
            scroll.add_widget(self.list_box)
            self.add_widget(scroll)
            log("ScrollView added")
        except Exception as e:
            log(f"Scroll fail: {e}")

        # Кнопка
        btn = Button(
            text="Загрузить треки",
            font_size=dp(16),
            size_hint=(1, 0.12),
            background_color=(0.48, 0.24, 1, 1),
        )
        btn.bind(on_release=self.load)
        self.add_widget(btn)

    def load(self, *args):
        log("load clicked")
        try:
            paths = scan()
            log(f"Найдено: {len(paths)}")
            self.list_box.clear_widgets()
            for p in paths:
                try:
                    info = read_tags(p)
                    txt = f"{info['artist']} - {info['title']}"
                    lbl = Label(
                        text=txt,
                        font_size=dp(13),
                        color=(1, 1, 1, 1),
                        size_hint_y=None,
                        height=dp(36),
                        halign="left",
                        valign="middle",
                    )
                    lbl.bind(size=lambda i, *_: setattr(i, "text_size", i.size))
                    self.list_box.add_widget(lbl)
                except Exception as e:
                    log(f"Track fail: {e}")
            self.status.text = f"Загружено {len(paths)}"
            log("load done")
        except Exception as e:
            log(f"LOAD FAIL: {e}\n{traceback.format_exc()}")


class TuneApp(App):
    def build(self):
        try:
            log("build start")
            self.title = "Tune"
            Window.clearcolor = (0, 0, 0, 1)
            root = TuneRoot()
            log("build OK")
            return root
        except Exception as e:
            log(f"BUILD FAIL: {e}\n{traceback.format_exc()}")
            # Возвращаем заглушку чтобы приложение не крашилось
            return Label(text=f"Error: {e}", color=(1, 0, 0, 1))


if __name__ == "__main__":
    try:
        TuneApp().run()
    except Exception as e:
        log(f"MAIN FAIL: {e}\n{traceback.format_exc()}")
        raise
