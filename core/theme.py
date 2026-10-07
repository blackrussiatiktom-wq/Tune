"""Темы приложения: чёрная и белая."""

class Theme:
    DARK = {
        "bg":        "#000000",
        "card":      "#0A0A12",
        "text":      "#FFFFFF",
        "text2":     "#8B8BA7",
        "divider":   "#1A1A24",
        "icon":      "#FFFFFF",
        "grad":      ("#FF2EBD", "#7B3DFF", "#00E5FF"),
    }
    LIGHT = {
        "bg":        "#FFFFFF",
        "card":      "#F2F2F7",
        "text":      "#0A0A12",
        "text2":     "#6B6B80",
        "divider":   "#E0E0E8",
        "icon":      "#0A0A12",
        "grad":      ("#FF2EBD", "#7B3DFF", "#00E5FF"),
    }

    def __init__(self, mode="dark"):
        self.mode = mode

    @property
    def c(self):
        return self.DARK if self.mode == "dark" else self.LIGHT

    def toggle(self):
        self.mode = "light" if self.mode == "dark" else "dark"
        return self.mode

    def hex_to_rgba(self, hex_color):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)) + (1.0,)
