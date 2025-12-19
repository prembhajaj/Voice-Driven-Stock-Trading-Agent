from fastapi import FastAPI, WebSocket
from langchain_core.runnables import RunnableGenerator

from agent import agent_stream
from stt import stt_stream
from tts import tts_stream

app = FastAPI()

pipeline = (
    RunnableGenerator(stt_stream)      # Audio -> STT events
    | RunnableGenerator(agent_stream)  # STT events -> Agent events
    | RunnableGenerator(tts_stream)    # Agent events -> TTS audio
)

# Use in WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def websocket_audio_stream():
        """Yield audio bytes from WebSocket."""
        while True:
            data = await websocket.receive_bytes()
            yield data

    # Transform audio through pipeline
    output_stream = pipeline.atransform(websocket_audio_stream())

    # Send TTS audio back to client
    async for event in output_stream:
        if event.type == "tts_chunk":
            await websocket.send_bytes(event.audio)
