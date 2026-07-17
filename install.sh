#!/bin/bash

# Define local user-space targets
TARGET_DIR="$HOME/.local/share/keyboard-novelist"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "📝 Installing Keyboard Novelist..."

# 1. Recreate clean directory trees
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR/novelist/ui"
mkdir -p "$TARGET_DIR/assets/audio"
mkdir -p "$TARGET_DIR/assets/icons"
mkdir -p "$DESKTOP_DIR"

# 2. Deploy your core Python source code components
cp main.py "$TARGET_DIR/"
cp novelist/layouts.py "$TARGET_DIR/novelist/"
cp novelist/ui/window.py "$TARGET_DIR/novelist/ui/"

# 3. FIXED: Fetch high-quality Open-Source audio files directly into your INSTALLED data folder
echo "🔊 Fetching audio chimes for installed suite environment..."
cp assets/audio/success.ogg "$TARGET_DIR/assets/audio"
cp assets/audio/error.ogg "$TARGET_DIR/assets/audio/"

# 4. Transfer the local custom pixel-art mechanical keyboard icon
echo "🎨 Transferring local key-deck artwork..."
cp assets/icons/keyboard-novelist.png "$TARGET_DIR/assets/icons/"

# 5. Compile and target the configuration configuration string templates
sed "s|TARGET_DIR|$TARGET_DIR|g" keyboard-novelist.desktop.template > "$DESKTOP_DIR/keyboard-novelist.desktop"
chmod +x "$DESKTOP_DIR/keyboard-novelist.desktop"

# 6. Flush systemic desktop index caches
update-desktop-database "$DESKTOP_DIR" &> /dev/null

echo "✨ Installed application environment fully populated with assets! Re-indexing menu..."

