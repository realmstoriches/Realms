import os, json, stripe
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import dotenv_values
from pydantic import BaseModel
from uvicorn import run