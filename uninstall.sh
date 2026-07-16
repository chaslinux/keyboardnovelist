#!/bin/bash

# Target local deployment paths
TARGET_DIR="$HOME/.local/share/keyboard-novelist"
DESKTOP_FILE="$HOME/.local/share/applications/keyboard-novelist.desktop"

echo "🗑️ Removing Keyboard Novelist..."

# 1. Cleanly wipe out application core folder directories
if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR"
    echo "✔ Cleaned application configuration assets."
fi

# 2. Extract the desktop start menu shortcut link
if [ -f "$DESKTOP_FILE" ]; then
    rm "$DESKTOP_FILE"
    echo "✔ Removed desktop menu shortcut."
fi

# 3. Force re-index global Mint environment directory indexes
update-desktop-database "$HOME/.local/share/applications" &> /dev/null

echo "✨ Keyboard Novelist has been successfully uninstalled."

