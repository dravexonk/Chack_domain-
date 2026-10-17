import subprocess
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def print_banner():
  print("=" * 65)
  print("      ADVANCED MOBILE NMAP WEB & SECURITY AUDITOR")
  print("      File Name: auditor_tool.py (100% Local / Zero API)")
  print("=" * 65)


def show_cli_help():
  print("\n" + "=" * 60)
  print("          COMMAND-LINE HELP & USAGE GUIDE")
  print("=" * 60)
  print(
      "Yeh tool aapke mobile (Termux) par ek professional security auditor"
      " ki tarah kaam karta hai."
  )
  print("Yahan bataya gaya hai ki iske modules kaise kaam karte hain:\n")
  print(
      "1. Nmap Port Scan (-T4 & Top Ports):"
      "\n   - Nmap engine ka use karke target domain ke 100 sabse common ports"
      " fast scan karta hai."
      "\n   - Yeh batata hai ki kaun se ports open hain aur wahan kaun si"
      " services chal rahi hain, jo hackers ke liye potential entry points ho"
      " sakti hain.\n"
  )
  print(
      "2. Web Header & Flaw Audit:"
      "\n   - Website ke HTTP headers check karta hai."
      "\n   - Check karta hai ki HTTPS active hai ya nahi, aur kya koi zaroori"
      " security header (jaise CSP, HSTS, X-Frame-Options) missing hai."
      "\n   - In missing headers ka fayda utha kar malicious attacks ho sakte"
      " hain.\n"
  )
  print(
      "3. Web Content & Research:"
      "\n   - Website ka Title, Meta Description aur clean text extract karta"
      " hai.\n"
  )
  print(
      "4. Output Options:"
      "\n   - Scan poora hone ke baad aap report ko direct screen par padh"
      " sakte hain ya phone me file ke roop me save kar sakte hain."
  )
  print("=" * 60 + "\n")


def run_nmap_scan(domain):
  report = []
  report.append("=" * 55)
  report.append("          NMAP NETWORK & PORT SCAN REPORT")
  report.append("=" * 55)
  try:
    print(f"[*] Nmap engine se fast scanning ho rahi hai ({domain})...")
    # -T4 fast speed ke liye, --top-ports 100 common ports check karne ke liye
    cmd = ["nmap", "-T4", "--top-ports", "100", domain]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60
    )

    if result.returncode == 0:
      report.append(result.stdout)
    else:
      report.append(
          "[!] Nmap execution error. Kya aapne Termux me nmap install kiya"
          f" hai?\nError: {result.stderr}"
      )
  except FileNotFoundError:
    report.append(
        "[!] Error: 'nmap' command nahi mili! Kripya Termux me 'pkg install"
        " nmap' run karein."
    )
  except subprocess.TimeoutExpired:
    report.append("[!] Nmap scan time out ho gaya.")
  except Exception as e:
    report.append(f"[!] Nmap error: {e}")
  return "\n".join(report)


def audit_security_headers(url):
  report = []
  report.append("\n" + "=" * 55)
  report.append("       WEB SECURITY & FLAW AUDIT (ENTRY POINTS)")
  report.append("=" * 55)
  try:
    resp = requests.get(url, timeout=10)
    headers = resp.headers

    if url.startswith("https://"):
      report.append("[✓] HTTPS Enabled: Secure transport connection.")
    else:
      report.append(
          "[!] Security Flaw: Website HTTP par hai! Data easily intercept ho"
          " sakta hai."
      )

    sec_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
    ]

    report.append("\n[+] Security Headers Status:")
    for h in sec_headers:
      if h in headers:
        report.append(f"    [✓] {h}: Present")
      else:
        report.append(
            f"    [!] {h}: MISSING (Potential vulnerability / Hacker entry"
            " point)"
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
      report.append("\n[+] Extracted Content Preview (First 1200 Characters):")
      report.append(text[:1200])
    else:
      report.append(f"[!] Page fetch failed with status: {resp.status_code}")
  except Exception as e:
    report.append(f"[!] Content Research Error: {e}")
  return "\n".join(report)


def main():
  print_banner()

  while True:
    print("\n--- MAIN MENU ---")
    print("1. Target Scan Shuru Karein (Nmap + Web Audit + Flaws)")
    print("2. Command-Line Help & Guide Dekhein")
    print("3. Exit (Bahir Jayein)")

    choice = input("\nApna option chunein (1-3): ").strip()

    if choice == "2":
      show_cli_help()
    elif choice == "3":
      print("Tool band ho raha hai. Alvida!")
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

      # Parse domain for nmap
      parsed = urlparse(url)
      domain = parsed.netloc if parsed.netloc else parsed.path
      domain = domain.split("/")[0]

      print(
          "\n[*] Bot active ho gaya hai... Live scanning shuru ho chuki hai..."
      )

      # --- 1. LIVE SCANNING RUNS FIRST ---
      nmap_output = run_nmap_scan(domain)
      header_output = audit_security_headers(url)
      content_output = research_content(url)

      full_audit_report = (
          f"{nmap_output}\n\n{header_output}\n\n{content_output}"
      )
      print("\n[✓] Scanning poori tarah complete ho chuki hai!")

      # --- 2. POST-SCAN OPTIONS (Strict Flow) ---
      while True:
        print("\n" + "=" * 55)
        print("  SCAN COMPLETE! AB AAP KYA KARNA CHAHTE HAIN?")
        print("=" * 55)
        print("1. Termux screen par direct report padhein (Display)")
        print("2. Phone me text file ke roop me save karein (Save to File)")
        print("3. Main Menu par wapas jayein (Skip)")

        opt = input("Option chunein (1, 2 ya 3): ").strip()

        if opt == "1":
          print("\n" + "=" * 25 + " FULL AUDIT REPORT " + "=" * 25)
          print(full_audit_report)
          print("=" * 65)
          break
        elif opt == "2":
          fname = (
              input(
                  "File ka naam likhein (jaise auditor_report.txt): "
              ).strip()
              or "auditor_report.txt"
          )
          try:
            with open(fname, "w", encoding="utf-8") as f:
              f.write(full_audit_report)
            print(
                f"[+] Success! Poori report aapke phone me '{fname}' ke naam se"
                " save ho gayi hai."
            )
          except Exception as e:
            print(f"[!] File save karne me error: {e}")
          break
        elif opt == "3":
          break
        else:
          print("[!] Kripya sahi option chunein (1, 2 ya 3).")
    else:
      print("[!] Galat option. Kripya 1, 2 ya 3 me se chunein.")


if __name__ == "__main__":
  main()
  
