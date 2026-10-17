import os
import socket
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def print_banner():
  print("=" * 60)
  print("   ADVANCED MOBILE WEB RESEARCH & AUDIT TOOL (Local)")
  print("=" * 60)


def show_help():
  print("\n--- HELP & COMMAND GUIDE ---")
  print(
      "1. Web Research / Reader: Website ka title, description aur main content"
      " nikalta hai."
  )
  print(
      "2. Security Audit (Flaws): Website ke security headers check karta hai"
      " (jaise HTTPS, X-Frame-Options, CSP) taaki kamiyan pata chalein."
  )
  print(
      "3. Port Scanner: Target website ke common open ports (80, 443, 21, etc.)"
      " ko scan karta hai."
  )
  print(
      "4. Output Options: Result ko turant screen par padhein ya file me save"
      " karein."
  )
  print("--------------------------------------------------\n")


def audit_security_headers(url):
  """Website ke security headers check karke kamiyan (flaws) batata hai."""
  report = []
  report.append("\n[+] --- SECURITY & HEADER AUDIT (FLAW CHECK) ---")
  try:
    response = requests.get(url, timeout=10)
    headers = response.headers

    # HTTPS Check
    if url.startswith("https://"):
      report.append("[✓] HTTPS Enabled: Connection secure hai.")
    else:
      report.append(
          "[!] Flaw Found: Website HTTP par hai (Insecure connection!)."
      )

    # Security Headers checks
    sec_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
    ]

    for sh in sec_headers:
      if sh in headers:
        report.append(f"[✓] {sh} header present hai.")
      else:
        report.append(
            f"[!] Flaw Found: '{sh}' header missing hai (Potential security"
            " risk)."
        )

  except Exception as e:
    report.append(f"[!] Header audit error: {e}")

  return "\n".join(report)


def scan_ports(domain):
  """Target domain ke common ports check karta hai."""
  report = []
  report.append("\n[+] --- PORT SCANNER REPORT ---")
  common_ports = [80, 443, 21, 22, 8080, 3306]

  try:
    # IP resolve karna
    ip = socket.gethostbyname(domain)
    report.append(f"[*] Target IP Address: {ip}")

    for port in common_ports:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(1.5)
      result = s.connect_ex((ip, port))
      if result == 0:
        report.append(
            f"[OPEN] Port {port} is OPEN (Service running / Accessible)"
        )
      else:
        report.append(f"[CLOSED] Port {port} is closed.")
      s.close()
  except Exception as e:
    report.append(
        f"[!] Port scanning error (Domain galat ho sakta hai): {e}"
    )

  return "\n".join(report)


def research_website(url):
  """Website ka content aur summary extract karta hai."""
  report = []
  report.append("\n[+] --- WEB CONTENT RESEARCH & READING ---")
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
        )
    }
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")

      # Title & Meta Description
      title = soup.title.string if soup.title else "No Title Found"
      meta_desc = ""
      desc_tag = soup.find("meta", attrs={"name": "description"})
      if desc_tag and desc_tag.get("content"):
        meta_desc = desc_tag["content"]

      report.append(f"[*] Page Title: {title.strip()}")
      if meta_desc:
        report.append(f"[*] Meta Description: {meta_desc.strip()}")

      # Unnecessary elements remove karna
      for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

      clean_text = soup.get_text(separator="\n", strip=True)
      report.append("\n[+] Extracted Content Preview (First 2000 Characters):")
      report.append(clean_text[:2000])
    else:
      report.append(
          f"[!] Page fetch nahi ho saka. Status Code: {response.status_code}"
      )
  except Exception as e:
    report.append(f"[!] Research Error: {e}")

  return "\n".join(report)


def main():
  print_banner()

  while True:
    print("\n--- MAIN MENU ---")
    print("1. Website Research, Flaw Detection & Port Scan shuru karein")
    print("2. Help & Commands Guide dekhein")
    print("3. Exit (Bahir jayein)")

    choice = input("\nApna option chunein (1-3): ").strip()

    if choice == "2":
      show_help()
      continue
    elif choice == "3":
      print("Tool band ho raha hai. Alvida!")
      break
    elif choice == "1":
      target_url = input(
          "Website ka URL daalein (jaise https://example.com): "
      ).strip()
      if not target_url:
        continue
      if not target_url.startswith("http"):
        target_url = "https://" + target_url

      # Parse domain for port scanning
      parsed_url = urlparse(target_url)
      domain = parsed_url.netloc or parsed_url.path

      print(
          "\n[*] Bot active ho gaya hai... Website ko scan aur read kiya ja"
          " raha hai..."
      )

      # Run all modules
      content_report = research_website(target_url)
      security_report = audit_security_headers(target_url)

      # Domain cleaning for socket
      clean_domain = domain.split("/")[0]
      port_report = scan_ports(clean_domain)

      full_output = f"{content_report}\n\n{security_report}\n\n{port_report}"

      # Output Options: Screen par direct display ya File me save
      print("\n" + "=" * 50)
      print("  OUTPUT OPTIONS (Aap kya karna chahte hain?)")
      print("=" * 50)
      print("1. Direct Screen par padhein (Display)")
      print("2. File me save karein (Save to File)")

      opt = input("Option chunein (1 ya 2): ").strip()

      if opt == "1":
        print("\n" + "=" * 20 + " FULL AUDIT REPORT " + "=" * 20)
        print(full_output)
        print("=" * 65)
      elif opt == "2":
        fname = (
            input(
                "File ka naam likhein (jaise audit_result.txt): "
            ).strip()
            or "audit_result.txt"
        )
        try:
          with open(fname, "w", encoding="utf-8") as f:
            f.write(full_output)
          print(
              f"[+] Success! Poori report aapke phone me '{fname}' ke naam se save"
              " ho gayi hai."
          )
        except Exception as e:
          print(f"[!] File save karne me error aayi: {e}")
      else:
        print("[!] Galat option chuna, default screen par dikha rahe hain:")
        print(full_output)
    else:
      print("[!] Kripya sahi option (1, 2 ya 3) chunein.")


if __name__ == "__main__":
  main()
  
