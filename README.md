# Faster-Indic Whisper

A FastAPI-based backend for real-time speech-to-text transcription using OpenAI's Whisper model. Designed for integration with mobile apps, supporting scalable, real-time audio streaming and transcription.

---

## Features
- Real-time audio transcription via HTTP or WebSocket (recommended for real-time)
- Supports chunked audio streaming from mobile clients
- Scalable architecture: stateless API, task queue, worker pool
- Works with CPU or GPU (GPU recommended for high throughput)
- Partial and final transcription results

---

## Architecture Overview

```
Mobile App <-> FastAPI (WebSocket/API) <-> Task Queue <-> Whisper Worker(s) <-> Result Store
```

- **Mobile App:** Streams audio chunks via WebSocket
- **FastAPI:** Handles connections, manages sessions, enqueues jobs
- **Task Queue:** (e.g., Redis, RabbitMQ) Buffers jobs for workers
- **Whisper Worker(s):** Run Whisper inference (CPU or GPU)
- **Result Store:** (e.g., Redis) Stores session state and results

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/SanthoshSiddegowda/faster-whisper
cd indic-whisper
```

### 2. Install dependencies
```bash
python -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the FastAPI server
```bash
uvicorn app.main:app --reload
```

---

## Usage

### HTTP API (Simple Transcription)
- `POST /transcribe` with an audio file (WAV, MP3, etc.)
- Returns the transcribed text

### WebSocket API (Recommended for Real-Time)
- (To be implemented) Connect via WebSocket, stream audio chunks, receive partial transcriptions

---

## Scalability Notes
- For production, use a task queue and worker pool for inference
- Deploy multiple FastAPI instances behind a load balancer
- Use Redis or similar for session and result storage
- Monitor CPU/GPU usage and autoscale workers as needed

---

## License
MIT 
