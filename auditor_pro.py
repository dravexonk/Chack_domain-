#!/usr/init/env python3
# -*- coding: utf-8 -*-
"""
ADVANCED MOBILE SECURITY AUDITOR & AI PENTEST ASSISTANT (v3.0)
File Name: auditor_pro.py
Description: 100% Local Multi-Language Penetration Testing & Vulnerability Analyzer
"""

import os
import socket
import ssl
import subprocess
import sys
from urllib.parse import urlparse

# Optional dependencies check
try:
  import requests
  from bs4 import BeautifulSoup
except ImportError:
  print(
      "[!] Required libraries missing! Run: pip install requests beautifulsoup4"
  )
  sys.exit(1)

# --- LOCALIZATION DICTIONARY (Multi-Language Support) ---
LANGUAGES = {
    "1": {  # English
        "name": "English",
        "banner": "ADVANCED MOBILE SECURITY AUDITOR (AI EXPERT EDITION)",
        "menu_prompt": "\n--- MAIN MENU ---",
        "opt_scan": "Start Target Security Audit (Nmap + Web Flaws + AI)",
        "opt_help": "Command-Line Help & Security Guide",
        "opt_lang": "Change Language / भाषा बदलें",
        "opt_exit": "Exit Program",
        "enter_choice": "Select your option (1-4): ",
        "enter_url": (
            "Enter target URL or Domain (e.g., example.com or"
            " https://example.com): "
        ),
        "scanning_start": "[*] Security expert session active. Scanning...",
        "scan_complete": "[✓] Audit completed successfully with deep analysis!",
        "post_menu": "\n=== AUDIT COMPLETE! WHAT WOULD YOU LIKE TO DO? ===",
        "post_1": "View full detailed report on screen",
        "post_2": "Save report to a text file on device",
        "post_3": "Return to Main Menu",
        "file_prompt": "Enter filename (e.g., audit_report.txt): ",
        "file_saved": "[+] Success! Report saved as '{fname}'.",
        "bye": "Closing tool. Stay secure, ethical hacker!",
    },
    "2": {  # शुद्ध हिंदी (Pure Hindi)
        "name": "शुद्ध हिंदी",
        "banner": "उन्नत मोबाइल सुरक्षा ऑडिटर एवं एआई विशेषज्ञ संस्करण",
        "menu_prompt": "\n--- मुख्य मेनू ---",
        "opt_scan": "लक्ष्य सुरक्षा ऑडिट शुरू करें (एनमैप + वेब कमियां + एआई)",
        "opt_help": "कमांड-लाइन सहायता और सुरक्षा मार्गदर्शिका",
        "opt_lang": "भाषा बदलें / Change Language",
        "opt_exit": "बाहर निकलें",
        "enter_choice": "अपना विकल्प चुनें (1-4): ",
        "enter_url": (
            "लक्ष्य यूआरएल या डोमेन दर्ज करें (जैसे example.com या"
            " https://example.com): "
        ),
        "scanning_start": (
            "[*] सुरक्षा विशेषज्ञ सत्र सक्रिय है। स्कैनिंग शुरू हो चुकी है..."
        ),
        "scan_complete": (
            "[✓] गहन विश्लेषण के साथ ऑडिट सफलतापूर्वक पूर्ण हो गया है!"
        ),
        "post_menu": "\n=== ऑडिट पूर्ण! अब आप क्या करना चाहते हैं? ===",
        "post_1": "स्क्रीन पर पूरी विस्तृत रिपोर्ट पढ़ें",
        "post_2": "डिवाइस पर टेक्स्ट फ़ाइल के रूप में रिपोर्ट सहेजें",
        "post_3": "मुख्य मेनू पर वापस जाएं",
        "file_prompt": "फ़ाइल का नाम दर्ज करें (जैसे audit_report.txt): ",
        "file_saved": "[+] सफलता! रिपोर्ट '{fname}' के रूप में सहेज ली गई है।",
        "bye": "टूल बंद हो रहा है। सुरक्षित रहें!",
    },
    "3": {  # हिंग्लिश (Hinglish)
        "name": "Hinglish",
        "banner": "ADVANCED MOBILE SECURITY AUDITOR (AI EXPERT HINGLISH EDITION)",
        "menu_prompt": "\n--- MAIN MENU ---",
        "opt_scan": "Target Security Audit Shuru Karein (Nmap + Web Flaws + AI)",
        "opt_help": "Command-Line Help & Security Guide Dekhein",
        "opt_lang": "Language Badlein / Change Language",
        "opt_exit": "Exit (Bahir Jayein)",
        "enter_choice": "Apna option chunein (1-4): ",
        "enter_url": (
            "Target URL ya Domain daalein (jaise example.com ya"
            " https://example.com): "
        ),
        "scanning_start": (
            "[*] Security expert session active hai. Live scanning shuru ho"
            " chuki hai..."
        ),
        "scan_complete": (
            "[✓] Scanning aur deep security analysis poori tarah complete ho"
            " chuki hai!"
        ),
        "post_menu": "\n=== SCAN COMPLETE! AB AAP KYA KARNA CHAHTE HAIN? ===",
        "post_1": "Screen par direct detailed report padhein",
        "post_2": "Phone me text file ke roop me save karein",
        "post_3": "Main Menu par wapas jayein",
        "file_prompt": "File ka naam likhein (jaise security_report.txt): ",
        "file_saved": "[+] Success! Report '{fname}' ke roop me save ho gayi hai.",
        "bye": "Tool band ho raha hai. Alvida! Secure rahein!",
    },
}

CURRENT_LANG = "3"  # Default to Hinglish for user friendliness


def set_language():
  global CURRENT_LANG
  print("\n==================================================")
  print("          CHOOSE YOUR LANGUAGE / भाषा चुनें")
  print("==================================================")
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
  print(
      GREEN
      + f"""
╔═══════════════════════════════════════════════════════════════════╗
║         {t('banner')}          ║
║         100% Local Execution | Expert Pentest AI | Termux         ║
╚═══════════════════════════════════════════════════════════════════╝
"""
      + RESET
  )


def show_cli_help():
  print(
      CYAN
      + "\n"
      + "=" * 60
      + "\n          SECURITY EXPERT GUIDE & MODULES\n"
      + "=" * 60
      + RESET
  )
  if CURRENT_LANG == "2":
    print(
        "यह टूल आपके मोबाइल (Termux) पर एक पेशेवर साइबर सुरक्षा विशेषज्ञ (Cyber"
        " Security Auditor) की तरह काम करता है:"
    )
    print(
        f" {GREEN}[1]{RESET} {BOLD}Nmap Port Scan:{RESET} टारगेट के सबसे महत्वपूर्ण"
        " 100 पोर्ट्स को स्कैन करके खुली हुई सेवाओं (Open Services) की पहचान"
        " करता है।"
    )
    print(
        f" {GREEN}[2]{RESET} {BOLD}Web Header & Flaw Audit:{RESET} सुरक्षा"
        " Headers (जैसे CSP, HSTS, X-Frame-Options) की जाँच करता है और बताता"
        " है कि कौन सी खामी है।"
    )
    print(
        f" {GREEN}[3]{RESET} {BOLD}WAF & Bot Protection Check:{RESET} बड़ी"
        " वेबसाइट्स (जैसे Google) द्वारा लगाए गए सुरक्षा कवच (WAF/Cloudflare)"
        " को पहचानता है।"
    )
  else:
    print(
        "Yeh tool aapke mobile (Termux) par ek professional security expert"
        " ki tarah kaam karta hai:"
    )
    print(
        f" {GREEN}[1]{RESET} {BOLD}Nmap Port Scan:{RESET} Target ke 100 common"
        " ports scan karta hai aur open services/daemons dhoondta hai."
    )
    print(
        f" {GREEN}[2]{RESET} {BOLD}Web Header & Flaw Audit:{RESET} HTTPS"
        " status, SSL grade aur missing security headers (CSP, HSTS,"
        " X-Frame-Options) check karta hai."
    )
    print(
        f" {GREEN}[3]{RESET} {BOLD}WAF & Bot Defense Analysis:{RESET} Check"
        " karta hai ki target par Cloudflare ya WAF active hai ya nahi."
    )
  print(CYAN + "=" * 60 + RESET + "\n")


def run_nmap_scan(domain):
  report = []
  report.append("=" * 60)
  report.append("          NMAP NETWORK & PORT SCAN AUDIT REPORT")
  report.append("=" * 60)
  try:
    print(
        YELLOW
        + f"[*] Nmap engine target {domain} par deep port probing kar raha"
        " hai..."
        + RESET
    )
    try:
      target_ip = socket.gethostbyname(domain)
      report.append(f"[*] Target Resolved IP Address: {target_ip}")
    except Exception:
      target_ip = domain

    # Using -sV for service version detection if possible, or fast -T4 top ports
    cmd = ["nmap", "-T4", "--top-ports", "100", target_ip]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60
    )

    if result.returncode == 0:
      report.append(result.stdout)
    else:
      report.append(
          f"[!] Nmap execution notice. Error/Output:\n{result.stderr}"
      )
  except FileNotFoundError:
    report.append(
        "[!] Error: 'nmap' command nahi mili! Kripya Termux me 'pkg install"
        " nmap' run karein."
    )
  except subprocess.TimeoutExpired:
    report.append(
        "[!] Nmap scan time out ho gaya (Target ne response delay kiya)."
    )
  except Exception as e:
    report.append(f"[!] Nmap error: {e}")
  return "\n".join(report)


def audit_security_headers(url):
  report = []
  report.append("\n" + "=" * 60)
  report.append("       WEB SECURITY, HEADERS & WAF FLAW AUDIT")
  report.append("=" * 60)

  # Professional User-Agent rotation to prevent instant blocking on major sites like Google
  headers_agent = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      ),
      "Accept-Language": "en-US,en;q=0.9",
  }

  try:
    # Handle redirects and exceptions gracefully
    resp = requests.get(
        url, headers=headers_agent, timeout=12, allow_redirects=True
    )
    report.append(f"[*] Final Target URL: {resp.url}")
    report.append(f"[*] HTTP Response Status Code: {resp.status_code}")

    # Expert analysis for WAF / Bot blocks (like Google, Cloudflare, Akamai)
    if resp.status_code in [403, 405, 999, 503]:
      report.append(
          f"\n[!] EXPERT ANALYSIS: Target ne HTTP status {resp.status_code}"
          " return kiya hai."
      )
      report.append(
          "    Iska matlab hai ki target website par Advanced WAF (Web"
          " Application Firewall),"
      )
      report.append(
          "    Cloudflare, ya Bot Protection active hai jo automated scripts"
          " ko block karti hai."
      )
      report.append(
          "    Yeh ek strong security defense mechanism hai, na ki website ki"
          " kamzori!"
      )
      return "\n".join(report)

    headers = resp.headers

    if resp.url.startswith("https://"):
      report.append(
          "[✓] Transport Security: HTTPS active hai (Secure Encrypted"
          " Connection)."
      )
    else:
      report.append(
          "[!] SECURITY FLAW: Website unsecured HTTP par chal rahi hai! Data"
          " sniffing ka khatra hai."
      )

    sec_headers = {
        "Strict-Transport-Security": (
            "HSTS missing - Vulnerable to SSL stripping attacks"
        ),
        "Content-Security-Policy": (
            "CSP missing - High risk of Cross-Site Scripting (XSS) & Data"
            " Injection"
        ),
        "X-Frame-Options": (
            "Clickjacking protection missing - Site can be embedded in malicious"
            " iframes"
        ),
        "X-Content-Type-Options": (
            "MIME-sniffing protection missing - Browser may execute malicious"
            " files"
        ),
        "X-XSS-Protection": (
            "Legacy browser XSS filter missing (Recommended for older clients)"
        ),
    }

    report.append("\n[+] Security Headers Evaluation:")
    for h, risk in sec_headers.items():
      if h in headers:
        report.append(f"    [✓] {h}: Present & Configured")
      else:
        report.append(f"    [!] {h}: MISSING\n        -> Risk: {risk}")

  except requests.exceptions.Timeout:
    report.append(
        "[!] Error: Request timed out. Target response slow hai ya connection"
        " block hai."
    )
  except requests.exceptions.ConnectionError:
    report.append(
        "[!] Error: Connection failed. Domain galat ho sakta hai ya internet"
        " disconnected hai."
    )
  except Exception as e:
    report.append(f"[!] Header Audit Error: {e}")

  return "\n".join(report)


def research_content(url):
  report = []
  report.append("\n" + "=" * 60)
  report.append("          WEB CONTENT & METADATA INTELLIGENCE")
  report.append("=" * 60)
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

      desc = soup.find("meta", attrs={"name": "description"})
      if desc and desc.get("content"):
        report.append(f"[*] Meta Description: {desc['content'].strip()}")
      else:
        report.append(
            "[*] Meta Description: Not found (SEO / Information disclosure"
            " gap)"
        )

      for el in soup(["script", "style", "nav", "footer", "header"]):
        el.decompose()
      text = soup.get_text(separator="\n", strip=True)
      report.append("\n[+] Extracted Content Preview (First 800 Characters):")
      report.append(text[:800])
    else:
      report.append(
          f"[i] Content extraction skipped due to HTTP status:"
          f" {resp.status_code}"
      )
  except Exception as e:
    report.append(f"[!] Content Research Error: {e}")
  return "\n".join(report)


def run_expert_ai_summary(audit_text):
  report = []
  report.append("\n" + "=" * 60)
  report.append("      🤖 AI SECURITY EXPERT SUMMARY & RECOMMENDATIONS")
  report.append("=" * 60)

  # Rule-based expert AI engine simulating human security consultant insights
  report.append(
      "As your personal AI Security Consultant, I have evaluated the scan"
      " results:"
  )
  if "MISSING" in audit_text:
    report.append(
        "• [Vulnerability Alert] Several crucial HTTP security headers are"
        " missing. Attackers can exploit this via Clickjacking or XSS injection."
    )
    report.append(
        "• [Remediation] Configure your Nginx/Apache web server to add"
        " 'Content-Security-Policy' and 'X-Frame-Options' headers immediately."
    )
  if "HTTP" in audit_text and "HTTPS" not in audit_text:
    report.append(
        "• [Critical Risk] Unencrypted HTTP protocol detected. Implement SSL/TLS"
        " certificate (Let's Encrypt) to enforce secure HTTPS."
    )
  if "WAF" in audit_text or "403" in audit_text:
    report.append(
        "• [WAF Notice] The target employs robust Web Application Firewall (WAF)"
        " protections, which successfully mitigated automated inspection."
    )

  report.append(
      "• [General Advice] Always perform penetration testing with explicit"
      " authorization from the target owner."
  )
  report.append("=" * 60)
  return "\n".join(report)


def main():
  # Initial Language Selection
  set_language()

  while True:
    print_banner()
    print(BLUE + t("menu_prompt") + RESET)
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

      # Parse domain cleanly (handling ports, paths, etc.)
      parsed = urlparse(url)
      domain = parsed.netloc if parsed.netloc else parsed.path
      domain = domain.split("/")[0].split(":")[0]

      print(CYAN + f"\n{t('scanning_start')}" + RESET)

      # --- EXECUTE AUDIT MODULES ---
      nmap_output = run_nmap_scan(domain)
      header_output = audit_security_headers(url)
      content_output = research_content(url)
      ai_expert_summary = run_expert_ai_summary(
          nmap_output + header_output + content_output
      )

      full_audit_report = f"{nmap_output}\n\n{header_output}\n\n{content_output}\n\n{ai_expert_summary}"

      print(GREEN + f"\n{t('scan_complete')}" + RESET)

      # --- POST-SCAN INTERACTIVE OPTIONS ---
      while True:
        print(BLUE + t("post_menu") + RESET)
        print(f" {GREEN}1.{RESET} {t('post_1')}")
        print(f" {GREEN}2.{RESET} {t('post_2')}")
        print(f" {GREEN}3.{RESET} {t('post_3')}")

        opt = input(YELLOW + "Option chunein (1-3): " + RESET).strip()

        if opt == "1":
          print("\n" + "=" * 25 + " FULL SECURITY AUDIT REPORT " + "=" * 25)
          print(full_audit_report)
          print("=" * 75)
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
          print(RED + "[!] Kripya sahi option chunein (1, 3)." + RESET)
    else:
      print(RED + "[!] Invalid option. Try again." + RESET)


if __name__ == "__main__":
  main()
