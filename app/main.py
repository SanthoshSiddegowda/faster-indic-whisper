from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from faster_whisper import WhisperModel
import tempfile
import os
import asyncio
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Bizom Whisper API", version="0.0.1")

# Optimized model configuration for CPU
# Using "tiny" model for faster processing, optimized for CPU
model = WhisperModel(
    "tiny",  # Smallest model for fastest CPU processing
    device="cpu",
    compute_type="int8",  # Best for CPU
    cpu_threads=os.cpu_count(),  # Use all CPU cores
    num_workers=1  # Single worker for CPU
)

class TranscriptionResponse(BaseModel):
    text: str
    processing_time: Optional[float] = None

class ErrorResponse(BaseModel):
    error: str
    detail: str

def cleanup_temp_file(file_path: str):
    """Clean up temporary file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {e}")

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Transcribe audio file with optimized CPU processing
    """
    import time
    start_time = time.time()
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload an audio file."
        )
    
    # Check file size (limit to 50MB for CPU processing)
    file_size = 0
    temp_file_path = None
    
    try:
        # Create temporary file with proper suffix
        suffix = os.path.splitext(file.filename)[1] if file.filename else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_file_path = tmp.name
            
            # Stream write to avoid memory issues
            chunk = await file.read(8192)  # 8KB chunks
            while chunk:
                file_size += len(chunk)
                if file_size > 50 * 1024 * 1024:  # 50MB limit
                    raise HTTPException(
                        status_code=413, 
                        detail="File too large. Maximum size is 50MB."
                    )
                tmp.write(chunk)
                chunk = await file.read(8192)
        
        # Transcribe with optimized settings
        logger.info(f"Starting transcription of {file.filename}")
        
        # Use optimized transcription settings for CPU
        segments, info = model.transcribe(
            temp_file_path,
            task="translate",  # Translate to English
            beam_size=1,  # Faster processing
            best_of=1,  # Reduce computation
            temperature=0,  # Deterministic output
            compression_ratio_threshold=2.4,
            log_prob_threshold=-1.0,
            no_speech_threshold=0.6,
            condition_on_previous_text=False,  # Faster processing
            initial_prompt=None,
            word_timestamps=False,  # Disable for speed
            prepend_punctuations=r'"\'¿([{-',
            append_punctuations=r'"\'.。,，!！?？:：")]}、'
        )
        
        # Process segments efficiently
        transcription_parts = []
        for segment in segments:
            if segment.text.strip():  # Only add non-empty segments
                transcription_parts.append(segment.text.strip())
        
        transcription = " ".join(transcription_parts)
        
        processing_time = time.time() - start_time
        logger.info(f"Transcription completed in {processing_time:.2f}s")
        
        return TranscriptionResponse(
            text=transcription,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file_path:
            if background_tasks:
                background_tasks.add_task(cleanup_temp_file, temp_file_path)
            else:
                cleanup_temp_file(temp_file_path)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "tiny", "device": "cpu"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Indic Whisper API",
        "version": "1.0.0",
        "model": "tiny",
        "device": "cpu",
        "endpoints": {
            "transcribe": "POST /transcribe",
            "health": "GET /health"
        }
    }
