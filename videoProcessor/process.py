import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing.context import Process

import time
from PIL import Image
import threading
from videoProcessor.preprocess import Preprocessor
import cv2
import os

class CleanOut:
    def __init__(self):
        self.done = False
        self.progress = 0
        t = threading.Thread(target=self.clean_out, daemon=True)
        t.start()

    def clean_out(self):
        prevwd = os.getcwd()
        os.chdir("out/")
        notdone = os.listdir(os.getcwd())
        total = len(notdone)
        count = 0
        while len(notdone) > 0:
            for index, file in enumerate(notdone):
                try:
                    os.remove(file)
                    count += 1
                    self.progress = count/total

                except (PermissionError, FileNotFoundError) as e:
                    pass
            notdone = os.listdir(os.getcwd())

        os.chdir(prevwd)
        time.sleep(1)
        self.done = True

class Processor:
    def __init__(self, path, pathOut):
        self.path = path
        self.pathOut = pathOut
        self.progress = 0
        self.done = False
        self.progressCount = 0
        self.threadsDone = 0
        self.prep = Preprocessor(300, 200, 6)
        self.total = 0

    def setPath(self, path):
        self.path = path

    def setPathOut(self, path):
        self.pathOut = path

    def assignFrameSkip(self, skip):
        self.prep.frames = skip

    def processFrame(self, i):
        prep = self.prep
        with Image.open(f"out/frame{i}.jpg") as f:
            im = prep.detectOutline(f)
            im.save(f"out/analyzed{i}.jpg")
            self.progressCount += int(prep.height * prep.width / 30)
            self.progress = self.progressCount/self.total
            self.threadsDone += 1

    def process(self):
        self.process_video(self.path, self.pathOut)


    def process_video(self, path, pathOut):
        vidcap = cv2.VideoCapture(path)
        len = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        success, image = vidcap.read()
        count = 0

        prep = self.prep

        frames = 0

        self.total = len + int(len/prep.frames + len/prep.frames * int(prep.height * prep.width / 30))
        self.progressCount = 0

        while success:
            success, image = vidcap.read()
            if (count % prep.frames == 0):
                if success:
                    cv2.imwrite(f"out/frame{round(count / prep.frames)}.jpg", prep.resize(image))
                    frames += 1
            count += 1
            self.progressCount += 1
            self.progress = self.progressCount/self.total

        self.threadsDone = 0
        multiprocessing.set_start_method("spawn")
        executor = ThreadPoolExecutor(max_workers=25)
        executor.map(self.processFrame, range(frames))

        # for i in range(frames):
        #     self.processFrame(i)

        while self.threadsDone != frames:
            pass

        video = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*"avc1"),
                                round(vidcap.get(cv2.CAP_PROP_FPS) / prep.frames), (300, 200))
        for i in range(frames):
            video.write(cv2.imread(f"out/analyzed{i}.jpg"))
            self.progressCount += 1
            self.progress = min(self.progressCount / self.total, 1)

        cv2.destroyAllWindows()
        video.release()
        self.done = True