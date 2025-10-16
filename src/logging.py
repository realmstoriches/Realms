import os
import datetime

def log_post_performance(product_name: str, platform: str, success: bool):
    """
    Logs the performance of a social media post to a simple text file.
    """
    output_dir = "logs"
    os.makedirs(output_dir, exist_ok=True)

    log_file = os.path.join(output_dir, "social_media_performance.log")

    timestamp = datetime.datetime.now().isoformat()
    status = "SUCCESS" if success else "FAILURE"

    with open(log_file, "a") as f:
        f.write(f"{timestamp}\t{product_name}\t{platform}\t{status}\n")