from moviepy.editor import VideoFileClip
from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
from deep_translator import GoogleTranslator
from torchaudio.transforms import Resample
from TTS.api import TTS
import torchaudio, torch, os, ffmpeg
from tempfile import NamedTemporaryFile

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
processor = WhisperProcessor.from_pretrained("openai/whisper-base")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)
translator = GoogleTranslator(source='en', target='ar')
tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')
tts.cuda()

def transcribe_video(video_path):
    temp_audio_path = NamedTemporaryFile(suffix=".mp3", delete=False).name
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(temp_audio_path)

    waveform, sample_rate = torchaudio.load(temp_audio_path)
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sample_rate != 16000:
        waveform = Resample(orig_freq=sample_rate, new_freq=16000)(waveform)

    input_features = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    summary = summarizer(transcription, max_length=500, min_length=70, do_sample=False)[0]['summary_text']
    translation = translator.translate(transcription)

    return translation, summary, transcription

def extract_speaker_audio(video_path, output_audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path)

def text_to_speech_xtts(text, speaker_audio_path, output_audio_path):
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    tts.tts_to_file(text=text, speaker_wav=speaker_audio_path, language="ar", file_path=output_audio_path)

def merge_audio_with_video(video_path, translated_audio, output_path):
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(translated_audio)
    #ffmpeg.output(input_video.video, input_audio, output_path, vcodec='copy', acodec='aac', strict='experimental').run(overwrite_output=True)
    ffmpeg.output(input_video.video, input_audio, output_path, vcodec='copy', acodec='aac', strict='experimental')\
    .run(cmd='ffmpeg', overwrite_output=True)

def process_video_with_translated_audio(video_path, output_video_path):
    speaker_audio_path = f"app/videos/speaker_{os.path.basename(video_path)}.mp3"
    xtts_audio_output = f"app/videos/xtts_output_{os.path.basename(video_path)}.wav"

    translated, summary, transcription = transcribe_video(video_path)
    extract_speaker_audio(video_path, speaker_audio_path)
    text_to_speech_xtts(translated, speaker_audio_path, xtts_audio_output)
    merge_audio_with_video(video_path, xtts_audio_output, output_video_path)

    return {
        "summary": summary,
        "output_path": output_video_path
    }
