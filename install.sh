#!/bin/bash

# Define system target installation directories
TARGET_DIR="$HOME/.local/share/keyboard-novelist"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"

echo "📝 Installing Keyboard Novelist..."

# 1. Clean up any older versions and recreate core application folders
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR/novelist/ui"
mkdir -p "$TARGET_DIR/assets/audio"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# 2. Copy the Python codebase into the user's local share folder
cp main.py "$TARGET_DIR/"
cp novelist/layouts.py "$TARGET_DIR/novelist/"
cp novelist/ui/window.py "$TARGET_DIR/novelist/ui/"

# 3. Pull high-quality Open Source assets directly if missing locally
echo "🔊 Fetching audio chimes..."
wget -q -O "$TARGET_DIR/assets/audio/success.ogg" "https://google.com"
wget -q -O "$TARGET_DIR/assets/audio/error.ogg" "https://google.com"

echo "🎨 Fetching application vector branding icon..."
wget -q -O "$ICON_DIR/keyboard-novelist.svg" "https://githubusercontent.com"

# 4. Generate the personalized Desktop launcher from the template
sed "s|TARGET_DIR|$TARGET_DIR|g" keyboard-novelist.desktop.template > "$DESKTOP_DIR/keyboard-novelist.desktop"

# 5. Set appropriate execution safety permissions
chmod +x "$DESKTOP_DIR/keyboard-novelist.desktop"

# 6. Rebuild Linux Mint desktop configuration cache tables
update-desktop-database "$DESKTOP_DIR" &> /dev/null
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" &> /dev/null

echo "✨ Installation complete! You can now launch Keyboard Novelist from your Mint Applications Menu."

