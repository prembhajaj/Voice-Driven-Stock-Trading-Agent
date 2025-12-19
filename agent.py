from typing import AsyncIterator
from uuid import uuid4
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from events import AgentChunkEvent, VoiceAgentEvent

# Define agent tools
def get_stock_price(symbol: str) -> str:
    """Return a simulated stock price for a symbol."""
    return f"{symbol.upper()} is trading at $123.45."

def buy_stock(symbol: str, quantity: int) -> str:
    """Buy a stock (simulated)."""
    return f"Placed order: buy {quantity} shares of {symbol.upper()}."

def sell_stock(symbol: str, quantity: int) -> str:
    """Sell a stock (simulated)."""
    return f"Placed order: sell {quantity} shares of {symbol.upper()}."

# Create agent with tools and memory
agent = create_react_agent(
    model="google_genai:gemini-2.5-flash-lite",  # Select your model
    tools=[get_stock_price, buy_stock, sell_stock],
    prompt="""You are a helpful stock trading assistant.
    Your goal is to help the user check prices and place simulated buy or sell orders.
    Be concise and friendly.
    Do NOT use emojis, special characters, or markdown.
    Your responses will be read by a text-to-speech engine.""",
    checkpointer=InMemorySaver(),
)

async def agent_stream(
    event_stream: AsyncIterator[VoiceAgentEvent],
) -> AsyncIterator[VoiceAgentEvent]:
    """
    Transform stream: Voice Events -> Voice Events (with Agent Responses)

    Passes through all upstream events and adds agent_chunk events
    when processing STT transcripts.
    """
    # Generate unique thread ID for conversation memory
    thread_id = str(uuid4())

    async for event in event_stream:
        # Pass through all upstream events
        yield event

        # Process final transcripts through the agent
        if event.type == "stt_output":
            # Stream agent response with conversation context
            stream = agent.astream(
                {"messages": [HumanMessage(content=event.transcript)]},
                {"configurable": {"thread_id": thread_id}},
                stream_mode="messages",
            )

            # Yield agent response chunks as they arrive
            async for message, _ in stream:
                if message.text:
                    yield AgentChunkEvent.create(message.text)
