import json

def pair_experts(expert_list):
    primes = []
    for i in range(0, len(expert_list), 2):
        alpha = expert_list[i]
        beta = expert_list[i+1]
        prime_name = f"{alpha.split()[0]}-{beta.split()[1]} Prime"
        primes.append({
            "name": prime_name,
            "alpha": alpha,
            "beta": beta
        })
    return primes

if __name__ == "__main__":
    with open("expert_manifest.txt", "r", encoding="utf-8") as f:
        expert_list = [line.strip() for line in f.readlines()]
    prime_agents = pair_experts(expert_list)
    with open("prime_agents.json", "w", encoding="utf-8") as f:
        json.dump(prime_agents, f, indent=4)
    print("✅ Prime agents generated and saved to prime_agents.json")