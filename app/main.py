from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from faster_whisper import WhisperModel
import tempfile
import os

app = FastAPI()

# Load Whisper model once at startup (use "small" or "tiny" for faster CPU)
model = WhisperModel("small", device="cpu", compute_type="int8")

class TranscriptionResponse(BaseModel):
    text: str

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Transcribe audio file with translation to English
        segments, _ = model.transcribe(tmp_path, task="translate")
        transcription = " ".join(segment.text for segment in segments)
    finally:
        os.remove(tmp_path)

    return TranscriptionResponse(text=transcription)
