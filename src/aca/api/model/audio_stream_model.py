import logging

import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8
BITS_PER_SAMPLE = 16
INPUT_DEVICE_INDEX = 1

logger = logging.getLogger(__name__)


class PyAudioContext:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def __enter__(self):
        return self.audio

    def __exit__(self, exc_type, exc_value, traceback):
        self.audio.terminate()


class PyStreamContext:
    def __init__(self, fmat, channels, rate, input_device_index, frames_per_buffer):
        self.format = fmat
        self.channels = channels
        self.rate = rate
        self.input_device_index = input_device_index
        self.frames_per_buffer = frames_per_buffer
        self.stream = None

    def __enter__(self):
        self.stream = pyaudio.PyAudio().open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=self.input_device_index,
            frames_per_buffer=self.frames_per_buffer
        )
        return self.stream

    def __exit__(self, exc_type, exc_value, traceback):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()


class AudioStreamModel:

    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def generate(self):
        with PyAudioContext() as audio:
            logger.info("Device info:")
            for i in range(audio.get_device_count()):
                info = audio.get_device_info_by_index(i)
                logger.info(
                    f"Device {i}: {info['name']},"
                    f" Channels: {info['maxInputChannels']},"
                    f" Rate: {info['defaultSampleRate']}"
                )

            wav_header = self.gen_header(RATE, BITS_PER_SAMPLE, CHANNELS)

            with PyStreamContext(FORMAT, CHANNELS, RATE, INPUT_DEVICE_INDEX, CHUNK) as stream:
                first_run = True
                while True:
                    stream_read = stream.read(CHUNK, exception_on_overflow=False)
                    if first_run:
                        data = wav_header + stream_read
                        first_run = False
                    else:
                        data = stream_read
                    yield data

    @staticmethod
    def gen_header(sample_rate, bits_per_sample, channels):
        datasize = 2000 * 10 ** 6
        o = bytes("RIFF", 'ascii')  # (4byte) Marks file as RIFF
        o += (datasize + 36).to_bytes(4, 'little')
        o += bytes("WAVE", 'ascii')  # (4byte) File type
        o += bytes("fmt ", 'ascii')  # (4byte) Format Chunk Marker
        o += (16).to_bytes(4, 'little')  # (4byte) Length of above format data
        o += (1).to_bytes(2, 'little')  # (2byte) Format type (1 - PCM)
        o += channels.to_bytes(2, 'little')  # (2byte)
        o += sample_rate.to_bytes(4, 'little')  # (4byte)
        o += (sample_rate * channels * bits_per_sample // 8).to_bytes(4, 'little')  # (4byte)
        o += (channels * bits_per_sample // 8).to_bytes(2, 'little')  # (2byte)
        o += bits_per_sample.to_bytes(2, 'little')  # (2byte)
        o += bytes("data", 'ascii')  # (4byte) Data Chunk Marker
        o += datasize.to_bytes(4, 'little')  # (4byte) Data size in bytes
        return o
