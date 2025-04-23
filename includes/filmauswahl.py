from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Box, Frame, Label
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.layout.containers import Window


def zeige_filmauswahl(filme):
    index = [0]
    def get_text():
        return [( 
                'class:selected' if i == index[0] else '', 
                f"{film['title']} ({film.get('release_date', '??')[:4]})\n"
            ) for i, film in enumerate(filme)]

    def up(event: KeyPressEvent):
        index[0] = (index[0] - 1) % len(filme)

    def down(event: KeyPressEvent):
        index[0] = (index[0] + 1) % len(filme)

    def enter(event: KeyPressEvent):
        app.exit(result=filme[index[0]])

    kb = KeyBindings()
    kb.add("up")(up)
    kb.add("down")(down)
    kb.add("enter")(enter)

    root_container = Box(
        body=Frame(
            HSplit([
                Label(text="Mit ↑ ↓ navigieren, Enter zur Auswahl"),
                Window(content=FormattedTextControl(get_text), always_hide_cursor=True)
            ])
        )
    )

    app = Application(layout=Layout(root_container), key_bindings=kb, full_screen=True)
    return app.run()