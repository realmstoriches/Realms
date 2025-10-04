import random
import os

roles = ["architect", "visionary", "designer", "qa", "tester"]
crews = ["development", "product", "ops", "infra", "strategy"]
departments = ["Engineering", "Innovation", "Quality", "Operations", "Design"]

expert_pool = {
    "architect": [("Linus Torvalds", "John Carmack"), ("Ada Lovelace", "Grace Hopper"), ("Alan Turing", "Dennis Ritchie")],
    "visionary": [("Steve Jobs", "Marty Cagan"), ("Reid Hoffman", "Peter Thiel"), ("Ben Horowitz", "Julie Zhuo")],
    "designer": [("Jony Ive", "Don Norman"), ("Jakob Nielsen", "Dieter Rams"), ("Susan Kare", "Brenda Laurel")],
    "qa": [("Kent Beck", "Martin Fowler"), ("Michael Feathers", "Gerald Weinberg"), ("Lisa Crispin", "Janet Gregory")],
    "tester": [("James Bach", "Michael Bolton"), ("Elisabeth Hendrickson", "Rex Black"), ("Dorothy Graham", "Cem Kaner")]
}

def random_name():
    first = random.choice(["George", "Clara", "Maxwell", "Ivy", "Theo", "Nina", "Jasper", "Luna", "Felix", "Mira"])
    last = random.choice(["Schmeeken", "Voss", "Kincaid", "Rutherford", "Zane", "Hollis", "Bennett", "Quinn", "Frost", "Marin"])
    return f"{first} {last}"

def generate_manifest():
    with open("pantheon_manifest.txt", "w") as f:
        for i in range(1, 1001):
            role = roles[(i - 1) % len(roles)]
            alpha, beta = expert_pool[role][(i - 1) % len(expert_pool[role])]
            agent_name = random_name()
            crew = crews[(i - 1) % len(crews)]
            department = departments[(i - 1) % len(departments)]
            role_id = f"{role}_{i}_prime"
            f.write(f"{role_id},{alpha},{beta},{agent_name},{crew},{role},{department}\n")

if __name__ == "__main__":
    generate_manifest()