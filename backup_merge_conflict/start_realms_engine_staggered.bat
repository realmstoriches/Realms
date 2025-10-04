@echo off
echo 🔄 Starting Realms Engine with staggered timing...

REM Activate environment
call pantheon_env\Scripts\activate
timeout /t 2

REM Ingest business plan
echo 🚀 Ingesting business plan...
python realms_core_alpha/agentic_launchpad/modules/ingest_business_plan.py
timeout /t 3

REM Launch monetization engine
echo 💰 Launching monetization engine...
start "" python realms_core_alpha/agentic_launchpad/modules/monetization_engine.py
timeout /t 5

REM Start crew scheduler
echo 🕒 Starting crew scheduler...
start "" python realms_core_alpha/agentic_launchpad/modules/crew_scheduler.py
timeout /t 5

REM Start dashboard
echo 📊 Starting dashboard...
start "" python realms_core_alpha/agentic_launchpad/modules/dashboard_builder.py
timeout /t 5

REM Start server
echo 🌐 Starting server...
start "" python server/launch_server.py
timeout /t 5

REM Run outreach modules
echo 📧 Sending email campaign...
python realms_core_alpha/agentic_launchpad/modules/email_campaign_manager.py
timeout /t 2

echo 📝 Publishing content pipeline...
python realms_core_alpha/agentic_launchpad/modules/content_pipeline.py
timeout /t 2

echo 🧠 Running investor outreach...
python realms_core_alpha/agentic_launchpad/modules/investor_relations.py
timeout /t 2

echo ✅ Realms Engine is live and staggered.
pause