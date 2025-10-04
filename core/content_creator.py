import os
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, TextClip, CompositeVideoClip
from tools.promptgen import generate