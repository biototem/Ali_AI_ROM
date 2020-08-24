import av
import numpy as np


class VideoWriter:
    def __init__(self, file, format='webm', codec='vp8', width=1280, height=720, fps=30, pix_fmt='yuv420p'):
        self.container = av.open(file, mode='w', format=format)
        self.stream = self.container.add_stream(codec, rate=fps)
        self.stream.pix_fmt = pix_fmt
        self.stream.width = width
        self.stream.height = height

    def push_data(self, im: np):
        assert im.shape == (self.stream.height, self.stream.width, 3)
        frame = av.VideoFrame.from_ndarray(im, format='rgb24')
        for packet in self.stream.encode(frame):
            self.container.mux(packet)

    def close(self):
        for packet in self.stream.encode():
            self.container.mux(packet)
        self.container.close()
        del self.container
        del self.stream


class VideoReader:
    def __init__(self, file):
        self.container = av.open(file, mode='r')
        self.stream = self.container.streams.video[0]
        self.pix_fmt = self.stream.pix_fmt
        self.width = self.stream.width
        self.height = self.stream.height
        self.fps = float(self.stream.average_rate)

    def next_data_gen(self):
        for vf in self.container.decode(video=0):
            yield vf.to_rgb().to_ndarray()

    def close(self):
        self.container.close()
        del self.container
        del self.stream
