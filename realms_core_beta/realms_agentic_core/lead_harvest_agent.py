import requests, re, time, random, smtplib, dns.resolver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from realms_agentic_core.proxy_pool import PROXIES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_rendered_html(url):
    try:
        options = uc.ChromeOptions()
        options.headless = True
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

def fetch_html(url):
    for attempt in range(3):
        proxy = random.choice(PROXIES)
        try:
            response = requests.get(url, headers=HEADERS, proxies={"http": proxy, "https": proxy}, timeout=10)
            return response.text
        except Exception as e:
            print(f"⚠️ Proxy failed: {proxy} — {e}")
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

def scrape_github_email_dumps():
    repos = [
        "https://github.com/Mithileysh/Email-Datasets",
        "https://github.com/Abumaude/Email_Datasets",
        "https://github.com/berzerk0/Probable-Wordlists"
    ]
    harvested = set()
    for repo in repos:
        html = fetch_html(repo)
        harvested.update(extract_emails_from_html(html))
    return harvested

def harvest_leads(domain_list):
    all_emails = set()
    failed_domains = []
    invalid_emails = []

    for url in domain_list:
        print(f"\n🔎 Scanning: {url}")
        html = fetch_html(url)
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
    github_emails = scrape_github_email_dumps()
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
    domains = [
        # 🧠 Founder & Startup Directories
        "https://www.bookyourdata.com/buy-email-list/founder",
        "https://www.iinfotanks.com/founder-email-list/",
        "https://angel.co/companies",
        "https://www.crunchbase.com/discover/organization.companies",
        "https://www.producthunt.com/startups",
        "https://www.startupblink.com/startups/united-states",
        "https://www.gust.com/startups",
        "https://www.f6s.com/startups",

        # 🧠 Developer & Engineer Hubs
        "https://github.com/torvalds",
        "https://github.com/sindresorhus",
        "https://github.com/gaearon",
        "https://github.com/yyx990803",
        "https://github.com/rauchg",
        "https://stackoverflow.com/users",
        "https://dev.to",

        # 🧠 University Faculty Directories
        "https://www.psu.edu/search/directories",
        "https://www.upenn.edu/directories",
        "https://www.cs.cmu.edu/people",
        "https://www.educationdatalists.com/database/university-lecturers-email-list",

        # 🧠 Tech Speaker Lists
        "https://www.leadingauthorities.com/speaker-list/technology-speakers",
        "https://www.allamericanspeakers.com/lists/view-all-lists.php",
        "https://keynotespeakers.info/technology-speakers/",

        # 🧠 Google Dork Searches
        "https://www.google.com/search?q=site:github.com+%22@gmail.com%22",
        "https://www.google.com/search?q=site:angel.co+%22@founder.com%22",
        "https://www.google.com/search?q=site:linkedin.com/in+%22@startup.ai%22"
    ]

    leads = harvest_leads(domains)
    print(f"\n✅ Final validated leads: {len(leads)}")
    with open("validated_emails.txt", "w") as f:
        for email in leads:
            f.write(email + "\n")