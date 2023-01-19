import os
import threading
import cv2
import pygame
from pygame.mixer import Sound

from videoProcessor import process
import moviepy.editor as mp

class VideoPlayer:
    def __init__(self, color, outline, screen, level):
        self.color = color
        self.outline = outline
        self.screen = screen
        self.colorFPS = 0
        self.outlineFPS = 0
        self.prep = process.Preprocessor(300, 200, 1)
        self.level = level
        self.firstFrame = None
        self.playingAudio = False
        self.resetPlayer()

    def resetPlayer(self):
        self.frame = 0
        self.dt = 0
        self.ready = [False, False]
        self.progress = 0
        self.playing = False
        self.playingAudio = False

    def setColor(self, color):
        self.color = color

    def setOutline(self, outline):
        self.outline = outline

    def load(self):
        t = threading.Thread(target=self.load_images, daemon=True)
        t.start()
        t2 = threading.Thread(target=self.load_sound, daemon=True)
        t2.start()


    def load_sound(self):
        video = mp.VideoFileClip(self.color)
        name = self.color.split("/")[-1]
        video.audio.write_audiofile(os.path.join("out", f"{name}.mp3"))
        self.ready[0] = True

    def play_audio(self, channel):
        if (not self.playingAudio):
            name = self.color.split("/")[-1]
            channel.play(Sound(os.path.join("out", f"{name}.mp3")))

        self.playingAudio = True


    def load_images(self):
        vidcap = cv2.VideoCapture(self.color)
        vidcap2 = cv2.VideoCapture(self.outline)
        success, image = vidcap.read()
        count = 0

        name = self.color.split("/")[-1]
        self.colorFPS = vidcap.get(cv2.CAP_PROP_FPS)
        first = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        total = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) + int(vidcap2.get(cv2.CAP_PROP_FRAME_COUNT))

        while success:
            success, image = vidcap.read()
            if success:
                cv2.imwrite(f"out/frame_{name}_{round(count / self.prep.frames)}.jpg", self.prep.resize(image))
            count += 1
            self.progress = count/(total)*100

        vidcap = cv2.VideoCapture(self.outline)
        success, image = vidcap.read()
        count = 0
        name = self.outline.split("/")[-1]
        self.outlineFPS = vidcap.get(cv2.CAP_PROP_FPS)

        while success:
            success, image = vidcap.read()
            if success:
                cv2.imwrite(f"out/frame_{name}_{round(count / self.prep.frames)}.jpg", self.prep.resize(image))
                self.level.load(f"out/frame_{name}_{round(count / self.prep.frames)}.jpg")
            count += 1
            self.progress = (count+first)/(total) * 100

        self.ready[1] = True

    def frame_exists(self, frame):
        return os.path.exists(frame)

    def render_next_frame(self, time):
        name = self.color.split("/")[-1]
        outlineName = self.outline.split("/")[-1]
        divisor = round(self.colorFPS/self.outlineFPS)
        renderFrame = f"frame_{name}_{(self.frame//divisor+1) * divisor}.jpg"
        rOutlineFrame = f"frame_{outlineName}_{self.frame//divisor}.jpg"

        done = True

        if self.frame_exists(f"out/{rOutlineFrame}"):
            img = pygame.image.load(f"out/{rOutlineFrame}").convert_alpha()
            img = pygame.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(img, (0, 0))
            done = False

        if self.frame == 0:
            self.firstFrame = img

        if self.frame_exists(f"out/{renderFrame}"):
            img = pygame.image.load(f"out/{renderFrame}").convert_alpha()
            img = pygame.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))
            img.fill((255, 255, 255, 160), None, pygame.BLEND_RGBA_MULT)
            self.screen.blit(img, (0, 0))
            done = False



        self.playing = not done
        self.dt += time
        self.frame += round(self.dt//(1/self.colorFPS))
        self.dt %= 1/self.colorFPS
