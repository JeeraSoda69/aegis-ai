import subprocess
import re
import time
import urllib.request
import json
import os

banned_ips = set()

def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, val = line.split('=', 1)
                    env_vars[key.strip()] = val.strip().strip('"\'')
    except FileNotFoundError:
        print("[!] FATAL: .env file not found.")
        exit(1)
    return env_vars

# --- THE NEW PLUG-AND-PLAY CONFIG ---
ENV = load_env()
API_KEY = ENV.get('OPENROUTER_API_KEY', '')
DISCORD_WEBHOOK = ENV.get('DISCORD_WEBHOOK', '')

if not API_KEY or not DISCORD_WEBHOOK:
    print("[!] FATAL: Missing API keys or Webhook in .env file. Please configure them.")
    exit(1)
# ------------------------------------

def ask_aegis(log_line):
    print("[*] Connecting to OpenRouter API (Auto-Free Routing)...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"You are Aegis, a strict cybersecurity AI. Analyze this raw server log: '{log_line}'. In exactly two sentences, tell the Admin what is happening and recommend if the IP should be banned. Start your response with 'THREAT:' or 'SAFE:'."
    
    data = {
        "model": "openrouter/free", 
        "messages": [{"role": "user", "content": prompt}]
    }
    
    req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode('utf-8'))
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"API ERROR: {e}"

def send_discord_alert(ip, report):
    print("[*] Ringing the Discord alarm...")
    data = {
        "content": f"🚨 **AEGIS ALERT: SSH ATTACK DETECTED** 🚨\n**Target IP:** `{ip}`\n\n**AI Intelligence Report:**\n> {report}\n\n*Log into the Kali tmux SOC to approve or deny the ban.*"
    }
    req = urllib.request.Request(DISCORD_WEBHOOK, data=json.dumps(data).encode('utf-8'), headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"[!] Discord Webhook Failed: {e}")

def tail_and_analyze():
    print("[*] Aegis-AI IDS online. Monitoring systemd journal for anomalies...")
    process = subprocess.Popen(['journalctl', '-u', 'ssh', '-f', '-n', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        while True:
            line = process.stdout.readline().decode('utf-8')
            if not line:
                time.sleep(0.1)
                continue
            
            if "Failed password" in line or "Connection closed" in line:
                match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    attacker_ip = match.group(1)
                    
                    if attacker_ip in banned_ips:
                        continue 
                        
                    print(f"\n[!] ANOMALY DETECTED from IP: {attacker_ip}")
                    
                    ai_report = ask_aegis(line)
                    
                    print("\n" + "="*50)
                    print(" AEGIS INTELLIGENCE REPORT")
                    print("="*50)
                    print(f"{ai_report}")
                    print("="*50 + "\n")
                    
                    send_discord_alert(attacker_ip, ai_report)
                    
                    action = input(f"[?] Execute UFW firewall ban on {attacker_ip}? (y/n): ")
                    
                    if action.lower() == 'y':
                        print(f"[*] Executing: sudo ufw deny from {attacker_ip}")
                        subprocess.run(['sudo', 'ufw', 'deny', 'from', attacker_ip])
                        banned_ips.add(attacker_ip)
                        print(f"[+] Target {attacker_ip} neutralized. Resuming patrol...\n")
                    else:
                        print("[-] Ban aborted by Admin. Resuming patrol...\n")
                        
    except KeyboardInterrupt:
        print("\n[*] Shutting down Aegis-AI.")
        process.terminate()

if __name__ == "__main__":
    subprocess.run(['sudo', 'ufw', 'delete', 'deny', 'from', '127.0.0.1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tail_and_analyze()
