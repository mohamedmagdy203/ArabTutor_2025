import uuid
import os

def generate_temp_paths(base_dir, ext=".mp4"):
    video_id = uuid.uuid4().hex
    return {
        "input": os.path.join(base_dir, f"input_{video_id}{ext}"),
        "output": os.path.join(base_dir, f"output_{video_id}{ext}"),
        "lip_sync": os.path.join(base_dir, f"lipsync_{video_id}{ext}")
    }
