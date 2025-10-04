import os

def build_dashboard():
    os.system("python monetization/generate_revenue_chart.py")
    os.system("python monetization/generate_agent_health.py")
    os.system("python monetization/generate_syndication_status.py")
    print("✅ Dashboard built. Check logs/ for output files.")

if __name__ == "__main__":
    build_dashboard()