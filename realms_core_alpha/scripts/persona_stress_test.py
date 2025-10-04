import json, random

with open("pantheon_forge/persona_descriptions.json", "r") as f:
    personas = json.load(f)

def stress_test(persona):
    print(f"\n🧠 Testing persona: {persona['name']}")
    print(f"Domain: {persona['domain']}")
    print(f"Challenge: {random.choice(['Ambiguity', 'Contradiction', 'Time Pressure'])}")
    print(f"Response Style: {persona.get('style', 'Unknown')}")
    print(f"Fallback Strategy: {persona.get('fallback', 'None')}\n")

for p in personas:
    stress_test(p)