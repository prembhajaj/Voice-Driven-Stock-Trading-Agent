from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Union

@dataclass
class STTChunkEvent:
    type: str
    transcript: str
    ts: float

    @classmethod
    def create(cls, transcript: str) -> "STTChunkEvent":
        return cls(type="stt_chunk", transcript=transcript, ts=time.time())

@dataclass
class STTOutputEvent:
    type: str
    transcript: str
    ts: float

    @classmethod
    def create(cls, transcript: str) -> "STTOutputEvent":
        return cls(type="stt_output", transcript=transcript, ts=time.time())

@dataclass
class AgentChunkEvent:
    type: str
    text: str
    ts: float

    @classmethod
    def create(cls, text: str) -> "AgentChunkEvent":
        return cls(type="agent_chunk", text=text, ts=time.time())

@dataclass
class TTSChunkEvent:
    type: str
    audio: bytes
    ts: float

    @classmethod
    def create(cls, audio: bytes) -> "TTSChunkEvent":
        return cls(type="tts_chunk", audio=audio, ts=time.time())

STTEvent = Union[STTChunkEvent, STTOutputEvent]
TTSEvent = TTSChunkEvent
VoiceAgentEvent = Union[STTChunkEvent, STTOutputEvent, AgentChunkEvent, TTSChunkEvent]
