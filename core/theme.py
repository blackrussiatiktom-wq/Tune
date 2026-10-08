"""Tune - цвета"""
class Theme:
    BG = "#000000"
    CARD = "#0A0A12"
    TEXT = "#FFFFFF"
    TEXT2 = "#8B8BA7"
    ACCENT = "#7B3DFF"
    GRAD_1 = "#FF2EBD"
    GRAD_2 = "#7B3DFF"
    GRAD_3 = "#00E5FF"

    @classmethod
    def rgba(cls, hex_color, alpha=1.0):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (alpha,)

    @classmethod
    def register_fonts(cls):
        # Не регистрируем шрифты — используем системный
        return "skipped"
