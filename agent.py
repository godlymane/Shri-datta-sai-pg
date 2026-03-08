import asyncio
import os
import sys

from livekit.agents import AutoSubscribe, JobContext, JobProcess, WorkerOptions, cli, llm
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import openai, silero, deepgram

# Set your API keys as environment variables before running:
# export LIVEKIT_URL="wss://your-livekit-server"
# export LIVEKIT_API_KEY="your-api-key"
# export LIVEKIT_API_SECRET="your-api-secret"
# export OPENAI_API_KEY="your-openai-api-key"

async def entrypoint(ctx: JobContext):
    # Setup the prompt that defines the AI's personality and knowledge
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a friendly, helpful, and professional receptionist for Shri Datta Sai PG, "
            "a premium paying guest accommodation for girls and boys in Hinjawadi, Pune. "
            "Your job is to answer phone calls from potential residents and their parents. "
            "Keep your answers short, conversational, and direct. "
            "If someone asks for pricing: Single occupancy is ₹14,000/month, Double sharing is ₹8,000/month. "
            "Security deposit is ₹3,000 (with ₹1,000 deducted as one-time maintenance). "
            "Lock-in period is 30 days. "
            "Amenities include 3 home-cooked meals daily, high-speed WiFi, 24/7 CCTV, washing machine, "
            "fridge, self-cooking gas, hot water, power backup, parking, daily cleaning, and an elevator on all floors. "
            "If they want to visit or book, tell them they can visit anytime during the day or message us on WhatsApp at +91 78756 68666. "
            "If they ask something you don't know, apologize and tell them to contact the owner directly on WhatsApp."
        ),
    )

    # Initialize the voice pipeline
    agent = VoicePipelineAgent(
        vad=silero.VAD.load(), # Voice Activity Detection (detects when user speaks/stops)
        stt=deepgram.STT(), # Speech-to-Text (converts caller's audio to text)
        llm=openai.LLM(), # The "Brain" (processes text and generates response)
        tts=openai.TTS(), # Text-to-Speech (converts AI's text back to audio)
        chat_ctx=initial_ctx,
    )

    # Connect to the room (the phone call)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Start the agent
    agent.start(ctx.room)

    # Greet the caller
    await agent.say("Hello! You've reached Shri Datta Sai PG in Hinjawadi. How can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))