import subprocess

def run_chain():
    print("\n🔗 Running Full Launch Chain...")
    steps = [
        "python post_launch_ignition.py",
        "python dashboard_builder.py",
        "python syndication_master.py",
        "python analytics_tracker.py",
        "python conversion_forecaster.py",
	"python conversion_forecaster.py",
        "python founder_dashboard.py",
        "python syndication_loop.py",
	"python crew_rotation.py",
        "python persona_overlay.py",
        "python traffic_heatmap.py"
    ]
    for step in steps:
        print(f"\n🚀 Executing: {step}")
        subprocess.run(step, shell=True)

if __name__ == "__main__":
    run_chain()