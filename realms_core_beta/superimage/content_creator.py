import os
import uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, TextClip, CompositeVideoClip
from .promptgen import generate as promptgen

class ContentCreator:
    def __init__(self):
        self.width = 1200
        self.height = 630
        self.bg_color = (30, 30, 30)
        self.title_color = (255, 255, 255)
        self.body_color = (200, 200, 200)
        self.cta_color = (0, 255, 0)
        self.font_path = os.path.join(os.path.dirname(__file__), "fonts", "OpenSans-Regular.ttf")
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def load_font(self, size):
        try:
            return ImageFont.truetype(self.font_path, size)
        except:
            return ImageFont.load_default()

    def generate_image(self, title=None, body=None, cta=None):
        title = title or "Realms Dispatch"
        body = body or promptgen()
        cta = cta or "Activate Now →"

        img = Image.new("RGB", (self.width, self.height), color=self.bg_color)
        draw = ImageDraw.Draw(img)

        draw.text((50, 50), title, font=self.load_font(48), fill=self.title_color)
        draw.text((50, 150), body, font=self.load_font(32), fill=self.body_color)
        draw.text((50, 550), cta, font=self.load_font(36), fill=self.cta_color)

        filename = f"{uuid.uuid4()}.png"
        path = Path(self.output_dir) / filename
        img.save(path)
        return str(path)

    def generate_video(self, image_path, duration=6):
        clip = ImageClip(image_path).set_duration(duration)

        overlay = TextClip("Realms Dispatch", fontsize=48, color='white', font='Arial-Bold')\
            .set_position(("center", "bottom")).set_duration(duration)

        video = CompositeVideoClip([clip, overlay])
        video_path = str(Path(self.output_dir) / f"{Path(image_path).stem}.mp4")
        video.write_videofile(video_path, fps=24, codec="libx264", audio=False, verbose=False, logger=None)
        return video_path

    def generate_batch(self, prompts):
        assets = []
        for prompt in prompts:
            img_path = self.generate_image(body=prompt)
            vid_path = self.generate_video(img_path)
            assets.append({"image": img_path, "video": vid_path})
        return assets

    def upload(self, filepath):
        # Replace with actual upload logic (e.g., S3, Cloudinary)
        return f"https://your-host.com/assets/{Path(filepath).name}"