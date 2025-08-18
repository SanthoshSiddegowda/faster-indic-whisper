# Performance Optimization Guide

## CPU Optimizations Applied

### 1. Model Configuration
- **Model Size**: Using "tiny" model (39MB) instead of "small" (244MB) for faster processing
- **CPU Threads**: Utilizing all available CPU cores with `cpu_threads=os.cpu_count()`
- **Compute Type**: Using `int8` quantization for optimal CPU performance
- **Single Worker**: Using `num_workers=1` for CPU tasks

### 2. Transcription Settings
- **Beam Size**: Set to 1 for faster processing
- **Best Of**: Set to 1 to reduce computation
- **Temperature**: Set to 0.0 for deterministic output
- **Word Timestamps**: Disabled for speed
- **Condition on Previous Text**: Disabled for faster processing

### 3. File Handling
- **Streaming**: 8KB chunk processing to avoid memory issues
- **File Size Limit**: 50MB maximum for CPU processing
- **Background Cleanup**: Temporary files cleaned up in background tasks
- **Proper File Extensions**: Preserves original file extensions

### 4. Server Configuration
- **Single Worker**: Optimal for CPU-intensive tasks
- **HTTP Tools**: Using httptools for faster HTTP parsing
- **Concurrency Limits**: 10 concurrent requests maximum
- **Request Limits**: Worker restart after 1000 requests

## Performance Benchmarks

### Expected Performance (CPU-only):
- **Tiny Model**: ~2-5x faster than small model
- **Processing Time**: 30-60 seconds for 1-minute audio
- **Memory Usage**: ~500MB RAM
- **CPU Usage**: 100% during transcription

### Optimization Tips:

1. **Audio Format**: Use WAV or MP3 for best performance
2. **File Size**: Keep files under 50MB for optimal processing
3. **Server Resources**: Ensure adequate CPU cores available
4. **Monitoring**: Use `/health` endpoint to check system status

## Running the Optimized Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run with optimized settings
python run_server.py

# Or with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --http httptools
```

## API Endpoints

- `POST /transcribe` - Transcribe audio file
- `GET /health` - Health check
- `GET /` - API information

## Response Format

```json
{
  "text": "Transcribed text in English",
  "processing_time": 45.23
}
```

## Error Handling

- File size validation (50MB limit)
- Audio format validation
- Proper error responses with status codes
- Logging for debugging

## Monitoring

The application includes:
- Processing time tracking
- File cleanup logging
- Error logging
- Health check endpoint 