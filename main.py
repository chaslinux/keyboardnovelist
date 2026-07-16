import gi
import random
import time
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib, Gio

ANSI_LAYOUT = [
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BackSpace"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
    ["Ctrl", "Super", "Alt", "Space", "Alt", "Ctrl"]
]

STORIES = [
    "The quick brown fox jumps over 12 lazy dogs at midnight!",
    "Error 404: The computer ate my homework & drank 3 coffees.",
    "Launch sequence initiated: 5... 4... 3... 2... 1... Lift off #Gnome!",
    "She sells 99 sea-shells by the sea-shore; it was quite a sight.",
    "Type faster! The matrix requires at least 7.5 gigawatts of power."
]

class KeyboardNovelistApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

        self.current_story = random.choice(STORIES)
        self.typed_buffer = ""
        self.key_buttons = {}

        self.start_time = None
        self.timer_active = False

    def on_activate(self, app):
        self.window = Adw.ApplicationWindow(application=app)
        self.window.set_title("Keyboard Novelist")
        self.window.set_default_size(950, 600)

        # Base layout box
        window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # FIX #2: Explicitly adding a standard Adw HeaderBar gives the mouse its grab-anchor for dragging
        header_bar = Adw.HeaderBar()
        window_box.append(header_bar)

        # Game UI Workspace Panel
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(30)
        main_box.set_margin_start(30)
        main_box.set_margin_end(30)

        header_grid = Gtk.Grid()
        header_grid.set_column_spacing(20)

        title_label = Gtk.Label(label="📝 Keyboard Novelist")
        title_label.add_css_class("title-1")
        header_grid.attach(title_label, 0, 0, 1, 1)

        self.wpm_label = Gtk.Label(label="⚡ WPM: 0  |  ⏱️ Time: 0s")
        self.wpm_label.add_css_class("heading")
        self.wpm_label.set_halign(Gtk.Align.END)
        self.wpm_label.set_hexpand(True)
        header_grid.attach(self.wpm_label, 1, 0, 1, 1)

        main_box.append(header_grid)

        self.story_label = Gtk.Label(label=self.current_story)
        self.story_label.set_wrap(True)
        self.story_label.add_css_class("title-2")
        main_box.append(self.story_label)

        self.input_label = Gtk.Label(label="Start typing or press [ESC] to skip chapter...")
        self.input_label.add_css_class("body")
        main_box.append(self.input_label)

        keyboard_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        keyboard_box.set_halign(Gtk.Align.CENTER)

        for row in ANSI_LAYOUT:
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            row_box.set_halign(Gtk.Align.CENTER)
            for key in row:
                btn = Gtk.Button(label=key)
                btn.set_focusable(False)

                if key in ["BackSpace", "Tab", "CapsLock", "Enter", "Shift"]:
                    btn.set_size_request(90, 45)
                elif key == "Space":
                    btn.set_size_request(300, 45)
                else:
                    btn.set_size_request(45, 45)

                row_box.append(btn)
                self.key_buttons[key.upper()] = btn
            keyboard_box.append(row_box)

        main_box.append(keyboard_box)
        window_box.append(main_box)

        # Register hardware event systems
        event_controller = Gtk.EventControllerKey.new()
        event_controller.connect("key-pressed", self.on_key_press)
        event_controller.connect("key-released", self.on_key_release)
        self.window.add_controller(event_controller)

        self.window.set_content(window_box)
        self.window.present()

    def update_metrics(self):
        if not self.timer_active:
            return False

        elapsed_time = time.time() - self.start_time
        if elapsed_time <= 0:
            return True

        char_count = len(self.typed_buffer)
        word_entries = char_count / 5.0
        wpm = round((word_entries / elapsed_time) * 60)

        self.wpm_label.set_label(f"⚡ WPM: {wpm}  |  ⏱️ Time: {int(elapsed_time)}s")
        return True

    def on_key_press(self, controller, keyval, keycode, state):
        key_name = Gdk.keyval_name(keyval)
        if not key_name:
            return False

        if key_name == "Escape":
            self.skip_chapter()
            return True

        if not self.timer_active:
            self.start_time = time.time()
            self.timer_active = True
            GLib.timeout_add(200, self.update_metrics)

        normal_key = key_name.upper()

        # UI Key highlighting adjustments for symbol strings
        alias_map = {"SEMICOLON": ";", "COMMA": ",", "PERIOD": ".", "MINUS": "-", "EQUAL": "=", "SLASH": "/", "BACKSLASH": "\\", "APOSTROPHE": "'", "BRACKETLEFT": "[", "BRACKETRIGHT": "]"}
        if normal_key in alias_map:
            normal_key = alias_map[normal_key]

        if normal_key in self.key_buttons:
            self.key_buttons[normal_key].add_css_class("suggested-action")

        # FIX #1: Use unicode transformation maps to parse standard character symbols safely
        unicode_char = chr(Gdk.keyval_to_unicode(keyval)) if Gdk.keyval_to_unicode(keyval) != 0 else ""

        if key_name == "space":
            self.check_word_accuracy()
            self.typed_buffer += " "
        elif key_name == "BackSpace":
            self.typed_buffer = self.typed_buffer[:-1]
        elif unicode_char and len(unicode_char) == 1:
            self.typed_buffer += unicode_char

        self.input_label.set_label(f"Your Novel: {self.typed_buffer}")
        return True

    def on_key_release(self, controller, keyval, keycode, state):
        key_name = Gdk.keyval_name(keyval)
        if key_name:
            normal_key = key_name.upper()
            alias_map = {"SEMICOLON": ";", "COMMA": ",", "PERIOD": ".", "MINUS": "-", "EQUAL": "=", "SLASH": "/", "BACKSLASH": "\\", "APOSTROPHE": "'", "BRACKETLEFT": "[", "BRACKETRIGHT": "]"}
            if normal_key in alias_map:
                normal_key = alias_map[normal_key]

            if normal_key in self.key_buttons:
                self.key_buttons[normal_key].remove_css_class("suggested-action")
        return True

    def skip_chapter(self):
        self.timer_active = False
        self.typed_buffer = ""
        self.current_story = random.choice(STORIES)
        self.story_label.set_label(self.current_story)
        self.input_label.set_label("Chapter skipped via [ESC]. Starting new fragment...")
        self.wpm_label.set_label("⚡ WPM: 0  |  ⏱️ Time: 0s")

    def check_word_accuracy(self):
        story_words = self.current_story.split()
        typed_words = self.typed_buffer.split()

        current_word_idx = len(typed_words) - 1
        if current_word_idx < len(story_words):
            if typed_words[-1] == story_words[current_word_idx]:
                self.play_sound("success")
            else:
                self.play_sound("error")

        if len(typed_words) >= len(story_words):
            self.timer_active = False
            self.input_label.set_label("✨ Finished successfully! Starting next chapter...")
            self.typed_buffer = ""
            self.current_story = random.choice(STORIES)
            self.story_label.set_label(self.current_story)

    def play_sound(self, sound_type):
        file_path = f"assets/audio/{sound_type}.ogg"
        if os.path.exists(file_path):
            os.system(f"paplay {file_path} &")
        else:
            Gio.app_info_launch_default_for_uri("bell://", None)

if __name__ == "__main__":
    app = KeyboardNovelistApp(application_id="com.novelist.KeyboardTester")
    app.run(None)

