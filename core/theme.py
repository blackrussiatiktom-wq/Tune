"""Tune - цвета, шрифты, градиенты"""

import os


class Theme:
    # Основные цвета
    BG = "#000000"
    CARD = "#0A0A12"
    CARD_LIGHT = "#15151F"
    TEXT = "#FFFFFF"
    TEXT2 = "#8B8BA7"
    TEXT3 = "#5A5A6E"
    DIVIDER = "#1A1A24"

    # Неон-градиент (акцент)
    GRAD_1 = "#FF2EBD"  # фуксия
    GRAD_2 = "#7B3DFF"  # фиолет
    GRAD_3 = "#00E5FF"  # циан
    ACCENT = "#7B3DFF"  # основной акцент
    ACCENT_LIGHT = "#9B5DFF"

    # Шрифты Inter
    FONTS_DIR = "assets/fonts"
    FONT_REGULAR = "Inter-Regular"
    FONT_MEDIUM = "Inter-Medium"
    FONT_SEMIBOLD = "Inter-SemiBold"
    FONT_BOLD = "Inter-Bold"

    # Размеры
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
        """#RRGGBB -> (r, g, b, a)"""
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (alpha,)

    @classmethod
    def register_fonts(cls):
        """Регистрирует шрифты Inter в Kivy"""
        from kivy.core.text import LabelBase
        base = os.path.expanduser("~/tune/" + cls.FONTS_DIR)
        # Fallback если запуск из другой папки
        if not os.path.isdir(base):
            base = cls.FONTS_DIR

        fonts = [
            (cls.FONT_REGULAR, "Inter-Regular.ttf"),
            (cls.FONT_MEDIUM, "Inter-Medium.ttf"),
            (cls.FONT_SEMIBOLD, "Inter-SemiBold.ttf"),
            (cls.FONT_BOLD, "Inter-Bold.ttf"),
        ]
        for name, filename in fonts:
            path = os.path.join(base, filename)
            if os.path.exists(path):
                LabelBase.register(name=name, fn_regular=path)
