import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def show_help():
  print("\n================ HELP GUIDE ================")
  print("1. Web Research: Website ka main text aur meta tags nikalta hai.")
  print(
      "2. Security Audit: HTTPS aur security headers check karta hai"
      " (kamiyan dhoondne ke liye)."
  )
  print("3. Port Scanner: Common ports (80, 443, etc.) check karta hai.")
  print(
      "4. Output Options: Scan hone ke baad screen par padhein ya file me"
      " save karein."
  )
  print("==========================================\n")


def scan_website(url):
  full_report = []

  # URL Parse for domain
  parsed = urlparse(url)
  domain = parsed.netloc if parsed.netloc else parsed.path
  domain = domain.split("/")[0]

  print(f"\n[1/3] Website Content & Research ki ja rahi hai ({url})...")
  content_res = research_content(url)
  full_report.append(content_res)

  print("[2/3] Security Headers Audit (Flaws Check) kiya ja raha hai...")
  sec_res = audit_headers(url)
  full_report.append(sec_res)

  print(f"[3/3] Ports scan kiye ja rahe hain ({domain})...")
  port_res = scan_open_ports(domain)
  full_report.append(port_res)

  print("\n[✓] Scanning poori tarah complete ho chuki hai!")
  return "\n\n".join(full_report)


def research_content(url):
  report = []
  report.append("=" * 45)
  report.append("           WEB CONTENT RESEARCH REPORT")
  report.append("=" * 45)
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
      report.append(f"Title: {title.strip()}")

      desc = soup.find("meta", attrs={"name": "description"})
      if desc and desc.get("content"):
        report.append(f"Description: {desc['content'].strip()}")

      for el in soup(["script", "style", "nav", "footer", "header"]):
        el.decompose()
      text = soup.get_text(separator="\n", strip=True)
      report.append("\n--- Extracted Text Preview (First 1500 Characters) ---")
      report.append(text[:1500])
    else:
      report.append(f"Error: Page fetch failed (Status: {resp.status_code})")
  except Exception as e:
    report.append(f"Research Error: {e}")
  return "\n".join(report)


def audit_headers(url):
  report = []
  report.append("\n" + "=" * 45)
  report.append("          SECURITY & FLAW AUDIT REPORT")
  report.append("=" * 45)
  try:
    resp = requests.get(url, timeout=10)
    headers = resp.headers

    if url.startswith("https://"):
      report.append("[✓] HTTPS: Active (Secure Connection)")
    else:
      report.append("[!] Flaw: Website HTTP par hai (Insecure connection!)")

    sec_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
    ]
    for h in sec_headers:
      if h in headers:
        report.append(f"[✓] Header Present: {h}")
      else:
        report.append(f"[!] Flaw / Missing Header: {h}")
  except Exception as e:
    report.append(f"Header Audit Error: {e}")
  return "\n".join(report)


def scan_open_ports(domain):
  report = []
  report.append("\n" + "=" * 45)
  report.append("            PORT SCANNER REPORT")
  report.append("=" * 45)
  ports = [80, 443, 21, 22, 8080, 3306]
  try:
    ip = socket.gethostbyname(domain)
    report.append(f"Target IP: {ip}")
    for p in ports:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(1.0)
      res = s.connect_ex((ip, p))
      if res == 0:
        report.append(f"[OPEN] Port {p} is OPEN")
      else:
        report.append(f"[CLOSED] Port {p} is closed")
      s.close()
  except Exception as e:
    report.append(f"Port Scan Error (Invalid domain or offline): {e}")
  return "\n".join(report)


def main():
  print("=" * 55)
  print("     ADVANCED MOBILE WEB SCANNER & AUDITOR")
  print("=" * 55)

  while True:
    print("\n--- MAIN MENU ---")
    print("1. Naya Scan Shuru Karein")
    print("2. Help & Commands Guide")
    print("3. Exit")

    choice = input("\nApna option chunein (1-3): ").strip()

    if choice == "2":
      show_help()
    elif choice == "3":
      print("Tool band ho raha hai. Alvida!")
      break
    elif choice == "1":
      url = input(
          "Website ka URL daalein (jaise example.com ya"
          " https://example.com): "
      ).strip()
      if not url:
        continue
      if not url.startswith("http"):
        url = "https://" + url

      # Step 1: Real scanning runs here first
      print(
          "\n[*] Bot active ho gaya hai... Website scanning shuru ho gayi"
          " hai..."
      )
      audit_report = scan_website(url)

      # Step 2: Options appear ONLY AFTER scan is fully complete
      while True:
        print("\n" + "=" * 50)
        print("  SCAN COMPLETE! AAP KYA KARNA CHAHTE HAIN?")
        print("=" * 50)
        print("1. Termux screen par direct padhein (Display)")
        print("2. Phone me file ke roop me save karein (Save to File)")
        print("3. Menu par wapas jayein (Skip)")

        opt = input("Option chunein (1, 2 ya 3): ").strip()

        if opt == "1":
          print("\n" + "=" * 25 + " FULL AUDIT REPORT " + "=" * 25)
          print(audit_report)
          print("=" * 65)
          break
        elif opt == "2":
          fname = (
              input("File ka naam likhein (jaise report.txt): ").strip()
              or "audit_report.txt"
          )
          try:
            with open(fname, "w", encoding="utf-8") as f:
              f.write(audit_report)
            print(
                f"[+] Success! Poori report aapke phone me '{fname}' ke roop me"
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
      print("[!] Galat choice. Kripya 1, 2 ya 3 me se chunein.")


if __name__ == "__main__":
  main()
  
