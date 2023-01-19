import pygame
import sys
from pygame.mixer import Sound
import os
import threading

import loader
from gui.button import Button
from gui.text import Text
from gui.loadingbar import LoadingBar
import tkinter.filedialog

from platformer.level import Level
from platformer.player import Player

if __name__ == "__main__":
    os.environ["IMAGEIO_FFMPEG_EXE"] = os.path.join(os.getcwd(), "ffmpeg.com")

    import moviepy.editor as mp
    from videoPlayer.VideoPlayer import VideoPlayer
    from videoProcessor import process
    import threading

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400

    prevWd = os.getcwd()
    co = process.CleanOut()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Clowning Around")

    l = Level([], [Player(0, 0, 40, 40, True, 1, prevWd, SCREEN_WIDTH, SCREEN_HEIGHT),
                   Player(0, 0, 40, 40, True, 2, prevWd, SCREEN_WIDTH, SCREEN_HEIGHT)], prevWd,
              SCREEN_WIDTH, SCREEN_HEIGHT)
    v = VideoPlayer("", "", screen, l)
    p = process.Processor("", "")

    screenID = 0

    def assignScreenID(val):
        global screenID
        screenID = val

    def startLoadingVideo():
        assignScreenID(3)
        v.load()

    def startAnalyzingVideo():
        assignScreenID(7)
        t = threading.Thread(target=p.process, daemon=True)
        t.start()

    def assignPathOut(path):
        if path.split("/")[-1].split(".")[-1] != "mp4":
            path = f"{path}.mp4"
        p.setPathOut(path)

    def loadVideo(color, outline):
        v.setColor(color)
        v.setOutline(outline)
        startLoadingVideo()


    clock = pygame.time.Clock()
    channel = pygame.mixer.find_channel()
    channel.play(Sound(f"{prevWd}/resources/background/Clownfucker.mp3"), loops=-1)


    menuButtons = [Button(50, 200, 128, 128, image=loader.load_image(f"{prevWd}/resources/buttonImgs/playPreset.png"),
                          text=Text("Play Preset", ("Trebuchet", 25), (0, 0, 0), (100, 328)),
                          callback=lambda: assignScreenID(8)),
                   Button(236, 200, 128, 128, image=loader.load_image(f"{prevWd}/resources/buttonImgs/playCustom.png"),
                          text=Text("Play Custom", ("Trebuchet", 25), (0, 0, 0), (286, 328)),
                          callback=lambda: assignScreenID(2)),
                   Button(400, 200, 128, 128, image=loader.load_image(f"{prevWd}/resources/buttonImgs/analyze.png"),
                          text=Text("Generate Outline", ("Trebuchet", 25), (0, 0, 0), (430, 328)),
                          callback=lambda: assignScreenID(6))

                   ]

    loadButtons = [Button(30, 100, 220, 50, color=(255, 0, 0),
                          text=Text("Pick REGULAR video", ("Calibri",25), (255, 255, 255), (40, 115)),
                          callback=lambda: v.setColor(tkinter.filedialog.askopenfilename(filetypes=[("Color Video File", "*.mp4")]))),
                   Button(270, 100, 220, 50, color=(0, 0, 255),
                          text=Text("Pick OUTLINE video", ("Calibri",25), (255, 255, 255), (280, 115)),
                          callback=lambda: v.setOutline(tkinter.filedialog.askopenfilename(filetypes=[("Outline Video File", "*.mp4")])))]

    analyzeButtons = [Button(30, 140, 100, 50, color=(255, 0, 0),
                             text=Text("Pick Video", ("Calibri", 20), (255, 255, 255), (40, 155)),
                             callback=lambda:p.setPath(tkinter.filedialog.askopenfilename(filetypes=[("Video File", "*.mp4")]))),
                      Button(150, 140, 100, 50, color=(0, 0, 255),
                             text=Text("Save to", ("Calibri", 20), (255, 255, 255), (160, 155)),
                             callback=lambda: assignPathOut(tkinter.filedialog.asksaveasfilename(filetypes=[("Video File", ".mp4")])))]

    frameButtons = [Button(10, 270, 130, 50,
                           text=Text("Analyze EVERY \n"
                                     "Frame", ("Calibri", 15), (255, 255, 255), (20, 280)),
                           color=(255, 0, 0),
                           callback=lambda:p.assignFrameSkip(1)),
                    Button(160, 270, 130, 50,
                           text=Text("Analyze every \nother frame", ("Calibri", 15), (255, 255, 255), (170, 280)),
                           color=(0, 255, 0),
                           callback=lambda:p.assignFrameSkip(2)),
                    Button(310, 270, 130, 50,
                           text=Text("Analyze every \nthird frame", ("Calibri", 15), (255, 255, 255), (320, 280)),
                           color=(0, 0, 255),
                           callback=lambda:p.assignFrameSkip(3)),
                    Button(460, 270, 130, 50,
                           text=Text("Analyze every \n6th frame", ("Calibri", 15), (255, 255, 255), (470, 280)),
                           color=(255, 0, 255),
                           callback=lambda:p.assignFrameSkip(6))
                    ]

    levelButtons = [
        Button(225, 120, 150, 100,
               image=loader.load_image(f"{prevWd}/resources/levelThumbnail/SMB.png"),
               text=Text("Super Mario Bros Speedrun\n(Medium, 5:29", ("Calibri", 15), (0, 0, 0), (225, 220)),
               callback=lambda:loadVideo(f"{prevWd}/resources/levels/Super Mario Bros Speedrun.mp4",
                                         f"{prevWd}/resources/levels/SMB Speedrun Outline.mp4")),
        Button(225, 270, 150, 100,
               image=loader.load_image(f"{prevWd}/resources/levelThumbnail/Bad Apple.png"),
               text=Text("Bad Apple\n(Medium, 3:39)", ("Calibri", 15), (0, 0, 0), (275, 370)),
               callback=lambda: loadVideo(f"{prevWd}/resources/levels/Bad Apple.mp4",
                                          f"{prevWd}/resources/levels/Bad Apple Outline.mp4")
               ),
        Button(425, 120, 150, 100,
               image=loader.load_image(f"{prevWd}/resources/levelThumbnail/CSM.png"),
               text=Text("Chainsaw Man Opening\n(Hard, 1:30)", ("Calibri", 15), (0, 0, 0), (425, 220)),
               callback=lambda: loadVideo(f"{prevWd}/resources/levels/Chainsaw Man Opening.mp4",
                                          f"{prevWd}/resources/levels/CSM OP Outline.mp4")
               ),
        Button(25, 120, 150, 100,
               image=loader.load_image(f"{prevWd}/resources/levelThumbnail/Techno.png"),
               text=Text("Technoblade Tribute\n(Easy, 1:06)", ("Calibri", 15), (0, 0, 0), (25, 220)),
               callback=lambda: loadVideo(f"{prevWd}/resources/levels/Technoblade.mp4",
                                          f"{prevWd}/resources/levels/Technoblade Outline.mp4"))

    ]

    homeButton = Button(SCREEN_WIDTH-48-10, 10, 48, 48,
                        image=loader.load_image(f"{prevWd}/resources/buttonImgs/exit.png"),
                        callback=lambda: assignScreenID(1))
    loadCustomButton = Button(10, 220, 60, 30,
                              text=Text("Load", ("Calibri", 25), (255, 255, 255), (20, 227)),
                              color=(128, 0, 255),
                              callback=lambda: startLoadingVideo())
    playButton = Button(SCREEN_WIDTH-100, SCREEN_HEIGHT-60, 90, 50,
                        text=Text("Play!", ("Calibri", 45), (255, 255, 255), (SCREEN_WIDTH-95, SCREEN_HEIGHT-55)),
                        color=(0, 255, 255),
                        callback=lambda:assignScreenID(4))
    analyzeButton = Button(30, 330, 150, 65,
                           text=Text("Analyze", ("Calibri", 45), (255, 255, 255), (37, 340)),
                           color=(255, 0, 255),
                           callback=lambda: startAnalyzingVideo())

    def isValid(x):
        try:
            x = int(x)

        except ValueError:
            return False

        return x>0 and x<=12


    running = True


    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False


        screen.fill((0, 0, 0))
        clock.tick()

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        mouseClicked = pygame.mouse.get_pressed()[0]
        dt = clock.get_time()/1000

        if screenID == 0: # initial loading screen
            screen.blit(loader.load_image(f"{prevWd}/resources/background/title.png"), (0, 0))
            LoadingBar(SCREEN_WIDTH/2-200, SCREEN_HEIGHT-40, 400, 30, co.progress).render(screen)
            if co.done:
                screenID = 1
            # screenID = 1

        elif screenID == 1: # menu
            screen.blit(loader.load_image(f"{prevWd}/resources/background/title.png"), (0, 0))
            [button.render(screen) for button in menuButtons]
            [button.check(mouseX, mouseY, mouseClicked) for button in menuButtons]
            Text("Credits:\nCoding - Frank Liu\nArt - Matthew Fang\nBackground - Clownfucker\nJames Roach, Toby Fox",
                 ("Calibri", 10), (0, 0, 0), (SCREEN_WIDTH-105, 10)).render(screen)
            p.done = False
            v.resetPlayer()
            l.reset()

        elif screenID == 2: # load custom level
            homeButton.render(screen)
            homeButton.check(mouseX, mouseY, mouseClicked)
            [button.render(screen) for button in loadButtons]
            [button.check(mouseX, mouseY, mouseClicked) for button in loadButtons]
            Text("Load Custom Level", ("Calibri", 30), (255, 255, 255), (10, 10)).render(screen)
            Text("In order to play a custom level, you must need a REGULAR video (.mp4) and the OUTLINE video (.mp4).\n"
                 "You can generate the OUTLINE version by visiting 'Generate Outline' (on home screen)", ("Calibri", 13),
                 (255, 255, 255), (10, 50)).render(screen)

            colorText = v.color[-75:]
            if colorText != v.color:
                colorText = f"...{colorText}"
            outlineText = v.outline[-75:]
            if outlineText != v.outline:
                outlineText = f"...{outlineText}"

            Text(f"Regular: {colorText}", ("Calibri", 15), (255, 255, 255), (10, 160)).render(screen)
            Text(f"Outline: {outlineText}", ("Calibri", 15), (255, 255, 255), (10, 180)).render(screen)
            if (v.color != "" and v.outline != ""):
                loadCustomButton.render(screen)
                loadCustomButton.check(mouseX, mouseY, mouseClicked)

        elif screenID == 3:
            Text(f"Next up - {v.color.split('/')[-1]}", ("Calibri", 42), (255, 255, 255), (10, 10)).render(screen)
            LoadingBar(10, 50, 400, 30, v.progress/100).render(screen)
            if (all(v.ready)):
                playButton.render(screen)
                playButton.check(mouseX, mouseY, mouseClicked)
            Text("""
Player 1 Controls:
    -----
    W - Jump up/doublejump
    S - Burst Down
    A - Move to Left
    D - Move to Right
    E - Force
            
Player 2 Controls:
    -----
    I - Jump up/doublejump
    K - Burst Down
    J - Move to Left
    L - Move To Right
    O - Force
            """, ("Calibri", 15), (255, 255, 255), (10, 100)).render(screen)

            Text("""
    Objective:
    Don't touch the bottom of the map, earn points, and be the last survivor!
    
    The level will play the video faintly with the outline overlaid.
    Black pixels are safe ground, but make sure you don't lose your footing!
    
    You earn points based on powerups gained, your average altitude,
    if you survived or not, and whether your opponent survived.
    
    You can try and kill your opponent by using your Force ability,
    creating a force radiating from your player that pushes the other away.
    
    Powerups will periodically appear, giving you abilities like:
    * Saving Grace (if you hit the ground, you are slowly lifted up)
    * Double jump (Allows for a jump midair)
    * Bigger force (Bigger push force)
     """,("Calibri", 13), (255, 255, 255), (200, 100)).render(screen)

        elif screenID == 4: # game
            if v.frame < len(l.level):
                l.frame = v.frame
            if l.delay < 5:
                if v.firstFrame is None:
                    v.render_next_frame(dt)
                screen.blit(v.firstFrame, (0, 0))
                l.delay += dt
                l.preGame(dt, pygame.key.get_pressed())

            else:
                v.play_audio(channel)
                v.render_next_frame(dt)
                l.tick(pygame.key.get_pressed(), dt)

            l.render(screen)

            if (not v.playing):
                screenID = 5

        elif screenID == 5: # rating screen
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, SCREEN_WIDTH/2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, (100, 255, 100), pygame.Rect(SCREEN_WIDTH/2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT))
            l.renderResult(screen)
            homeButton.render(screen)
            homeButton.check(mouseX, mouseY, mouseClicked)

        elif screenID == 6: # outline prep
            Text("Create outline for Video", ("Calibri", 42), (255, 255, 255), (10, 10)).render(screen)
            Text("If you need an outline for a level, you can generate one here.\n"
                 "Supply an .mp4 file below, and choose how many frames (1-6) you want to take\n"
                 "1 means you take every frame, 2 means you take every 2, 6 means every 6, etc.\n"
                 "The higher the value, the faster generation will be, but the video will be stutter-y.",
                 ("Calibri", 15), (255, 255, 255), (10, 50)).render(screen)
            [button.render(screen) for button in analyzeButtons]
            [button.check(mouseX, mouseY, mouseClicked) for button in analyzeButtons]
            pathText = p.path[-75:]
            if pathText != p.path:
                pathText = f"...{pathText}"
            pathOutText = p.pathOut[-75:]
            if pathOutText != p.pathOut:
                pathOutText = f"...{pathOutText}"

            Text(f"Video: {pathText}", ("Calibri", 15), (255, 255, 255), (10, 210)).render(screen)
            Text(f"Save to: {pathOutText}", ("Calibri", 15), (255, 255, 255), (10, 230)).render(screen)
            homeButton.render(screen)
            homeButton.check(mouseX, mouseY, mouseClicked)
            Text(f"Take 1 in every {p.prep.frames} frames", ("Calibri", 15), (255, 255, 255), (10, 250)).render(screen)
            [button.render(screen) for button in frameButtons]
            [button.check(mouseX, mouseY, mouseClicked) for button in frameButtons]
            if (p.path != "" and p.pathOut != ""):
                analyzeButton.render(screen)
                analyzeButton.check(mouseX, mouseY, mouseClicked)

        elif screenID == 7: # outline gen
            Text(f"Analyzing {p.path.split('/')[-1]}...", ("Calibri", 42), (255, 255, 255), (10, 10)).render(screen)
            LoadingBar(10, 50, 300, 30, p.progress).render(screen)
            if p.done:
                Text("Finished!", ("Calibri", 40), (255, 255, 255), (10, 90)).render(screen)
                homeButton.render(screen)
                homeButton.check(mouseX, mouseY, mouseClicked)
            else:
                Text(f"no idea what the eta is, just check back eventually :)", ("Calibri", 15), (255, 255, 255), (10, 90)).render(screen)

        elif screenID == 8: # level select
            screen.blit(loader.load_image(f"{prevWd}/resources/background/title.png"), (0, 0))
            Text("Level Select", ("Calibri", 42), (0, 0, 0), (10, 10)).render(screen)
            homeButton.render(screen)
            homeButton.check(mouseX, mouseY, mouseClicked)
            [button.render(screen) for button in levelButtons]
            [button.check(mouseX, mouseY, mouseClicked) for button in levelButtons]

        pygame.display.flip()


    # set-executionpolicy RemoteSigned -Scope CurrentUser
