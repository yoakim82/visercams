

class DummyCam:
    def __init__(self):

        self.cam = "a camera"

    def start_recording(self, encoder, output):
        pass

    def stop_recording(self):
        pass


class FfmpegOutput:
    def __init__(self, output):
        self.output = output


class DummyEnc:
    def __init__(self):

        self.enc = "an encoder"

