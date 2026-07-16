#!/bin/bash

sudo apt update
sudo apt -y install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 wget

TARGET_DIR="$HOME/.local/share/keyboard-novelist"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "📝 Installing Keyboard Novelist..."

# 1. Clean and rebuild local storage paths
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR/novelist/ui"
mkdir -p "$TARGET_DIR/assets/audio"
mkdir -p "$TARGET_DIR/assets/icons"
mkdir -p "$DESKTOP_DIR"

# 2. Deploy your application code files
cp main.py "$TARGET_DIR/"
cp novelist/layouts.py "$TARGET_DIR/novelist/"
cp novelist/ui/window.py "$TARGET_DIR/novelist/ui/"

# 3. Pull default open-source audio chimes
echo "🔊 Fetching audio chimes..."
wget -q -O "$TARGET_DIR/assets/audio/success.ogg" "https://google.com"
wget -q -O "$TARGET_DIR/assets/audio/error.ogg" "https://google.com"

# 4. Copy your local pixel-art keyboard graphic to the app asset directory
echo "🎨 Transferring local key-deck artwork..."
cp assets/icons/keyboard-novelist.png "$TARGET_DIR/assets/icons/"

# 5. Compile and target the configuration launcher strings
sed "s|TARGET_DIR|$TARGET_DIR|g" keyboard-novelist.desktop.template > "$DESKTOP_DIR/keyboard-novelist.desktop"
chmod +x "$DESKTOP_DIR/keyboard-novelist.desktop"

# 6. Flush global desktop metadata tables
update-desktop-database "$DESKTOP_DIR" &> /dev/null

echo "✨ Re-installation complete!"

