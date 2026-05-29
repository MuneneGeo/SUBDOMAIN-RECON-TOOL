## 📋 Overview
A Python automation script that performs subdomain enumeration on a target domain using **Subfinder**, probes discovered subdomains for live HTTP services using **Httpx**, and sends real-time Telegram notifications with results.

Built as part of the AfricaHackon Cybersecurity Program — Python Scripting module (C3A).

## ✨ Features
- CLI argument parsing (`-d` for domain, `-o` for output prefix)
- Subdomain enumeration via Subfinder
- Live host probing via Httpx
- Saves results to output files automatically
- Telegram bot notifications on scan completion
- Error handling for missing tools and failed commands

## 🛠️ Prerequisites
- Python 3.x
- Subfinder — `go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest`
- Httpx — `go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest`
- Python requests library — `pip install requests`

## 🚀 Usage
python3 notifications.py -d vulnweb.com
python3 notifications.py -d vulnweb.com -o output_results

## ⚙️ Telegram Setup
Edit the TELEGRAM_TOKEN and TELEGRAM_CHAT_ID variables in notifications.py with your own bot token and chat ID. Get a bot token from @BotFather on Telegram.

## 📄 Output
- `<domain>.txt` — all discovered subdomains\n- `<domain>_live.txt` — live/responding subdomains only\n- Telegram message confirming scan completion

## ⚠️ Disclaimer
This tool is for educational and authorised security testing only. Do not use against systems you do not have permission to test.
