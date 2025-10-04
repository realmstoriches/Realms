import urllib.parse

def generate_sources(expert_name):
    base = expert_name.replace(" ", "_")
    return [
        f"https://en.wikipedia.org/wiki/{base}",
        f"https://github.com/{base.lower().replace('_', '')}",
        f"https://www.ted.com/search?q={urllib.parse.quote(expert_name)}",
        f"https://www.semanticscholar.org/search?q={urllib.parse.quote(expert_name)}",
        f"https://{base.lower()}.com"
    ]