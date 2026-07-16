# ~/Projects/KeyboardNovelist/main.py

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw

from novelist.ui.window import NovelistWindow

class KeyboardNovelistApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        window = NovelistWindow(app)
        window.present()

if __name__ == "__main__":
    app = KeyboardNovelistApp(application_id="com.novelist.KeyboardTester")
    app.run(None)
