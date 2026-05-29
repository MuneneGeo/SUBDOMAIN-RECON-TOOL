#!/usr/bin/env python3
"""
Placed all the imports at the top
"""

import argparse
import subprocess
import sys
import os
import shutil
import requests

def run_command(command, output_file):
    """
    Runs a shell command and saves output to a file.
    Error handling was done here
    """
    try:
        print(f"[+] Running command: {' '.join(command)}")
        with open(output_file, "w") as f:
            subprocess.run(
                command,
                stdout=f,
                stderr=subprocess.DEVNULL,
                check=True
            )
        print(f"[✓] Results saved to {output_file}\n")
    except subprocess.CalledProcessError:
        print(f"[!] Error occurred while running command: {' '.join(command)}")
        sys.exit(1)

def send_telegram_message(token, chat_id, message):
    """
    Sends a notification message to Telegram
    """
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        requests.post(url, data=payload, timeout=5)
    except requests.RequestException:
        print("[!] Telegram notification failed")

def main():
    # CLI argument parsing
    parser = argparse.ArgumentParser(
        description="Subdomain Enumeration & Live Host Probing Script"
    )
    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Target domain (e.g vulnweb.com)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file prefix (default = domain name)"
    )

    args = parser.parse_args()

    domain = args.domain
    output_prefix = args.output if args.output else domain

    subdomains_file = f"{output_prefix}.txt"
    live_subdomains_file = f"{output_prefix}_live.txt"

    # Telegram Configuration
    TELEGRAM_TOKEN = ""
    TELEGRAM_CHAT_ID = ""
    

    print("=" * 50)
    print("[*] Python Automation Script Started")
    print(f"[*] Target Domain: {domain}")
    print("=" * 50)

    # Check if required tools exist
    for tool in ["subfinder", "httpx"]:
        if not shutil.which(tool):
            print(f"[!] {tool} is not installed or not in PATH.")
            sys.exit(1)

    # Subdomain Enumeration
    print("[*] Enumerating subdomains...")
    subfinder_cmd = ["subfinder", "-d", domain, "-silent"]
    run_command(subfinder_cmd, subdomains_file)

    # Check live subdomains
    print("[*] Probing live subdomains...")
    httpx_cmd = ["httpx", "-silent", "-l", subdomains_file]
    run_command(httpx_cmd, live_subdomains_file)

    # Conditional check
    if os.path.getsize(live_subdomains_file) > 0:
        print("[✓] Live hosts found and saved successfully.")
        send_telegram_message(
            TELEGRAM_TOKEN,
            TELEGRAM_CHAT_ID,
            f"[+] Live subdomains found for {domain}"
        )
    else:
        print("[!] No live subdomains found.")
        send_telegram_message(
            TELEGRAM_TOKEN,
            TELEGRAM_CHAT_ID,
            f"[-] Scan completed for {domain}. No live hosts found."
        )

    print("\n[✓] Script execution completed successfully.")

if __name__ == "__main__":
    main()
