![Application Screenshot](https://private-user-images.githubusercontent.com/97259120/622904736-a631a52b-1031-4c9b-a2b8-22224717d229.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3ODQyMzUyMDAsIm5iZiI6MTc4NDIzNDkwMCwicGF0aCI6Ii85NzI1OTEyMC82MjI5MDQ3MzYtYTYzMWE1MmItMTAzMS00YzliLWEyYjgtMjIyMjQ3MTdkMjI5LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA3MTYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNzE2VDIwNDgyMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWYwNjA2OTY1ZmNjY2NkNTc0YTEzNWY0MWMxNmE3OTZiYTAzY2E5NDdkZmZhYTMzYzdhMDUwMTc2NmJmMmNkYzgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.CZMXqBi2v-npiHc8NIAL_raZ9xtLwPVVFxmn7AXp6og)

# 📝 Keyboard Novelist

A gamified hardware keyboard layout test suite built natively for the GNOME 3/4 desktop ecosystem using Python 3, GTK 4, and Libadwaita. This application transforms standard hardware verification checks into an engaging 5-chapter story typing exercise that monitors real-time performance metrics and maps exact modifier combinations.

---

## ✨ Features
* **Gamified Layout Suite:** Progress through 5 uniquely randomized, character-rich text chapters.
* **Full Modifier Testing:** Intercepts and maps raw control inputs like `Ctrl`, `Alt`, `Shift`, and the `Super` layout switches.
* **Live Analytics Engine:** Dynamic asynchronous updating for live **Words Per Minute (WPM)** counts and duration clocks.
* **Hardware Resilience Escape:** Skip stuck or broken physical switches at any time using the `Escape` key.
* **Sleek Libadwaita Interface:** Modern layout structures featuring fluid resizing, drag headers, and clear color animations.

---

## 🚀 Installation & Setup

Keyboard Novelist can be installed locally on **Linux Mint 22.3** (or any modern Ubuntu/Debian derivative) using the automated installer sequence. 

### 1. Install System Dependencies
Open a terminal and make sure your local system has the required GTK 4 compilation bindings and language libraries:

```bash
sudo apt update
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 wget
```

### 2. Clone and Run the Automated Installer
Clone your project repository, step into the working tree, and launch the localized deployment script:

```bash
git clone https://github.com/chaslinux/keyboardnovelist
cd keyboardnovelist
chmod +x install.sh
./install.sh
```

The script will automatically register the codebase assets under your local user partition, safely configure internal operational rules, pull vector icon definitions, and build a native launcher profile link.

---

## 🎮 How to Play

Once the setup routine finishes, tap the **Super key** (Windows/Mint Menu key), type **Keyboard Novelist**, and select the application launcher. 

* **Typing Passages:** Begin typing the prompted story shown on the display. As you hit alphanumeric values and symbols, the on-screen physical key map highlights in blue.
* **Sentence Submission:** Pressing `Space` checks your accuracy mid-sentence. When you reach the absolute end of a sentence fragment, you **must press the Enter key** to validate the final word and load the next chapter.
* **Hardware Evaluation:** Look at the post-game summary panel to check your total key coverage percentage and verified layout analytics.

