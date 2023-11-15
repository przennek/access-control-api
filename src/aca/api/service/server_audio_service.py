import logging
import os
import subprocess

logger = logging.getLogger(__name__)


class ServerAudioService:

    @staticmethod
    def play(path: str, blocking=True):
        full_path = os.path.join(os.getcwd(), path)

        if blocking:
            subprocess.call(["aplay", "-D", "hw:1,0", "-c", "2", "-f", "S16_LE", full_path])
        else:
            subprocess.Popen(["aplay", "-D", "hw:1,0", "-c", "2", "-f", "S16_LE", full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
