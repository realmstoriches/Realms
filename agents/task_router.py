import json, logging
from fallback_manager import escalate_if_needed
from agent_output_generator import generate_output
from core.executor import execute_tool