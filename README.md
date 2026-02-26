# Aegis-AI: AI-Powered SSH Intrusion Detection System

Aegis is a lightweight, Human-in-the-Loop Intrusion Detection System (IDS) designed for bare-metal Linux servers. Instead of relying on static regex rules, Aegis hooks directly into your `systemd` journal, captures brute-force attack vectors, and uses an LLM to analyze the threat context in real-time.

It pushes a formatted intelligence report to your Discord server and pauses execution in a headless terminal, waiting for your explicit authorization before modifying kernel-level firewall rules.

## 🚀 Features
* **AI Threat Analysis:** Streams failed SSH auth logs to an LLM (via OpenRouter) for intelligent context parsing.
* **Discord SOC Integration:** Real-time push notifications with formatted intelligence reports.
* **Human-in-the-Loop:** Pauses execution to ensure an admin authorizes UFW firewall changes, preventing accidental lockouts.
* **Headless Patrol:** Designed to run persistently in a background `tmux` session so you can monitor your server while gaming or working.

## 📋 Prerequisites
* Ubuntu/Debian-based Linux (requires `apt`, `ufw`, and `journalctl`)
* Python 3
* OpenRouter API Key (Free tier works perfectly)
* A Discord Webhook URL (for the alarm bell)

## 🛠️ Installation & Setup

**1. Unzip the package and enter the directory:**
```bash
unzip aegis-ids.zip
cd aegis-ids
```

**2. Run the Installer:**
This will install required dependencies (`tmux`, `python3`) and prepare the environment.
```bash
chmod +x install.sh
./install.sh
```

**3. Configure your API Vault:**
Create your active config file from the provided template.
```bash
cp .env.example .env
nano .env
```
*Paste your OpenRouter API key and Discord Webhook URL inside the quotes, then save and exit.*

## 🛡️ Usage: The Virtual SOC

**1. Start the Command Center**
Launch a new `tmux` session so Aegis can run independently in the background:
```bash
tmux new -s aegis
```

**2. Arm the Watchdog**
Start the AI patrol (requires `sudo` to read system logs and execute `ufw`):
```bash
sudo python3 watchdog.py
```

**3. Detach and Walk Away**
Leave the script running invisibly:
1. Press and hold `Ctrl + B`
2. Release both keys
3. Press `D`

**4. Respond to Threats**
When your Discord alarm rings with an intelligence report, reattach to the session to approve or deny the ban:
```bash
tmux attach -t aegis
```
*Press `y` to ban the attacker, or `n` to ignore them. Then detach again to let Aegis resume its patrol.*

---
**Disclaimer:** Aegis modifies kernel-level firewall rules (`ufw`). Always review the target IP in the Discord intelligence report before authorizing a ban to ensure you do not lock yourself out of your own server.
