#!/bin/bash
source .env
echo "🚀 Bootstrapping Agentic Company..."
python launch_master.py
python agents/business_plan_agent.py
python agents/hrm_agent.py
python agents/president_agent.py
python agents/cfo_agent.py
python agents/cto_agent.py
python agents/cmo_agent.py
python agents/product_manager_agent.py
python agents/software_architect_agent.py
python agents/software_developer_agent.py
python agents/devops_agent.py
python agents/qa_agent.py
python agents/ui_ux_designer_agent.py
python agents/technical_writer_agent.py
python agents/marketing_content_agent.py
python agents/sales_agent.py
python agents/legal_counsel_agent.py
python agents/customer_support_agent.py
echo "✅ All systems active. MonitorAgent is watching."