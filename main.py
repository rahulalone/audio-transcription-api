from fastapi import FastAPI, UploadFile, File, Request
from fastapi.concurrency import run_in_threadpool
from faster_whisper import WhisperModel
from database import database, logs, create_tables
import os
import time

app = FastAPI()

model = WhisperModel("small")

def transcribe():
    seg, info = model.transcribe("temp_audio.wav")
    text = "".join([i.text for i in seg])
    return text, info.language, round(info.duration, 2)

# DB connect on startup, disconnect on shutdown
@app.on_event("startup")
async def startup():
    create_tables()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/audio_to_text")
async def audio_to_text(request: Request, file: UploadFile = File(...)):
    content     = await file.read()
    file_size   = round(len(content) / 1024, 2)   # KB
    client_ip   = request.client.host

    with open("temp_audio.wav", "wb") as f:
        f.write(content)

    text = language = None
    audio_duration = processing_time = None
    status = "failed"
    error_message = None

    try:
        start_time = time.time()
        text, language, audio_duration = await run_in_threadpool(transcribe)
        processing_time = round(time.time() - start_time, 2)
        status = "success"
    except Exception as e:
        error_message = str(e)
    finally:
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

    # Save log to PostgreSQL
    query = logs.insert().values(
        file_name          = file.filename,
        file_size_kb       = file_size,
        transcription      = text,
        word_count         = len(text.split()) if text else 0,
        language           = language,
        audio_duration_sec = audio_duration,
        processing_time_sec= processing_time,
        client_ip          = client_ip,
        status             = status,
        error_message      = error_message,
    )
    await database.execute(query)

    return {
        "transcription"      : text,
        "language"           : language,
        "word_count"         : len(text.split()) if text else 0,
        "audio_duration_sec" : audio_duration,
        "processing_time_sec": processing_time,
        "file_size_kb"       : file_size,
        "status"             : status,
    }

@app.get("/h")
async def say():
    return "Hello World my name is rahul"

@app.get("/logs")
async def get_logs():
    query = logs.select().order_by(logs.c.created_at.desc())
    return await database.fetch_all(query)
