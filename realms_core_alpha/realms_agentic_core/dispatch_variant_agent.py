import random
from datetime import datetime

def generate_variant(payment_link=None):
    title_variants = [
        "🧭 Founder Log: Autonomous Cycle Complete",
        "📅 System Reflection: Credential Flow Verified",
        "🛠️ Quiet Dispatch: No Manual Steps Required",
        "🧠 Realms Update: Legacy Enforced"
    ]
    theme_variants = [
        "Today I watched Realms complete a full cycle—credentials refreshed, content distributed, no manual steps required.",
        "The system ran cleanly—automated credential flows, successful content routing, zero human intervention.",
        "Realms executed a full dispatch loop—tokens rotated, content posted, fallback logic verified.",
        "Another quiet cycle—agents performed credential refresh and platform routing without interruption."
    ]
    reflection_variants = [
        "Grateful for the quiet hours when systems run without intervention.",
        "Every cycle reminds me why automation is legacy.",
        "No alerts. No errors. Just sovereign execution.",
        "This is what operational independence feels like."
    ]
    cta_variants = [
        "Support the mission → {link}",
        "Access the ritual → {link}",
        "Join the system → {link}",
        "Explore Realms tools → {link}"
    ]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    emoji = random.choice(["🧭", "📅", "⏱️", "🕒"])
    hashtag = f"#FounderLog_{timestamp.replace(':','').replace(' ','_')}"
    footer = f"{emoji} Logged at {timestamp}\n{hashtag}"

    structures = [
        lambda r, t, th, c, f: f"{r}\n\n{t}\n\n{th}\n\n{c}\n\n{f}",
        lambda r, t, th, c, f: f"{t}\n\n{r}\n\n{th}\n\n{c}\n\n{f}",
        lambda r, t, th, c, f: f"{th}\n\n{r}\n\n{c}\n\n{t}\n\n{f}",
        lambda r, t, th, c, f: f"{r}\n\n{th}\n\n{t}\n\n{c}\n\n{f}"
    ]

    title = random.choice(title_variants)
    theme = random.choice(theme_variants)
    reflection = random.choice(reflection_variants)
    structure = random.choice(structures)

    cta = random.choice(cta_variants).format(link=payment_link) if payment_link else ""

    content = structure(reflection, title, theme, cta, footer)

    return {
        "title": title,
        "content": content
    }