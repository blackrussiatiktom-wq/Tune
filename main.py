from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window


class TuneApp(App):
    def build(self):
        self.title = "Tune"
        Window.clearcolor = (0, 0, 0, 1)
        layout = BoxLayout(orientation='vertical', padding=50)
        label = Label(
            text='[b]Tune[/b]\n\nHello!',
            markup=True,
            font_size='40sp',
            color=(1, 1, 1, 1),
            halign='center',
        )
        layout.add_widget(label)
        return layout


if __name__ == '__main__':
    TuneApp().run()
