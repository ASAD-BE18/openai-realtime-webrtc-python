import asyncio
import logging
from typing import Optional, Callable
import sounddevice as sd
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from .audio_handler import AudioHandler, SAMPLE_RATE, CHANNELS
from .audio_output import FRAME_DURATION_MS
from .webrtc_manager import WebRTCManager
from typing import Optional, Deque, Dict, Tuple

logger = logging.getLogger(__name__)
SYSTEM_MESSAGE = "You are a friendly assistant.",

def get_default_audio_info() -> Tuple[Dict, Dict]:
    try:
        input_device = sd.query_devices(kind='input')
        output_device = sd.query_devices(kind='output')

        logger.info("Default Input Device:")
        logger.info(f"  Name: {input_device['name']}")
        logger.info(f"  Channels: {input_device['max_input_channels']}")
        logger.info(f"  Sample Rate: {input_device['default_samplerate']}Hz")

        logger.info("Default Output Device:")
        logger.info(f"  Name: {output_device['name']}")
        logger.info(f"  Channels: {output_device['max_output_channels']}")
        logger.info(f"  Sample Rate: {output_device['default_samplerate']}Hz")

        return input_device, output_device
    except Exception as e:
        logger.error(f"Error getting audio device info: {str(e)}")
        raise



class OpenAIWebRTCClient:
    def __init__(
        self,
        api_key: str,
        model: str = "whisper-1",
        sample_rate: int = SAMPLE_RATE,
        channels: int = CHANNELS,
        frame_duration: int = FRAME_DURATION_MS,
        system_message: str = SYSTEM_MESSAGE,
    ):
        self.api_key = api_key
        self.model = model
        self.sample_rate = sample_rate
        self.channels = channels
        self.frame_duration = frame_duration
        self.system_message = system_message

        self.audio_handler = AudioHandler(
            sample_rate=sample_rate,
            channels=channels,
            frame_duration=frame_duration
        )
        self.webrtc_manager = WebRTCManager()

        self.peer_connection: Optional[RTCPeerConnection] = None
        self.is_streaming = False
        self.on_transcription: Optional[Callable[[str], None]] = None

    async def start_streaming(self):
        """Start the audio streaming session."""
        if self.is_streaming:
            logger.warning("Streaming is already active")
            return

        try:
            # Initialize WebRTC connection
            self.peer_connection = await self.webrtc_manager.create_connection()

            # Add audio track
            audio_track = self.audio_handler.create_audio_track()
            self.peer_connection.addTransceiver(audio_track, "sendrecv")

            # Create and set local description
            offer = await self.peer_connection.createOffer()
            await self.peer_connection.setLocalDescription(offer)

            # Connect to OpenAI's WebRTC endpoint
            response = await self.webrtc_manager.connect_to_openai(
                self.api_key,
                self.model,
                offer,
                self.system_message # pass system message prompt
            )

            # Set remote description
            answer = RTCSessionDescription(
                sdp=response["sdp"],
                type=response["type"]
            )
            await self.peer_connection.setRemoteDescription(answer)

            self.is_streaming = True
            logger.info("Streaming started successfully")

        except Exception as e:
            logger.error(f"Failed to start streaming: {str(e)}")
            await self.stop_streaming()
            raise

    async def stop_streaming(self):
        """Stop the audio streaming session."""
        if not self.is_streaming:
            return

        try:
            await self.webrtc_manager.cleanup()
            await self.audio_handler.stop()
            self.is_streaming = False
            logger.info("Streaming stopped successfully")

        except Exception as e:
            logger.error(f"Error while stopping streaming: {str(e)}")
            raise

    async def pause_streaming(self):
        """Pause the audio streaming."""
        if not self.is_streaming:
            return
        await self.audio_handler.pause()

    async def resume_streaming(self):
        """Resume the audio streaming."""
        if not self.is_streaming:
            return
        await self.audio_handler.resume()

    def set_audio_input_device(self, input_device_index: int):
        self.audio_handler.set_input_device(input_device_index)

    def set_audio_output_device(self, output_device_index: int):
        self.audio_handler.set_output_device(output_device_index)

    def _handle_transcription(self, text: str):
        """Handle incoming transcription."""
        if self.on_transcription:
            self.on_transcription(text)
