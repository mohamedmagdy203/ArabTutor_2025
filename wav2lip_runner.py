import sys
import subprocess
import os

print("🚀 Starting wav2lip_runner.py")

if len(sys.argv) != 4:
    print("❌ Usage error")
    sys.exit(1)

video_path = sys.argv[1]
audio_path = sys.argv[2]
output_path = sys.argv[3]

print(f"🎥 Input video: {video_path}")
print(f"🔊 Input audio: {audio_path}")
print(f"📤 Output path: {output_path}")

if os.path.exists(output_path):
    os.remove(output_path)
    print("🗑️ Old output removed.")

command = [
    "python", "Wav2Lip/inference.py",
    "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth",
    "--face", video_path,
    "--audio", audio_path,
    "--outfile", output_path,
    "--pads", "0", "20", "0", "0",
    "--resize_factor", "4",
    "--nosmooth"
]

print("▶️ Running Wav2Lip inference...")
result = subprocess.run(command, capture_output=True, text=True)

print("📄 Wav2Lip stdout:\n", result.stdout)
print("📄 Wav2Lip stderr:\n", result.stderr)

if result.returncode != 0:
    print("❌ Wav2Lip failed.")
    sys.exit(1)

if os.path.exists(output_path):
    print("✅ Wav2Lip output created.")
else:
    print("⚠️ Wav2Lip finished but no output found.")
