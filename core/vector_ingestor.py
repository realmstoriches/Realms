import json
import requests
import logging
import time
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings