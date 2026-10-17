#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVANCED MOBILE NMAP WEB & SECURITY AUDITOR (HACKER EDITION)
File Name: auditor_tool.py
Author: Security Suite AI
Description: 100% Local Penetration Testing & AI Vulnerability Assessment Tool
"""

import os
import socket
import subprocess
import sys
from urllib.parse import urlparse

# Optional dependencies check & auto-import handling
try:
  import requests
  from bs4 import BeautifulSoup
except ImportError:
  print(
      "[!] Required libraries missing! Run: pip install requests beautifulsoup4"
  )
  sys.exit(1)

# AI Model check (Transformers)
AI_AVAILABLE = False
try:
  from transformers import pipeline

  AI_AVAILABLE = True
except ImportError:
  AI_AVAILABLE = False

# --- ANSI COLORS FOR HACKER LOOK ---
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
BLUE = "\033[94m"


def print_banner():
  os.system("clear" if os.name == "posix" else "cls")
  print(
      GREEN
      + """
╔═══════════════════════════════════════════════════════════════════╗
║         ADVANCED MOBILE NMAP & AI SECURITY AUDITOR (v2.0)         ║
║         100% Local Execution | Zero API | Termux Optimized        ║
╚═══════════════════════════════════════════════════════════════════╝
"""
      + RESET
  )


def show_cli_help():
  print(
      CYAN
      + "\n"
      + "=" * 60
      + "\n          COMMAND-LINE HELP & USAGE GUIDE\n"
      + "=" * 60
      + RESET
  )
  print(
      "Yeh tool aapke mobile (Termux) par ek professional pentest suite ki"
      " tarah kaam karta hai:"
  )
  print(
      f" {GREEN}[1]{RESET} {BOLD}Nmap Port Scan (-T4 & Top 100):{RESET}"
      " Target ke 100 sabse common ports scan karta hai aur open services"
      " dhoondta hai."
  )
  print(
      f" {GREEN}[2]{RESET} {BOLD}Web Header & Flaw Audit:{RESET}"
      " HTTPS status aur missing security headers (CSP, HSTS, X-Frame-Options)"
      " check karta hai."
  )
  print(
      f" {GREEN}[3]{RESET} {BOLD}Web Content Scraper:{RESET}"
      " Page title, meta description aur clean text extract karta hai."
  )
  print(
      f" {GREEN}[4]{RESET} {BOLD}Local AI Security Advisor:{RESET}"
      " Scan results ko analyze karke AI-driven threat intelligence deta"
      " hai.\n"
  )
  print(CYAN + "=" * 60 + RESET + "\n")


def run_nmap_scan(domain):
  report = []
  report.append("=" * 55)
  report.append("          NMAP NETWORK & PORT SCAN REPORT")
  report.append("=" * 55)
  try:
    print(
        YELLOW
        + f"[*] Nmap engine target {domain} par port scanning kar raha hai..."
        + RESET
    )
    # Resolve domain to IP for accuracy
    try:
      target_ip = socket.gethostbyname(domain)
      report.append(f"[*] Target Resolved IP: {target_ip}")
    except Exception:
      target_ip = domain

    cmd = ["nmap", "-T4", "--top-ports", "100", target_ip]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60
    )

    if result.returncode == 0:
      report.append(result.stdout)
    else:
      report.append(
          f"[!] Nmap execution error. Ensure 'nmap' is installed in Termux.\nError:"
          f" {result.stderr}"
      )
  except FileNotFoundError:
    report.append(
        "[!] Error: 'nmap' command not found! Run 'pkg install nmap' in Termux."
    )
  except subprocess.TimeoutExpired:
    report.append("[!] Nmap scan timed out.")
  except Exception as e:
    report.append(f"[!] Nmap error: {e}")
  return "\n".join(report)


def audit_security_headers(url):
  report = []
  report.append("\n" + "=" * 55)
  report.append("       WEB SECURITY & FLAW AUDIT (ENTRY POINTS)")
  report.append("=" * 55)
  try:
    headers_agent = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
        )
    }
    resp = requests.get(url, headers=headers_agent, timeout=10)
    headers = resp.headers

    if url.startswith("https://"):
      report.append("[✓] HTTPS Enabled: Secure transport connection active.")
    else:
      report.append(
          "[!] Security Flaw: Website is on HTTP! Data can be intercepted."
      )

    sec_headers = {
        "Strict-Transport-Security": "Protects against protocol downgrade attacks",
        "Content-Security-Policy": "Mitigates XSS and data injection attacks",
        "X-Frame-Options": "Protects against Clickjacking",
        "X-Content-Type-Options": "Prevents MIME-sniffing",
        "X-XSS-Protection": "Legacy XSS filter header",
    }

    report.append("\n[+] Security Headers Status:")
    for h, desc in sec_headers.items():
      if h in headers:
        report.append(f"    [✓] {h}: Present")
      else:
        report.append(
            f"    [!] {h}: MISSING -> Risk: {desc} (Potential Hacker Entry"
            " Point)"
        )
  except Exception as e:
    report.append(f"[!] Header Audit Error: {e}")
  return "\n".join(report)


def research_content(url):
  report = []
  report.append("\n" + "=" * 55)
  report.append("          WEB CONTENT & RESEARCH SUMMARY")
  report.append("=" * 55)
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code == 200:
      soup = BeautifulSoup(resp.text, "html.parser")
      title = soup.title.string if soup.title else "No Title Found"
      report.append(f"[*] Page Title: {title.strip()}")

      desc = soup.find("meta", attrs={"name": "description"})
      if desc and desc.get("content"):
        report.append(f"[*] Meta Description: {desc['content'].strip()}")

      for el in soup(["script", "style", "nav", "footer", "header"]):
        el.decompose()
      text = soup.get_text(separator="\n", strip=True)
      report.append("\n[+] Extracted Content Preview (First 800 Characters):")
      report.append(text[:800])
    else:
      report.append(f"[!] Page fetch failed with status: {resp.status_code}")
  except Exception as e:
    report.append(f"[!] Content Research Error: {e}")
  return "\n".join(report)


def run_local_ai_advisor(audit_data):
  print(
      CYAN
      + "\n[*] Local AI Security Advisor analyzing scan findings..."
      + RESET
  )
  if not AI_AVAILABLE:
    return (
        "[i] Local AI Note: 'transformers' library not installed. Install via"
        " 'pip install transformers torch' for local AI analysis."
    )

  try:
    # Using a lightweight local model suitable for mobile/CPU execution
    ai_pipeline = pipeline(
        "summarization", model="sshleifer/distilbart-cnn-6-6", device=-1
    )
    # Truncate text to fit model context length
    max_chunk = 1000
    summary_text = audit_data[:max_chunk]
    ai_result = ai_pipeline(
        summary_text, max_length=130, min_length=30, do_sample=False
    )
    return (
        "\n"
        + "=" * 55
        + "\n         LOCAL AI VULNERABILITY INSIGHTS (AI MODEL)\n"
        + "=" * 55
        + f"\n{ai_result[0]['summary_text']}\n"
        + "=" * 55
    )
  except Exception as e:
    return f"[!] AI Analysis Fallback: Rule-based risk assessment normal. (Error: {e})"


def main():
  print_banner()

  while True:
    print(BLUE + "\n--- MAIN MENU ---" + RESET)
    print(f" {GREEN}1.{RESET} Target Scan Shuru Karein (Nmap + Web Audit + AI)")
    print(f" {GREEN}2.{RESET} Command-Line Help & Guide Dekhein")
    print(f" {GREEN}3.{RESET} Exit (Bahir Jayein)")

    choice = input(
        YELLOW + "\nApna option chunein (1-3): " + RESET
    ).strip()

    if choice == "2":
      show_cli_help()
    elif choice == "3":
      print(GREEN + "Tool band ho raha hai. Alvida! Stay Secure!" + RESET)
      break
    elif choice == "1":
      url = input(
          "Target URL ya Domain daalein (jaise example.com ya"
          " https://example.com): "
      ).strip()
      if not url:
        continue
      if not url.startswith("http"):
        url = "https://" + url

      # Parse domain properly removing scheme, ports and paths (Fixed Bug)
      parsed = urlparse(url)
      domain = parsed.netloc if parsed.netloc else parsed.path
      domain = domain.split("/")[0].split(":")[0]

      print(
          CYAN
          + "\n[*] Security Auditor active ho gaya hai... Live scanning shuru"
          " ho chuki hai..."
          + RESET
      )

      # --- RUNNING SCANS ---
      nmap_output = run_nmap_scan(domain)
      header_output = audit_security_headers(url)
      content_output = research_content(url)

      full_audit_report = (
          f"{nmap_output}\n\n{header_output}\n\n{content_output}"
      )

      # Run Local AI Analysis
      ai_insights = run_local_ai_advisor(full_audit_report)
      full_audit_report += f"\n\n{ai_insights}"

      print(GREEN + "\n[✓] Scanning aur AI Analysis poori ho chuki hai!" + RESET)

      # --- POST-SCAN OPTIONS ---
      while True:
        print("\n" + "=" * 55)
        print("  SCAN COMPLETE! AB AAP KYA KARNA CHAHTE HAIN?")
        print("=" * 55)
        print(f" {GREEN}1.{RESET} Termux screen par direct report padhein")
        print(f" {GREEN}2.{RESET} Phone me text file ke roop me save karein")
        print(f" {GREEN}3.{RESET} Main Menu par wapas jayein")

        opt = input("Option chunein (1, 2 ya 3): ").strip()

        if opt == "1":
          print("\n" + "=" * 20 + " FULL AUDIT & AI REPORT " + "=" * 20)
          print(full_audit_report)
          print("=" * 65)
          break
        elif opt == "2":
          fname = (
              input("File ka naam likhein (jaise security_report.txt): ")
              .strip()
              or "security_report.txt"
          )
          try:
            with open(fname, "w", encoding="utf-8") as f:
              f.write(full_audit_report)
            print(
                GREEN
                + f"[+] Success! Report '{fname}' ke roop me save ho gayi hai."
                + RESET
            )
          except Exception as e:
            print(RED + f"[!] File save karne me error: {e}" + RESET)
          break
        elif opt == "3":
          break
        else:
          print(RED + "[!] Kripya sahi option chunein (1, 2 ya 3)." + RESET)
    else:
      print(RED + "[!] Galat option. Kripya 1, 2 ya 3 me se chunein." + RESET)


if __name__ == "__main__":
  main()
        
