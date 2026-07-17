# ~/Projects/KeyboardNovelist/novelist/ui/window.py
# CHUNK 1 OF 4: IMPORTS, CORE INITIALIZATION, AND HEADER DESIGN

import gi
import random
import time
import os
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib, Gio

from novelist.layouts import ANSI_LAYOUT, POOL_OF_STORIES

class NovelistWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Keyboard Novelist")
        self.set_default_size(950, 600)
        
        # FIXED: Automatically calculates the real project root directory location dynamically
        ui_dir = os.path.dirname(os.path.abspath(__file__))
        novelist_dir = os.path.dirname(ui_dir)
        self.base_dir = os.path.dirname(novelist_dir)
        
        # LOOKUP METRIC: Flattens the ANSI matrix layout into a single reference tracking set
        self.all_expected_keys = set(key.upper() for row in ANSI_LAYOUT for key in row)
        
        self.story_playlist = random.sample(POOL_OF_STORIES, 5)
        self.current_chapter_index = 0
        self.current_story = self.story_playlist[self.current_chapter_index]
        
        self.typed_buffer = ""
        self.key_buttons = {}
        self.pressed_keys_history = set()
        
        self.start_time = None
        self.timer_active = False
        
        self.build_ui()
        self.setup_keyboard()

    def build_ui(self):
        self.window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window_box.append(Adw.HeaderBar())

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self.main_box.set_margin_top(20)
        self.main_box.set_margin_bottom(30)
        self.main_box.set_margin_start(30)
        self.main_box.set_margin_end(30)

        header_grid = Gtk.Grid()
        header_grid.set_column_spacing(20)
        
        title_label = Gtk.Label(label="📝 Keyboard Novelist")
        title_label.add_css_class("title-1")
        header_grid.attach(title_label, 0, 0, 1, 1)

        self.wpm_label = Gtk.Label(label="📖 Chapter 1/5  |  ⚡ WPM: 0  |  ⏱️ Time: 0s")
        self.wpm_label.add_css_class("heading")
        self.wpm_label.set_halign(Gtk.Align.END)
        self.wpm_label.set_hexpand(True)
        header_grid.attach(self.wpm_label, 1, 0, 1, 1)
        self.main_box.append(header_grid)

        self.story_label = Gtk.Label(label=self.current_story)
        self.story_label.set_wrap(True)
        self.story_label.add_css_class("title-2")
        self.main_box.append(self.story_label)

        # MONOSPACE INITIALIZATION: Protects characters from visual compression
        self.input_label = Gtk.Label()
        self.input_label.set_use_markup(True) 
        self.input_label.set_markup("<span font_family='monospace' size='large'>Start typing or press [ESC] to skip chapter...</span>")
        self.input_label.add_css_class("body")
        self.main_box.append(self.input_label)


# CHUNK 2 OF 4: CLEANED KEYBOARD ENGINE VIEW SETUP & INITIALIZATION

        keyboard_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        keyboard_box.set_halign(Gtk.Align.CENTER)
        
        for row in ANSI_LAYOUT:
            row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            row_box.set_halign(Gtk.Align.CENTER)
            for key in row:
                # FIX: Add [0] index to grab the clean string text and prevent a list crash
                display_label = key.split('_')[0]
                btn = Gtk.Button(label=display_label)
                btn.set_focusable(False)
                
                if any(x in key for x in ["BackSpace", "Tab", "CapsLock", "Enter", "Shift", "Control", "Alt", "Super"]):
                    btn.set_size_request(90, 45)
                elif key == "Space":
                    btn.set_size_request(300, 45)
                else:
                    btn.set_size_request(45, 45)

                row_box.append(btn)
                self.key_buttons[key.upper()] = btn
            keyboard_box.append(row_box)
            
        self.main_box.append(keyboard_box)
        self.window_box.append(self.main_box)
        self.set_content(self.window_box)

    def setup_keyboard(self):
        event_controller = Gtk.EventControllerKey.new()
        event_controller.connect("key-pressed", self.on_key_press)
        event_controller.connect("key-released", self.on_key_release)
        self.add_controller(event_controller)

    def update_metrics(self):
        if not self.timer_active:
            return False
        elapsed_time = time.time() - self.start_time
        if elapsed_time <= 0:
            return True

        char_count = len(self.typed_buffer)
        word_entries = char_count / 5.0 
        wpm = round((word_entries / elapsed_time) * 60)
        self.wpm_label.set_label(f"📖 Chapter {self.current_chapter_index + 1}/5  |  ⚡ WPM: {wpm}  |  ⏱️ Time: {int(elapsed_time)}s")
        return True

# CHUNK 3 OF 4: KEY COMPRESSION ENGINE, CHAR MAPPINGS, COLOR HOOKS

    def on_key_press(self, controller, keyval, keycode, state):
        key_name = Gdk.keyval_name(keyval)
        if not key_name:
            return False

        if key_name == "Escape":
            self.advance_game(skipped=True)
            return True

        if not self.timer_active:
            self.start_time = time.time()
            self.timer_active = True
            GLib.timeout_add(200, self.update_metrics)

        normal_key = key_name.upper()
        alias_map = {
            "SEMICOLON": ";", "COMMA": ",", "PERIOD": ".", "MINUS": "-", "EQUAL": "=", 
            "SLASH": "/", "BACKSLASH": "\\", "APOSTROPHE": "'", "BRACKETLEFT": "[", "BRACKETRIGHT": "]"
        }
        if normal_key in alias_map:
            normal_key = alias_map[normal_key]

        target_key = normal_key
        if "SHIFT" in normal_key: target_key = "SHIFT_L" if "L" in normal_key or keycode == 50 else "SHIFT_R"
        if "CONTROL" in normal_key or "CTRL" in normal_key: target_key = "CONTROL_L" if "L" in normal_key or keycode == 37 else "CONTROL_R"
        if "ALT" in normal_key: target_key = "ALT_L" if "L" in normal_key or keycode == 64 else "ALT_R"
        if "SUPER" in normal_key: target_key = "SUPER_L"

        if target_key in self.key_buttons:
            self.key_buttons[target_key].add_css_class("suggested-action")
            self.pressed_keys_history.add(target_key)
            self.key_buttons[target_key].add_css_class("tested-key")

        unicode_char = chr(Gdk.keyval_to_unicode(keyval)) if Gdk.keyval_to_unicode(keyval) != 0 else ""

        if key_name == "space":
            self.check_word_accuracy(is_enter=False)
            self.typed_buffer += " "
        elif key_name in ["Return", "KP_Enter"]:
            self.check_word_accuracy(is_enter=True)
            return True
        elif key_name == "BackSpace":
            self.typed_buffer = self.typed_buffer[:-1]
        elif unicode_char and len(unicode_char) == 1:
            if not (state & (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.ALT_MASK)):
                self.typed_buffer += unicode_char

        # ESCAPE FIX: Automatically encodes raw strings (like & or <) into safe Pango markup tokens
        safe_buffer = GLib.markup_escape_text(self.typed_buffer)

        self.input_label.set_markup(f"<span font_family='monospace' size='large'>Your Novel: {safe_buffer}</span>")
        return True

    def on_key_release(self, controller, keyval, keycode, state):
        key_name = Gdk.keyval_name(keyval)
        if key_name:
            normal_key = key_name.upper()
            alias_map = {
                "SEMICOLON": ";", "COMMA": ",", "PERIOD": ".", "MINUS": "-", "EQUAL": "=", 
                "SLASH": "/", "BACKSLASH": "\\", "APOSTROPHE": "'", "BRACKETLEFT": "[", "BRACKETRIGHT": "]"
            }
            if normal_key in alias_map:
                normal_key = alias_map[normal_key]
                
            target_key = normal_key
            if "SHIFT" in normal_key: target_key = "SHIFT_L" if "L" in normal_key or keycode == 50 else "SHIFT_R"
            if "CONTROL" in normal_key or "CTRL" in normal_key: target_key = "CONTROL_L" if "L" in normal_key or keycode == 37 else "CONTROL_R"
            if "ALT" in normal_key: target_key = "ALT_L" if "L" in normal_key or keycode == 64 else "ALT_R"
            if "SUPER" in normal_key: target_key = "SUPER_L"

            if target_key in self.key_buttons:
                self.key_buttons[target_key].remove_css_class("suggested-action")
        return True

# CHUNK 4 OF 4: PROOFED VALIDATION, REPORT CARD SCREEN, INTERNAL ENGINE AUDIO + LOGGER

    def check_word_accuracy(self, is_enter=False):
        story_words = self.current_story.split()
        typed_words = self.typed_buffer.strip().split()
        
        if not typed_words:
            return
        
        current_word_idx = len(typed_words) - 1
        
        if not is_enter:
            if current_word_idx < len(story_words):
                if typed_words[-1] == story_words[current_word_idx]:
                    self.play_sound("success")
                else:
                    self.play_sound("error")
        else:
            if len(typed_words) >= len(story_words):
                if typed_words[-1] == story_words[-1]:
                    self.play_sound("success")
                    self.advance_game(skipped=False)
                else:
                    self.play_sound("error")
            else:
                self.play_sound("error")

    def advance_game(self, skipped=False):
        self.timer_active = False
        self.typed_buffer = ""
        self.current_chapter_index += 1
        
        if self.current_chapter_index < 5:
            self.current_story = self.story_playlist[self.current_chapter_index]
            self.story_label.set_label(self.current_story)
            status_text = "Chapter skipped. Advancing..." if skipped else "Chapter finished! Loading next scene..."
            self.input_label.set_markup(f"<span font_family='monospace' size='large'>{status_text}</span>")
            self.wpm_label.set_label(f"📖 Chapter {self.current_chapter_index + 1}/5  |  ⚡ WPM: 0  |  ⏱️ Time: 0s")
        else:
            self.show_results_screen()

    def show_results_screen(self):
        self.window_box.remove(self.main_box)
        
        results_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        results_container.set_margin_top(40)
        results_container.set_margin_bottom(40)
        results_container.set_margin_start(40)
        results_container.set_margin_end(40)
        results_container.set_halign(Gtk.Align.CENTER)
        
        victory_title = Gtk.Label(label="🏆 The Novel is Complete!")
        victory_title.add_css_class("title-1")
        results_container.append(victory_title)
        
        total_hardware_keys = len(self.all_expected_keys)
        keys_hit_count = len(self.pressed_keys_history)
        coverage_percent = round((keys_hit_count / total_hardware_keys) * 100)
        
        untouched_keys_set = self.all_expected_keys - self.pressed_keys_history
#        clean_untouched_list = [k.split('_') for k in sorted(list(untouched_keys_set))]
        clean_untouched_list = [k.split('_')[0] for k in sorted(untouched_keys_set)]
        
        if clean_untouched_list:
            untouched_display_text = ", ".join(clean_untouched_list)
        else:
            untouched_display_text = "None! Flawless 100% hardware matrix activation!"

        summary_label = Gtk.Label(label=f"You successfully completed your 5-chapter story exploration!\n\n"
                                        f"🎹 Hardware Keys Tested: {keys_hit_count} / {total_hardware_keys} ({coverage_percent}% coverage)")
        summary_label.add_css_class("title-3")
        summary_label.set_justify(Gtk.Justification.CENTER)
        results_container.append(summary_label)
        
        missed_title = Gtk.Label(label="⚠️ Untouched Keys Remaining:")
        missed_title.add_css_class("heading")
        results_container.append(missed_title)
        
        missed_detail = Gtk.Label(label=untouched_display_text)
        missed_detail.add_css_class("body")
        missed_detail.set_wrap(True)
        missed_detail.set_justify(Gtk.Justification.CENTER)
        results_container.append(missed_detail)
        
        exit_btn = Gtk.Button(label="Close Application")
        exit_btn.add_css_class("destructive-action")
        exit_btn.set_size_request(200, 50)
        exit_btn.set_halign(Gtk.Align.CENTER)
        exit_btn.connect("clicked", lambda b: self.close())
        results_container.append(exit_btn)
        
        self.window_box.append(results_container)

    def play_sound(self, sound_type):
        """Uses native GNOME GStreamer loops and writes errors to an external log file."""
        log_file = os.path.join(self.base_dir, "audio_debug.log")
        file_path = os.path.join(self.base_dir, f"assets/audio/{sound_type}.ogg")
        
        try:
            # Dynamically initialize GStreamer internally
            import gi
            gi.require_version('Gst', '1.0')
            from gi.repository import Gst
            Gst.init(None)
            
            # Construct a clean native playbin pipeline
            pipeline = Gst.parse_launch(f"playbin uri=file://{os.path.abspath(file_path)}")
            if pipeline:
                pipeline.set_state(Gst.State.PLAYING)
                # Garbage collector to free audio memory after 1.5 seconds
                GLib.timeout_add(1500, lambda: [pipeline.set_state(Gst.State.NULL), False])
                
        except Exception as e:
            # Write any internal environment or permission errors directly to a log file
            with open(log_file, "a") as f:
                f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Audio error: {str(e)} | Checked path: {file_path}\n")
            print("\a", end="", flush=True)

