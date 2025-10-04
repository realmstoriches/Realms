#!/bin/bash
echo "📦 Installing dependencies..."
pip install -r server/requirements.txt
pip install chromadb fastapi uvicorn openai
echo "✅ Environment ready"