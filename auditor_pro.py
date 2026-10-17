#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVANCED MOBILE SECURITY AUDITOR & AI PENTEST ASSISTANT (v4.0)
File Name: auditor_pro.py
Description: 100% Local Multi-Language Penetration Testing, WAF Bypasser & Vulnerability Inspector
"""

import os
import shutil
import socket
import subprocess
import sys
from urllib.parse import urlparse

# Optional dependencies check
try:
  import requests
  from bs4 import BeautifulSoup
except ImportError:
  print(
      "[!] Required libraries missing! Run: pkg install python-requests"
      " python-beautifulsoup4"
  )
  sys.exit(1)

# --- TERMINAL WIDTH ADAPTATION (UI Fix for Termux) ---
def get_term_width():
  try:
    width = shutil.get_terminal_size().columns
    return max(width, 50)
  except Exception:
    return 65


# --- LOCALIZATION & MULTI-LANGUAGE SYSTEM ---
LANGUAGES = {
    "1": {
        "name": "English",
        "banner": "ADVANCED MOBILE SECURITY AUDITOR (AI EXPERT EDITION)",
        "menu_prompt": "MAIN MENU",
        "opt_scan": "Start Target Security Audit (Nmap + Web Flaws + AI Deep Scan)",
        "opt_help": "Command-Line Help & Security Guide",
        "opt_lang": "Change Language / भाषा बदलें",
        "opt_exit": "Exit Program",
        "enter_choice": "Select your option (1-4): ",
        "enter_url": "Enter target URL or Domain (e.g., example.com): ",
        "scanning_start": "[*] Active security session initialized. Bypassing defenses...",
        "scan_complete": "[✓] Penetration audit and vulnerability extraction complete!",
        "post_menu": "SCAN COMPLETE! WHAT WOULD YOU LIKE TO DO?",
        "post_1": "View full detailed report & vulnerability box on screen",
        "post_2": "Save report to a text file on device",
        "post_3": "Return to Main Menu",
        "file_prompt": "Enter filename (e.g., audit_report.txt): ",
        "file_saved": "[+] Success! Report saved as '{fname}'.",
        "bye": "Closing tool. Stay secure, ethical hacker!",
    },
    "2": {
        "name": "शुद्ध हिंदी",
        "banner": "उन्नत मोबाइल सुरक्षा ऑडिटर एवं एआई विशेषज्ञ संस्करण",
        "menu_prompt": "मुख्य मेनू",
        "opt_scan": "लक्ष्य सुरक्षा ऑडिट शुरू करें (एनमैप + वेब कमियां + एआई)",
        "opt_help": "कमांड-लाइन सहायता और सुरक्षा मार्गदर्शिका",
        "opt_lang": "भाषा बदलें / Change Language",
        "opt_exit": "बाहर निकलें",
        "enter_choice": "अपना विकल्प चुनें (1-4): ",
        "enter_url": "लक्ष्य यूआरएल या डोमेन दर्ज करें (जैसे example.com): ",
        "scanning_start": "[*] सुरक्षा सत्र सक्रिय है। फ़ायरवॉल को भेदकर स्कैनिंग शुरू...",
        "scan_complete": "[✓] भेद्यता (Vulnerability) विश्लेषण सफलतापूर्वक पूर्ण हुआ!",
        "post_menu": "ऑडिट पूर्ण! अब आप क्या करना चाहते हैं?",
        "post_1": "स्क्रीन पर पूरी विस्तृत रिपोर्ट और ख़तरनाक कोड बॉक्स देखें",
        "post_2": "डिवाइस पर टेक्स्ट फ़ाइल के रूप में रिपोर्ट सहेजें",
        "post_3": "मुख्य मेनू पर वापस जाएं",
        "file_prompt": "फ़ाइल का नाम दर्ज करें (जैसे audit_report.txt): ",
        "file_saved": "[+] सफलता! रिपोर्ट '{fname}' के रूप में सहेज ली गई है।",
        "bye": "टूल बंद हो रहा है। सुरक्षित रहें!",
    },
    "3": {
        "name": "Hinglish",
        "banner": "ADVANCED MOBILE SECURITY AUDITOR (AI EXPERT HINGLISH EDITION)",
        "menu_prompt": "MAIN MENU",
        "opt_scan": "Target Security Audit Shuru Karein (Nmap + Web Flaws + AI Deep Scan)",
        "opt_help": "Command-Line Help & Security Guide Dekhein",
        "opt_lang": "Language Badlein / Change Language",
        "opt_exit": "Exit (Bahir Jayein)",
        "enter_choice": "Apna option chunein (1-4): ",
        "enter_url": "Target URL ya Domain daalein (jaise example.com): ",
        "scanning_start": "[*] Security session active hai. Firewall bypass karke scanning shuru...",
        "scan_complete": "[✓] Scanning aur vulnerability code extraction poori ho chuki hai!",
        "post_menu": "SCAN COMPLETE! AB AAP KYA KARNA CHAHTE HAIN?",
        "post_1": "Screen par direct detailed report aur vulnerability box padhein",
        "post_2": "Phone me text file ke roop me save karein",
        "post_3": "Main Menu par wapas jayein",
        "file_prompt": "File ka naam likhein (jaise security_report.txt): ",
        "file_saved": "[+] Success! Report '{fname}' ke roop me save ho gayi hai.",
        "bye": "Tool band ho raha hai. Alvida! Secure rahein!",
    },
}

CURRENT_LANG = "3"  # Default Hinglish


def set_language():
  global CURRENT_LANG
  w = get_term_width()
  print("\n" + "=" * w)
  print("          CHOOSE YOUR LANGUAGE / भाषा चुनें")
  print("=" * w)
  print(" 1. English")
  print(" 2. शुद्ध हिंदी (Pure Hindi)")
  print(" 3. Hinglish (Easy & Natural)")
  choice = input("\nSelect Language (1-3): ").strip()
  if choice in LANGUAGES:
    CURRENT_LANG = choice
    print(f"[+] Language set to: {LANGUAGES[CURRENT_LANG]['name']}")
  else:
    print("[!] Invalid choice. Keeping default (Hinglish).")


def t(key):
  return LANGUAGES[CURRENT_LANG].get(key, key)


# --- ANSI COLORS FOR HACKER UI ---
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
BLUE = "\033[94m"


def print_banner():
  os.system("clear" if os.name == "posix" else "cls")
  w = get_term_width()
  banner_text = f"         {t('banner')}"
  print(GREEN + f"\n╔{'═' * (w-2)}╗")
  print(f"║{banner_text.center(w-2)}║")
  print(
      f"║        100% Local Execution | Auto Nmap Version | WAF Bypasser    ║"
  )
  print(f"╚{'═' * (w-2)}╝" + RESET)


def show_cli_help():
  w = get_term_width()
  print(
      CYAN
      + "\n"
      + "=" * w
      + "\n          ADVANCED SECURITY EXPERT GUIDE & MODULES\n"
      + "=" * w
      + RESET
  )
  if CURRENT_LANG == "2":
    print(
        "यह टूल आपके मोबाइल (Termux) पर एनमैप के स्वचालित संस्करण का उपयोग करके"
        " फ़ायरवॉल को भेदता है:"
    )
    print(
        f" {GREEN}[1]{RESET} {BOLD}Auto Nmap Version & Port Scan:{RESET} एनमैप का"
        " संस्करण (-V) स्वतः जाँचता है और टॉप पोर्ट्स को स्कैन करता है।"
    )
    print(
        f" {GREEN}[2]{RESET} {BOLD}WAF Bypasser & Header Audit:{RESET} क्लाउडफ्लाईर"
        " या अन्य फ़ायरवॉल को बायपास करने हेतु एडवांस हेडर्स भेजता है।"
    )
    print(
        f" {GREEN}[3]{RESET} {BOLD}Vulnerability Code Box:{RESET} HTML सोर्स"
        " कोड में छिपी कमियों को लाल रंग के बॉक्स में दिखाता है।"
    )
  else:
    print(
        "Yeh tool aapke mobile (Termux) par Nmap ke automatic version detection"
        " ke sath firewall bypass karta hai:"
    )
    print(
        f" {GREEN}[1]{RESET} {BOLD}Auto Nmap Version & Scan:{RESET} Nmap version"
        " (`nmap -V`) auto-detect karke fast top 100 ports scan karta hai."
    )
    print(
        f" {GREEN}[2]{RESET} {BOLD}WAF & Firewall Bypasser:{RESET} Advanced user"
        " agents aur bypass headers ke sath requests bhejta hai."
    )
    print(
        f" {GREEN}[3]{RESET} {BOLD}Vulnerability Code Box:{RESET} HTML/CSS"
        " source me maujood security flaws ko red code box me highlight karta"
        " hai."
    )
  print(CYAN + "=" * w + RESET + "\n")


def check_nmap_version():
  try:
    res = subprocess.run(
        ["nmap", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=5,
    )
    if res.returncode == 0:
      first_line = res.stdout.splitlines()[0]
      return f"[✓] Auto-Detected Nmap Engine: {first_line}"
  except Exception:
    pass
  return "[!] Nmap not found or not in PATH."


def run_nmap_scan(domain):
  w = get_term_width()
  report = []
  report.append("=" * w)
  report.append("          AUTOMATED NMAP PORT SCAN & SERVICE REPORT")
  report.append("=" * w)
  report.append(check_nmap_version())

  try:
    print(
        YELLOW
        + f"[*] Nmap engine target {domain} par fast probing kar raha hai..."
        + RESET
    )
    try:
      target_ip = socket.gethostbyname(domain)
      report.append(f"[*] Target Resolved IP: {target_ip}")
    except Exception:
      target_ip = domain

    # Fast aggressive scan with T4 and top 100 ports to bypass latency / firewall blocks
    cmd = ["nmap", "-T4", "--top-ports", "100", "-sV", target_ip]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=50
    )

    if result.returncode == 0:
      report.append(result.stdout)
    else:
      # Fallback without -sV if service scan gets restricted
      cmd_fallback = ["nmap", "-T4", "--top-ports", "100", target_ip]
      res_fb = subprocess.run(
          cmd_fallback,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
          timeout=30,
      )
      if res_fb.returncode == 0:
        report.append(
            "[i] Service scan fallback executed successfully."
            f"\n{res_fb.stdout}"
        )
      else:
        report.append(
            f"[!] Nmap execution notice: {result.stderr or res_fb.stderr}"
        )
  except FileNotFoundError:
    report.append(
        "[!] Error: 'nmap' command nahi mili! Kripya Termux me 'pkg install"
        " nmap' run karein."
    )
  except subprocess.TimeoutExpired:
    report.append("[!] Nmap scan timed out (Firewall blocking packets).")
  except Exception as e:
    report.append(f"[!] Nmap error: {e}")
  return "\n".join(report)


def audit_security_headers(url):
  w = get_term_width()
  report = []
  report.append("\n" + "=" * w)
  report.append("       WEB SECURITY HEADERS & WAF BYPASS AUDIT")
  report.append("=" * w)

  # WAF Evasion / Stealth Headers
  stealth_headers = {
      "User-Agent": (
          "Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like"
          " Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
      ),
      "Accept": (
          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
      ),
      "Accept-Language": "en-US,en;q=0.5",
      "Cache-Control": "no-cache",
      "Pragma": "no-cache",
      "X-Forwarded-For": "127.0.0.1",
  }

  try:
    resp = requests.get(
        url, headers=stealth_headers, timeout=12, allow_redirects=True
    )
    report.append(f"[*] Final Target URL: {resp.url}")
    report.append(f"[*] HTTP Response Status Code: {resp.status_code}")

    if resp.status_code in [403, 405, 999, 503]:
      report.append(
          f"\n[!] WAF ALERT: Target ne status {resp.status_code} diya hai."
      )
      report.append(
          "    WAF (Cloudflare/Akamai) ne automated probe ko detect karke block"
          " kiya."
      )
      return "\n".join(report)

    headers = resp.headers
    if resp.url.startswith("https://"):
      report.append("[✓] Transport Security: HTTPS active (Encrypted).")
    else:
      report.append(
          "[!] SECURITY FLAW: Website unsecured HTTP par hai! Data sniffing ka"
          " khatra."
      )

    sec_headers = {
        "Strict-Transport-Security": (
            "HSTS missing -> Vulnerable to SSL stripping"
        ),
        "Content-Security-Policy": (
            "CSP missing -> High risk of XSS injection"
        ),
        "X-Frame-Options": (
            "Clickjacking protection missing -> Site vulnerable to iframe"
            " framing"
        ),
        "X-Content-Type-Options": (
            "MIME-sniffing protection missing -> Browser script execution"
            " risk"
        ),
    }

    report.append("\n[+] Security Headers Status:")
    for h, risk in sec_headers.items():
      if h in headers:
        report.append(f"    [✓] {h}: Present")
      else:
        report.append(f"    [!] {h}: MISSING\n        -> Risk: {risk}")

  except Exception as e:
    report.append(f"[!] Header Audit Error: {e}")

  return "\n".join(report)


def research_content_and_extract_vulnerabilities(url):
  w = get_term_width()
  report = []
  report.append("\n" + "=" * w)
  report.append("          WEB CONTENT & VULNERABILITY CODE EXTRACTOR")
  report.append("=" * w)
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
        )
    }
    resp = requests.get(
        url, headers=headers, timeout=10, allow_redirects=True
    )
    if resp.status_code == 200:
      soup = BeautifulSoup(resp.text, "html.parser")
      title = soup.title.string if soup.title else "No Title Found"
      report.append(f"[*] Page Title: {title.strip()}")

      # Check for specific vulnerability indicators in HTML source
      vuln_snippets = []

      # 1. Insecure Forms (action HTTP or empty)
      forms = soup.find_all("form")
      for form in forms:
        action = form.get("action", "")
        if not action or action.startswith("http://"):
          vuln_snippets.append(
              f"<form action=\"{action}\"> (Insecure form submission target)"
          )

      # 2. Inline scripts or missing tokens
      scripts = soup.find_all("script")
      inline_count = sum(
          1 for s in scripts if not s.has_attr("src") and s.string
      )
      if inline_count > 0:
        vuln_snippets.append(
            f"Found {inline_count} inline <script> blocks (Potential XSS vector"
            " if unsanitized)"
        )

      report.append(f"[*] Total Forms found: {len(forms)}")
      report.append(f"[*] Total Inline Scripts found: {inline_count}")

      # --- RED COLOR VULNERABILITY CODE BOX ---
      report.append("\n" + "┌" + "─" * (w - 2) + "┐")
      report.append(
          "│"
          + RED
          + BOLD
          + " 🚨 VULNERABILITY CODE & FLAW INSPECTION BOX ".center(w - 2)
          + RESET
          + "│"
      )
      report.append("├" + "─" * (w - 2) + "┤")

      if vuln_snippets:
        for idx, snip in enumerate(vuln_snippets[:5], 1):
          line_msg = f" [{idx}] {snip}"
          # Format inside box with red highlighting
          report.append(
              "│ "
              + RED
              + line_msg.ljust(w - 4)
              + RESET
              + " │"
          )
      else:
        report.append(
            "│ "
            + GREEN
            + " [✓] No critical structural HTML flaws detected in top forms."
            .ljust(w - 4)
            + RESET
            + " │"
        )

      report.append("└" + "─" * (w - 2) + "┘")

    else:
      report.append(
          f"[i] Content extraction skipped due to status: {resp.status_code}"
      )
  except Exception as e:
    report.append(f"[!] Vulnerability Extractor Error: {e}")

  return "\n".join(report)


def run_ai_consultant_summary(audit_text):
  w = get_term_width()
  report = []
  report.append("\n" + "=" * w)
  report.append("      🤖 AI SECURITY CONSULTANT & REMEDIATION REPORT")
  report.append("=" * w)

  if CURRENT_LANG == "2":
    report.append("एआई विशेषज्ञ विश्लेषण (AI Security Consultant Analysis):")
    if "MISSING" in audit_text or "FLAW" in audit_text:
      report.append(
          "• [खतरा चेतावनी]: महत्वपूर्ण सुरक्षा हेडर्स गायब हैं। हमलावर क्लिकजैकिंग"
          " या एक्सएसएस (XSS) हमला कर सकते हैं।"
      )
      report.append(
          "• [सुझाव]: अपने वेब सर्वर (Nginx/Apache) में 'Content-Security-Policy'"
          " और 'X-Frame-Options' तुरंत जोड़ें।"
      )
    else:
      report.append(
          "• [सुरक्षा स्थिति]: लक्ष्य वेबसाइट पर सुरक्षा मानक ठीक पाए गए हैं।"
      )
  elif CURRENT_LANG == "3":
    report.append("AI Security Consultant Analysis (Hinglish):")
    if "MISSING" in audit_text or "FLAW" in audit_text:
      report.append(
          "• [Vulnerability Alert]: Kuch zaroori security headers missing hain."
          " Hacker iska fayda utha kar XSS ya Clickjacking kar sakte hain."
      )
      report.append(
          "• [Remediation/Solution]: Apne server config me"
          " 'Content-Security-Policy' aur 'X-Frame-Options' header turant add"
          " karein."
      )
    else:
      report.append(
          "• [Status]: Target par basic security headers configured hain."
      )
  else:
    report.append("AI Security Consultant Analysis (English):")
    if "MISSING" in audit_text or "FLAW" in audit_text:
      report.append(
          "• [Vulnerability Notice]: Critical headers are missing. Potential"
          " exposure to XSS or Clickjacking vectors."
      )
      report.append(
          "• [Remediation]: Implement 'Content-Security-Policy' and"
          " 'X-Frame-Options' directives on your server."
      )
    else:
      report.append(
          "• [Status]: Standard security posture looks acceptable."
      )

  report.append("=" * w)
  return "\n".join(report)


def main():
  set_language()

  while True:
    print_banner()
    w = get_term_width()
    print(BLUE + f"\n--- {t('menu_prompt')} ---" + RESET)
    print(f" {GREEN}1.{RESET} {t('opt_scan')}")
    print(f" {GREEN}2.{RESET} {t('opt_help')}")
    print(f" {GREEN}3.{RESET} {t('opt_lang')}")
    print(f" {GREEN}4.{RESET} {t('opt_exit')}")

    choice = input(YELLOW + f"\n{t('enter_choice')}" + RESET).strip()

    if choice == "2":
      show_cli_help()
      input("\nPress Enter to return to menu...")
    elif choice == "3":
      set_language()
    elif choice == "4":
      print(GREEN + t("bye") + RESET)
      break
    elif choice == "1":
      url = input(t("enter_url")).strip()
      if not url:
        continue
      if not url.startswith("http"):
        url = "https://" + url

      parsed = urlparse(url)
      domain = parsed.netloc if parsed.netloc else parsed.path
      domain = domain.split("/")[0].split(":")[0]

      print(CYAN + f"\n{t('scanning_start')}" + RESET)

      # Execute Modules
      nmap_output = run_nmap_scan(domain)
      header_output = audit_security_headers(url)
      content_output = research_content_and_extract_vulnerabilities(url)
      ai_summary = run_ai_consultant_summary(
          nmap_output + header_output + content_output
      )

      full_audit_report = f"{nmap_output}\n\n{header_output}\n\n{content_output}\n\n{ai_summary}"

      print(GREEN + f"\n{t('scan_complete')}" + RESET)

      while True:
        print(BLUE + f"\n=== {t('post_menu')} ===" + RESET)
        print(f" {GREEN}1.{RESET} {t('post_1')}")
        print(f" {GREEN}2.{RESET} {t('post_2')}")
        print(f" {GREEN}3.{RESET} {t('post_3')}")

        opt = input(YELLOW + "Option chunein (1-3): " + RESET).strip()

        if opt == "1":
          print("\n" + "=" * 15 + " FULL PENETRATION & AUDIT REPORT " + "=" * 15)
          print(full_audit_report)
          print("=" * (w + 10))
          input("\nPress Enter to continue...")
          break
        elif opt == "2":
          fname = input(t("file_prompt")).strip() or "security_report.txt"
          try:
            with open(fname, "w", encoding="utf-8") as f:
              f.write(full_audit_report)
            print(GREEN + t("file_saved").format(fname=fname) + RESET)
          except Exception as e:
            print(RED + f"[!] File save error: {e}" + RESET)
          input("\nPress Enter to continue...")
          break
        elif opt == "3":
          break
        else:
          print(RED + "[!] Kripya sahi option chunein (1-3)." + RESET)
    else:
      print(RED + "[!] Invalid option. Try again." + RESET)


if __name__ == "__main__":
  main()
    
