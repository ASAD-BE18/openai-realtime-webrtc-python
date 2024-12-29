from setuptools import setup, find_packages

setup(
    name="openai-realtime-webrtc",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "sounddevice>=0.4.6",
        "numpy>=1.24.0",
        "websockets>=11.0.3",
        "openai>=1.3.0",
        "aiohttp>=3.8.5",
        "pyaudio>=0.2.13",
        "python-dotenv>=1.0.0",
        "aiortc>=1.6.0",
    ],
    python_requires=">=3.7",
)
