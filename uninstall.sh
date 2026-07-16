#!/bin/bash

TARGET_DIR="$HOME/.local/share/keyboard-novelist"
DESKTOP_FILE="$HOME/.local/share/applications/keyboard-novelist.desktop"

echo "🗑️ Removing Keyboard Novelist and deployment assets..."

# Wipe out the core data folder along with the audio and icon folders
if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR"
    echo "✔ Cleaned application configuration assets and audio tracks."
fi

# Remove the system panel shortcut
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "✔ Removed desktop menu shortcut."
fi

# Re-index desktop tables
update-desktop-database "$HOME/.local/share/applications" &> /dev/null

echo "✨ Keyboard Novelist has been successfully uninstalled."

