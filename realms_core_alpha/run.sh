#!/bin/bash
echo "🔧 Setting up Realms Core..."
source setup_env.sh
echo "🚀 Launching FastAPI server..."
uvicorn server.main:app --reload