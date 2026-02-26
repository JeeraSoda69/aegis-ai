#!/bin/bash

echo "========================================"
echo "    AEGIS-AI IDS INSTALLATION SCRIPT    "
echo "========================================"

echo "[*] Updating system packages..."
sudo apt update -y > /dev/null 2>&1

echo "[*] Installing required dependencies (tmux, python3)..."
sudo apt install tmux python3 -y > /dev/null 2>&1

echo "[*] Checking configuration..."
if [ ! -f .env ]; then
    echo "[!] No .env file found!"
    echo "    Please rename .env.example to .env and add your API keys."
    exit 1
fi

echo "[+] Installation complete."
echo "[+] To start the AI Bouncer in the background, run:"
echo "    tmux new -s aegis 'sudo python3 watchdog.py'"
echo "========================================"
