"""
OpenAI Realtime WebRTC Python Client

A Python library for real-time audio streaming with OpenAI's API using WebRTC protocol.
"""

import logging

from .client import OpenAIWebRTCClient
from .audio_handler import AudioHandler
from .webrtc_manager import WebRTCManager

__version__ = "0.1.0"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

__all__ = ['OpenAIWebRTCClient', 'AudioHandler', 'WebRTCManager']
