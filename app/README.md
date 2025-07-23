# FastAPI App for Indic Whisper

This directory contains the FastAPI application for the Indic Whisper backend.

## Endpoints

### POST `/transcribe`
- Accepts: Audio file upload (WAV, MP3, etc.)
- Returns: Transcribed text (in English)
- Validates file type and resamples audio to 16kHz if needed

## Development Notes
- Uses HuggingFace Transformers Whisper model
- Uses Torchaudio for audio processing
- Pydantic models for request/response validation
- See main.py for implementation details

## To Run
```bash
uvicorn app.main:app --reload
``` 