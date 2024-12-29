# openai-realtime-webrtc-python

A Python library for real-time audio streaming with OpenAI's API using WebRTC protocol.

## Features

- Real-time audio streaming with OpenAI's API
- WebRTC-based communication
- Low-latency audio transmission
- Easy-to-use Python API
- Support for various audio formats and devices
- Automatic audio device management

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- aiortc
- sounddevice
- numpy
- websockets
- openai

## Quick Start

```python
from openai_realtime_webrtc import OpenAIWebRTCClient

async def main():
    client = OpenAIWebRTCClient(
        api_key="your-openai-api-key",
        model="whisper-1"
    )
    
    # Start streaming audio
    await client.start_streaming()
    
    # Stop streaming
    await client.stop_streaming()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Project Structure

```
openai-realtime-webrtc-python/
├── src/
│   └── openai_realtime_webrtc/
│       ├── __init__.py
│       ├── client.py
│       ├── audio_handler.py
│       └── webrtc_manager.py
├── examples/
│   └── basic_streaming.py
├── tests/
├── README.md
└── requirements.txt
```

## API Reference

### OpenAIWebRTCClient

The main client class for interacting with OpenAI's API using WebRTC.

```python
client = OpenAIWebRTCClient(
    api_key: str,                # Your OpenAI API key
    model: str = "whisper-1",    # OpenAI model to use
    sample_rate: int = 48000,    # Audio sample rate
    channels: int = 1,           # Number of audio channels
    frame_duration: int = 20     # Frame duration in milliseconds
)
```

#### Methods

- `start_streaming()`: Start audio streaming session
- `stop_streaming()`: Stop audio streaming session
- `pause_streaming()`: Pause audio streaming
- `resume_streaming()`: Resume audio streaming
- `set_audio_device(device_id: str)`: Set specific audio input device

## Examples

### Basic Streaming Example

```python
from openai_realtime_webrtc import OpenAIWebRTCClient

async def main():
    client = OpenAIWebRTCClient(api_key="your-openai-api-key")
    
    def on_transcription(text):
        print(f"Transcription: {text}")
    
    client.on_transcription = on_transcription
    await client.start_streaming()
    
    # Stream for 60 seconds
    await asyncio.sleep(60)
    await client.stop_streaming()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Changelog

### v0.1.0
- Initial release
- Basic WebRTC streaming functionality
- OpenAI API integration
- Real-time audio processing
