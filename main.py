"""Tune v0.3.3 MINIMAL - проверка базы"""
import os
import sys
import traceback

# === БАЗА ===
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# Лог в папке где точно можно писать
LOG_FILE = os.path.join(PROJECT_DIR, "tune_log.txt")

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass

# Чистим лог
try:
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
except Exception:
    pass

log("=== START v0.3.3 ===")
log(f"PROJECT_DIR = {PROJECT_DIR}")
log(f"CWD = {os.getcwd()}")

# === KIVY ===
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.image import Image
    from kivy.core.window import Window
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.metrics import dp
    log("Kivy imported OK")
except Exception as e:
    log(f"KIVY FAIL: {e}\n{traceback.format_exc()}")

# === ПРИЛОЖЕНИЕ ===
class SimpleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        log("SimpleScreen init")
        
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(20))
        
        # Иконка
        icon_path = os.path.join(PROJECT_DIR, "assets", "icon.png")
        log(f"Icon path: {icon_path}, exists: {os.path.exists(icon_path)}")
        
        if os.path.exists(icon_path):
            img = Image(source=icon_path, size_hint=(1, 0.4))
            layout.add_widget(img)
        else:
            layout.add_widget(Label(text="[icon not found]", color=(1,1,1,1)))
        
        # Заголовок
        layout.add_widget(Label(
            text="Tune",
            font_size=dp(48),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.15),
        ))
        
        # Текст
        self.status = Label(
            text="Приложение работает!",
            font_size=dp(18),
            color=(0.7, 0.7, 0.8, 1),
            size_hint=(1, 0.15),
        )
        layout.add_widget(self.status)
        
        # Кнопка
        btn = Button(
            text="Проверить папки",
            font_size=dp(18),
            size_hint=(1, 0.15),
            background_color=(0.48, 0.24, 1, 1),
        )
        btn.bind(on_release=self.check_folders)
        layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def check_folders(self, *args):
        log("check_folders clicked")
        dirs = [
            "/storage/emulated/0/Music",
            "/storage/emulated/0/Download",
            "/sdcard/Music",
        ]
        found = []
        for d in dirs:
            if os.path.isdir(d):
                try:
                    files = os.listdir(d)
                    found.append(f"{d}: {len(files)} файлов")
                    log(f"OK {d}: {len(files)} files")
                except Exception as e:
                    found.append(f"{d}: ошибка {e}")
                    log(f"ERR {d}: {e}")
            else:
                log(f"NOT FOUND {d}")
        
        self.status.text = "\n".join(found[:3]) if found else "Папки не найдены"


class TuneMiniApp(App):
    def build(self):
        try:
            log("TuneMiniApp.build()")
            self.title = "Tune"
            Window.clearcolor = (0, 0, 0, 1)
            
            sm = ScreenManager()
            sm.add_widget(SimpleScreen(name="main"))
            log("ScreenManager OK")
            return sm
        except Exception as e:
            log(f"BUILD FAIL: {e}\n{traceback.format_exc()}")
            raise
    
    def on_start(self):
        log("App started OK")


if __name__ == "__main__":
    try:
        TuneMiniApp().run()
    except Exception as e:
        log(f"MAIN FAIL: {e}\n{traceback.format_exc()}")
        raise
