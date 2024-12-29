import asyncio
import os
import logging
from dotenv import load_dotenv
from openai_realtime_webrtc import OpenAIWebRTCClient
from openai_realtime_webrtc.audio_handler import SAMPLE_RATE, CHANNELS, DTYPE

# 设置日志级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


async def main():
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENAI_API_KEY environment variable")

    print(f"Audio Configuration:")
    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print(f"Channels: {CHANNELS} (Mono)")
    print(f"Bit Depth: {DTYPE} (16-bit)")

    # Create client instance
    client = OpenAIWebRTCClient(
        api_key=api_key,
        model="gpt-4o-realtime-preview-2024-12-17",
        sample_rate=SAMPLE_RATE,
        channels=CHANNELS,
        frame_duration=20
    )

    # Define transcription callback
    def on_transcription(text: str):
        print(f"Transcription: {text}")

    client.on_transcription = on_transcription

    try:
        # Start streaming
        print("Starting audio streaming... Press Ctrl+C to stop")
        await client.start_streaming()

        # Keep the connection alive
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping streaming...")
    except Exception as e:
        logger.error(f"Error during streaming: {str(e)}")
    finally:
        # Clean up
        await client.stop_streaming()

if __name__ == "__main__":
    asyncio.run(main())
