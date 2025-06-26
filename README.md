# 🎓 Arab Tutor - AI Video Dubbing & Summarization

This graduation project, **Arab Tutor**, is designed to help Arabic-speaking students understand English educational content more easily by automatically dubbing English videos into Arabic and summarizing their content.

By using advanced AI techniques, the project transforms English videos into:

* 🎧 **Arabic-dubbed versions** with synchronized lip movements
* 🧠 **Arabic summaries** of the content to aid understanding and studying

Ideal for students who face language barriers when studying international material like MOOCs, academic lectures, and tutorials.

---

## 🌐 API Overview

### POST `/dub`

Upload an English video to start the dubbing + summarization process.

#### Request

* `multipart/form-data`
* Field: `file` (MP4 video)

#### Response

```json
{
  "summary": "...Arabic summary...",
  "download_url": "https://abc123.ngrok.io/download/output_xxx.mp4"
}
```

---

### GET `/download/{filename}`

Download the final dubbed video using the filename from the `/dub` response.

---

## ⚙️ Technologies Used

* **FastAPI** – RESTful API backend
* **Whisper** – Speech-to-text transcription (English)
* **BART** – Text summarization
* **XTTS** – Multilingual Text-to-Speech (Arabic)
* **Wav2Lip** – Lip-syncing Arabic speech to the speaker's lips
* **Deep Translator** – English to Arabic translation
* **MoviePy & ffmpeg** – Audio/video processing
* **ngrok** – Public URL for local testing

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/mohamedmagdy203/Arab_tutor.git
cd Arab_tutor
```

### 2. Install Requirements

Create and activate your Python environment:

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Start ngrok Tunnel

```bash
ngrok config add-authtoken <your-token>
ngrok http 8000
```

### 5. Open API Docs

Go to:

```
https://abc123.ngrok.io/docs
```

---

## 🔁 API Flow (Frontend Integration)

1. Frontend uploads video via `POST /dub`
2. Receives:

   * `summary`: Arabic summary string
   * `download_url`: URL to download dubbed video
3. Hits `GET /download/{filename}` to fetch the processed video

---

## ⚠️ Important Notes

* Make sure both FastAPI server and ngrok are running
* Wav2Lip is executed inside a separate virtual environment
* Video/audio files are handled locally and temporarily stored under `app/videos`

---

## 👨‍💻 Author

**Mohamed Magdy**
AI/ML Engineer — Deep Learning | NLP | MLOps
Graduation Project, Faculty of Computers & AI, 2025

🔗 GitHub Repo: [Arab Tutor](https://github.com/mohamedmagdy203/Arab_tutor_2025)

---
