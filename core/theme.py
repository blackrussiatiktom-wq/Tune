"""Tune - цвета, шрифты, градиенты"""
import os


class Theme:
    BG = "#000000"
    CARD = "#0A0A12"
    CARD_LIGHT = "#15151F"
    TEXT = "#FFFFFF"
    TEXT2 = "#8B8BA7"
    TEXT3 = "#5A5A6E"
    DIVIDER = "#1A1A24"

    GRAD_1 = "#FF2EBD"
    GRAD_2 = "#7B3DFF"
    GRAD_3 = "#00E5FF"
    ACCENT = "#7B3DFF"
    ACCENT_LIGHT = "#9B5DFF"

    FONTS_DIR = "assets/fonts"
    FONT_REGULAR = "Inter-Regular"
    FONT_MEDIUM = "Inter-Medium"
    FONT_SEMIBOLD = "Inter-SemiBold"
    FONT_BOLD = "Inter-Bold"

    SIZE_TINY = "10sp"
    SIZE_SMALL = "12sp"
    SIZE_BODY = "14sp"
    SIZE_BUTTON = "16sp"
    SIZE_SUBTITLE = "18sp"
    SIZE_TITLE = "22sp"
    SIZE_HEADER = "28sp"
    SIZE_LOGO = "36sp"

    @classmethod
    def rgba(cls, hex_color, alpha=1.0):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (alpha,)

    @classmethod
    def register_fonts(cls):
        """Регистрирует шрифты Inter. Логирует что получилось."""
        from kivy.core.text import LabelBase
        import traceback
        results = []
        
        # Пробуем несколько путей
        possible_dirs = []
        try:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            possible_dirs.append(os.path.join(base, "assets", "fonts"))
        except Exception:
            pass
        possible_dirs.append("assets/fonts")
        possible_dirs.append("./assets/fonts")
        
        fonts = [
            (cls.FONT_REGULAR, "Inter-Regular.ttf"),
            (cls.FONT_MEDIUM, "Inter-Medium.ttf"),
            (cls.FONT_SEMIBOLD, "Inter-SemiBold.ttf"),
            (cls.FONT_BOLD, "Inter-Bold.ttf"),
        ]
        
        for name, filename in fonts:
            loaded = False
            for base in possible_dirs:
                path = os.path.join(base, filename)
                if os.path.exists(path):
                    try:
                        LabelBase.register(name=name, fn_regular=path)
                        results.append(f"{name}: OK from {path}")
                        loaded = True
                        break
                    except Exception as e:
                        results.append(f"{name}: FAIL {e}")
            if not loaded:
                results.append(f"{name}: NOT FOUND in {possible_dirs}")
        
        # Логируем
        try:
            log_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "tune_log.txt"
            )
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("--- Font registration ---\n")
                for r in results:
                    f.write(f"  {r}\n")
        except Exception:
            pass
        
        return results
