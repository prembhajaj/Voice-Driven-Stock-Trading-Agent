# Voice-Driven Stock Trading Agent

Voice-Driven Stock Trading Agent is a demo voice assistant that lets users ask
for stock prices and place simulated buy or sell orders using speech. It
showcases a streaming voice pipeline (STT -> agent -> TTS) with LangChain,
AssemblyAI, and Cartesia.


## Setup

1. Create a virtual environment and install dependencies:

   python -m venv .venv

   .venv\Scripts\activate
   
   pip install -r requirements.txt

2. Set API keys (example names used by the code):

   setx ASSEMBLYAI_API_KEY "your_key"
   
   setx CARTESIA_API_KEY "your_key"
   
   setx GOOGLE_API_KEY "your_key"


3. Run the server:

   uvicorn app:app --reload

## Notes

- The server exposes a WebSocket endpoint at /ws that expects PCM audio frames.
- This is a direct copy of the doc snippets plus minimal glue for a runnable layout.
