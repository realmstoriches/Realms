# heartbeat.sh
#!/bin/bash
modules=("dispatch_wordpress.py" "dispatch_linkedin.py" "fallback_email.py")

foreach ($module in $modules) { ... }
do
  if ! pgrep -f "$module" > /dev/null
  then
    echo "$(date) - $module not running" >> heartbeat_log.txt
    python fallback_${module}
  fi
done
echo "$(date) - All modules running" >> heartbeat_log.txt