import asyncio
import numpy as np
import sounddevice as sd
from aiortc.mediastreams import MediaStreamTrack, MediaStreamError
from av import AudioFrame
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SAMPLE_RATE = 48000
CHANNELS = 1
DTYPE = np.int16

class AudioTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self, audio_handler):
        super().__init__()
        self._audio_handler = audio_handler
        self._queue = asyncio.Queue()
        self._task = None

    async def recv(self):
        if self._task is None:
            self._task = asyncio.create_task(self._audio_handler.start_recording(self._queue))

        try:
            frame = await self._queue.get()
            return frame
        except Exception as e:
            logger.error(f"Error receiving audio frame: {str(e)}")
            raise MediaStreamError("Failed to receive audio frame")

class AudioHandler:
    def __init__(self, sample_rate: int = SAMPLE_RATE, channels: int = CHANNELS, frame_duration: int = 20, dtype: np.dtype = DTYPE, input_device_index: Optional[int] = None, output_device_index: Optional[int] = None):
        self.sample_rate = sample_rate
        self.channels = channels
        self.frame_duration = frame_duration
        self.dtype = dtype
        self.input_device_index = input_device_index
        self.output_device_index = output_device_index
        self.frame_size = int(sample_rate * frame_duration / 1000)
        self.stream = None
        self.is_recording = False
        self.is_paused = False
        self._loop = None
        self._pts = 0

    def create_audio_track(self) -> AudioTrack:
        return AudioTrack(self)

    async def start_recording(self, queue: asyncio.Queue):
        if self.is_recording:
            return

        self.is_recording = True
        self.is_paused = False
        self._loop = asyncio.get_running_loop()
        self._pts = 0

        try:
            def callback(indata, frames, time, status):
                if status:
                    logger.warning(f"Audio input status: {status}")
                if not self.is_paused:
                    audio_data = indata.copy()
                    if audio_data.dtype != self.dtype:
                        audio_data = audio_data.astype(self.dtype)
                    frame = AudioFrame(samples=len(audio_data), layout='mono', format='s16')
                    frame.rate = self.sample_rate
                    frame.pts = self._pts
                    self._pts += len(audio_data)
                    frame.planes[0].update(audio_data.tobytes())
                    asyncio.run_coroutine_threadsafe(queue.put(frame), self._loop)

            self.stream = sd.InputStream(device=self.input_device_index, channels=self.channels, samplerate=self.sample_rate, dtype=self.dtype, blocksize=self.frame_size, callback=callback)
            self.stream.start()

            while self.is_recording:
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Error in audio recording: {str(e)}")
            raise
        finally:
            await self.stop()

    async def stop(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    async def pause(self):
        self.is_paused = True

    async def resume(self):
        self.is_paused = False

    def set_input_device(self, input_device_index: int):
        self.input_device_index = input_device_index
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def set_output_device(self, output_device_index: int):
        self.output_device_index = output_device_index
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
