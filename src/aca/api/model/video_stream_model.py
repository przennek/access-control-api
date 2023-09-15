import cv2


class VideoCaptureContext:
    def __init__(self, source):
        self.source = source
        self.capture = None

    def __enter__(self):
        self.capture = cv2.VideoCapture(self.source)
        return self.capture

    def __exit__(self, exc_type, exc_value, traceback):
        if self.capture is not None:
            self.capture.release()


class VideoStreamModel:

    def generate(self):
        with VideoCaptureContext(0) as vc:
            while True:
                _, frame = vc.read()
                path = '/tmp/frame.jpg'
                cv2.imwrite(path, frame)
                frame = open(path, 'rb').read()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
