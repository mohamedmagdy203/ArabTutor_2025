import os
import boto3
import sys
import glob
from fastapi import APIRouter, Request
from dotenv import load_dotenv
from app.dubbing import process_video_with_translated_audio
import subprocess

load_dotenv()

router = APIRouter()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

@router.post("/mkz")
async def dub_from_s3(request: Request):
    data = await request.json()
    key = data.get("key", data.get("Key"))

    print(f"🚀 Full request data: {data}")
    print(f"📥 Received key: {key}")

    if not key:
        return {"error": "Missing S3 key!"}

    base_filename = os.path.basename(key)
    base_name_only = os.path.splitext(base_filename)[0]

    local_in = f"temp/{base_filename}"
    output_no_lip = f"temp/dubbed_{base_name_only}.mp4"
    lipsynced_out = f"temp/lipsync_{base_name_only}.mp4"
    os.makedirs("temp", exist_ok=True)

    try:
        print(f"⬇️ Downloading from S3: {key} to {local_in}")
        s3.download_file(BUCKET_NAME, key, local_in)
    except Exception as e:
        return {"error": f"Failed to download from S3: {e}"}

    result = process_video_with_translated_audio(local_in, output_no_lip)
    print(f"✅ Dubbing done. Output path: {result.get('output_path')}, Summary: {result.get('summary')}")

    if not result.get("output_path"):
        return {"error": "process_video_with_translated_audio() did not return output_path!"}

    command = [
        "conda", "run", "-n", "wave_env", "python", "wav2lip_runner.py",
        local_in, result["output_path"], lipsynced_out
    ]

    print(f"🔁 Running Wav2Lip with command:\n{' '.join(command)}")

    wav2lip_result = subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)

    if wav2lip_result.returncode != 0:
        return {
            "error": "Wav2Lip failed",
            "stderr": "See console output for details"
        }

    print(f"📁 Checking lipsynced_out path: {lipsynced_out}")
    print(f"📂 Temp folder content:", os.listdir("temp"))

    if not os.path.exists(lipsynced_out):
        matches = glob.glob("temp/lipsync_*.mp4")
        print("🔍 Found lipsync files:", matches)
        return {"error": "Lipsynced output video not found after Wav2Lip!"}

    final_key = f"lipsync_{base_name_only}.mp4"
    try:
        print(f"⬆️ Uploading to S3: {final_key}")
        s3.upload_file(lipsynced_out, BUCKET_NAME, final_key,ExtraArgs={'ContentType': 'video/mp4'})
        print("✅ Uploaded to S3 successfully")
    except Exception as e:
        return {"error": f"Failed to upload final output to S3: {e}"}

    return {
        "dubbed_key": final_key,
        "summary": result["summary"]
    }
