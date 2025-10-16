# Scheduling the Agentic Workforce

To make the agentic workforce fully autonomous, you can schedule the main script to run automatically at a specific time each day. On Linux-based systems (like a server or a Raspberry Pi), the standard way to do this is with a `cron` job.

## Setting Up a Daily Cron Job

Here are the steps to set up a `cron` job that runs the `main.py` script every day at 9:00 AM.

### 1. Open the Crontab

Open a terminal and enter the following command to edit the cron table for the current user:

```bash
crontab -e
```

If it's your first time, you might be asked to choose a text editor (like `nano` or `vim`). Choose the one you are most comfortable with.

### 2. Add the Cron Job Entry

Add the following line to the end of the file:

```
0 9 * * * /usr/bin/python3 /path/to/your/project/main.py >> /path/to/your/project/logs/cron.log 2>&1
```

### Breaking Down the Command:

-   `0 9 * * *`: This is the schedule. It means "at minute 0 of hour 9 on every day of the month, every month, and every day of the week." In short: 9:00 AM daily.
-   `/usr/bin/python3`: This is the absolute path to your Python 3 interpreter. You can find this by running `which python3` in your terminal. **It's very important to use the absolute path.**
-   `/path/to/your/project/main.py`: This is the **absolute path** to the `main.py` script in your project directory. Replace `/path/to/your/project/` with the actual full path (e.g., `/home/user/agentic-swarm/main.py`).
-   `>> /path/to/your/project/logs/cron.log 2>&1`: This part is for logging.
    -   `>>`: Appends the output to a log file.
    -   `/path/to/your/project/logs/cron.log`: The location of the log file. Make sure the `logs` directory exists.
    -   `2>&1`: Redirects any errors (`stderr`) to the same log file, so you can see both normal output and error messages in one place.

### 3. Save and Exit

-   If you are using `nano`, press `Ctrl + X`, then `Y` to confirm, and `Enter` to save.
-   If you are using `vim`, press `Esc`, then type `:wq` and press `Enter`.

The cron job is now active and will run your agentic workforce automatically every morning. You can check the `cron.log` file to see the output of each run.