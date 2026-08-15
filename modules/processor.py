import cv2
from PIL import Image

def preprocess_image(uploaded_file, max_size=1024):
    image = Image.open(uploaded_file).convert('RGB')
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image

def extract_video_frames(video_file, frame_interval=30):
    vidcap = cv2.VideoCapture(video_file)
    success, image = vidcap.read()
    frames = []
    count = 0
    while success:
        if count % frame_interval == 0:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(image_rgb)
            frames.append(pil_img)
        success, image = vidcap.read()
        count += 1
    vidcap.release()
    return frames
