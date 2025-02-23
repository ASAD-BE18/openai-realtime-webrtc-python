# openai-realtime-webrtc-python

A Python library for real-time audio streaming communication based on WebRTC, supporting real-time audio interaction with the OpenAI Realtime API.

## Features

- Real-time audio communication based on WebRTC
- Support for OpenAI Realtime API
- Automatic audio device management
- Automatic sampling rate conversion
- Low-latency audio transmission
- Audio buffer management
- Support for pausing/resuming streaming

## Installation Requirements

- Python 3.7+
- Supported operating systems: Windows, macOS, Linux
- Audio device support

### Dependencies

```bash
sounddevice>=0.4.6
numpy>=1.24.0
websockets>=11.0.3
openai>=1.3.0
aiohttp>=3.8.5
pyaudio>=0.2.13
python-dotenv>=1.0.0
aiortc>=1.6.0
scipy>=1.12.0
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/openai-realtime-webrtc-python.git
cd openai-realtime-webrtc-python
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install in development mode:
```bash
pip install -e .
```

## Usage

1. Set environment variables:
Create a `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=your-api-key-here
```

2. Basic usage example:
```python
import asyncio
from openai_realtime_webrtc import OpenAIWebRTCClient

async def main():
    # Create client instance
    client = OpenAIWebRTCClient(
        api_key="your-api-key",
        model="gpt-4o-realtime-preview-2024-12-17"
    )

    # Define transcription callback
    def on_transcription(text: str):
        print(f"Transcription: {text}")

    client.on_transcription = on_transcription

    try:
        # Start streaming
        await client.start_streaming()
        
        # Keep connection alive
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        # Stop streaming
        await client.stop_streaming()

if __name__ == "__main__":
    asyncio.run(main())
```

3. Run the example:
```bash
python examples/basic_streaming.py
```

## Contribution Guidelines

Pull Requests and Issues are welcome!

## License

MIT License

## Changelog

### v0.1.0
- Initial release
- Basic WebRTC audio streaming functionality
- Support for OpenAI Realtime API
- Automatic audio device management
- Audio resampling support
