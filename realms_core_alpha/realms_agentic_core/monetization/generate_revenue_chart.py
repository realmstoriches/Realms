from datetime import datetime

def estimate_revenue(email_count, content):
    # === Basic heuristic: $0.50 per email dispatched ===
    base_rate = 0.50
    multiplier = 1.0

    # === Bonus if Stripe CTA is present ===
    if "stripe.com" in content.lower():
        multiplier += 0.25

    # === Bonus if variant content is appended ===
    if "#FounderLog_" in content:
        multiplier += 0.25

    estimated = round(email_count * base_rate * multiplier, 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"💰 Estimated revenue: ${estimated} from {email_count} emails @ {timestamp}")
    return estimated