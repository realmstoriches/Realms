import requests, re, time, random, smtplib, dns.resolver, shutil
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_rendered_html(url):
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        chrome_path = shutil.which("chrome") or shutil.which("google-chrome")
        if chrome_path:
            options.binary_location = chrome_path
        driver = uc.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"❌ Headless render failed: {url} — {e}")
        return ""

def extract_emails_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    emails = set()

    for a in soup.find_all("a", href=True):
        if "mailto:" in a["href"]:
            emails.add(a["href"].replace("mailto:", "").strip())

    for code_block in soup.find_all("code"):
        found = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", code_block.text)
        emails.update(found)

    text = soup.get_text()
    found = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    emails.update(found)

    return emails

def fetch_html(url, proxies=None):
    for attempt in range(3):
        proxy = random.choice(proxies) if proxies else None
        try:
            response = requests.get(url, headers=HEADERS, proxies={"http": proxy, "https": proxy} if proxy else None, timeout=10)
            return response.text
        except Exception as e:
            print(f"⚠️ Proxy failed: {proxy} — {e}")
    print("🔁 Retrying without proxy...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.text
    except Exception as e:
        print(f"❌ Final failure: {url} — {e}")
        return ""

def validate_email(email):
    domain = email.split('@')[-1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)
        server = smtplib.SMTP()
        server.connect(mx_host)
        server.helo()
        server.mail('test@realms.ai')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False

def scrape_github_email_dumps(proxies=None):
    repos = [
        "https://github.com/Mithileysh/Email-Datasets",
        "https://github.com/Abumaude/Email_Datasets",
        "https://github.com/berzerk0/Probable-Wordlists"
    ]
    harvested = set()
    for repo in repos:
        html = fetch_html(repo, proxies=proxies)
        harvested.update(extract_emails_from_html(html))
    return harvested

def harvest_leads(domain_list, proxies=None):
    all_emails = set()
    failed_domains = []
    invalid_emails = []

    for url in domain_list:
        print(f"\n🔎 Scanning: {url}")
        html = fetch_html(url, proxies=proxies)
        emails = extract_emails_from_html(html)

        if not emails:
            print("⚠️ No emails via raw HTML — trying headless browser...")
            html = get_rendered_html(url)
            emails = extract_emails_from_html(html)

        if not emails:
            failed_domains.append(url)
            continue

        for email in emails:
            print(f"🔍 Validating: {email}")
            if validate_email(email):
                print(f"✅ Valid: {email}")
                all_emails.add(email)
            else:
                print(f"❌ Invalid: {email}")
                invalid_emails.append(email)

    print("\n📦 Scraping GitHub email dump repositories...")
    github_emails = scrape_github_email_dumps(proxies=proxies)
    for email in github_emails:
        print(f"🔍 Validating GitHub dump email: {email}")
        if validate_email(email):
            print(f"✅ Valid: {email}")
            all_emails.add(email)
        else:
            print(f"❌ Invalid: {email}")
            invalid_emails.append(email)

    if failed_domains:
        with open("harvest_failed.txt", "w") as f:
            for d in failed_domains:
                f.write(d + "\n")
        print(f"\n⚠️ Logged {len(failed_domains)} failed domains to harvest_failed.txt")

    if invalid_emails:
        with open("invalid_emails.txt", "w") as f:
            for e in invalid_emails:
                f.write(e + "\n")
        print(f"⚠️ Logged {len(invalid_emails)} invalid emails to invalid_emails.txt")

    return list(all_emails)

if __name__ == "__main__":
    domains = [ ... ]  # your full domain list here
    leads = harvest_leads(domains, proxies=None)
    print(f"\n✅ Final validated leads: {len(leads)}")
    with open("validated_emails.txt", "w") as f:
        for email in leads:
            f.write(email + "\n")

def fallback_regex_scrape(html):
    import re
    return re.findall(r'[\w\.-]+@[\w\.-]+', html)
