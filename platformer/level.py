import math
import random

import numpy
import pygame
from PIL import Image

import loader
from gui.text import Text

class Powerup:
    def __init__(self, type, x, y, w, h, wD, timeAlive):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
        self.wD = wD
        self.timeLeft = timeAlive
        self.originalTime = timeAlive

    def render(self, screen):
        if self.type == 0:
            img = loader.load_image(f"{self.wD}/resources/sprites/balloon_save.png")

        elif self.type == 1:
            img = loader.load_image(f"{self.wD}/resources/sprites/double_jump.png")

        else:
            img = loader.load_image(f"{self.wD}/resources/sprites/force_field_icon.png")

        img = pygame.transform.scale(img, (self.w + math.sin(self.timeLeft) * self.w/2, self.h + math.sin(self.timeLeft) * self.w/2))
        screen.blit(img, (self.x, self.y))

    def tick(self, dt):
        self.timeLeft -= dt


class Level:
    def __init__(self, level, players, workingDir, screenW, screenH):
        self.level = level
        self.players = players
        self.frame = 0
        self.workingDir = workingDir
        self.screenW = screenW
        self.screenH = screenH
        self.powerups = []
        self.timeUntilNextPowerup = random.randint(1, 10)
        self.timeSinceLastPowerup = 0

        self.delay = 0

    def reset(self):
        self.frame = 0
        [player.reset() for player in self.players]
        self.level = []
        self.powerups = []
        self.timeUntilNextPowerup = random.randint(1, 10)
        self.timeSinceLastPowerup = 0

    def load(self, path):
        with Image.open(path) as f:
            array = numpy.array(f)
            self.level.append(array)


    def tick(self, keys, dt):
        self.timeSinceLastPowerup += dt
        if self.timeSinceLastPowerup > self.timeUntilNextPowerup:
            self.timeUntilNextPowerup = random.randint(1, 10)
            self.timeSinceLastPowerup = 0
            self.powerups.append(Powerup(random.randint(0, 2), random.randint(0, self.screenW), random.randint(0, self.screenH),
                                         40, 40, self.workingDir, random.randint(3, 6)))

        [powerup.tick(dt) for powerup in self.powerups]
        self.powerups = [powerup for powerup in self.powerups if powerup.timeLeft > 0]
        goodPowerups = []
        for powerup in self.powerups:
            good = True
            for player in self.players:
                if not (powerup.x > player.x + player.w or powerup.x + powerup.w < player.x or
                        powerup.y > player.y + player.h or powerup.y + powerup.h < player.y):
                    good = False
                    player.powerupsGotten += 1
                    if powerup.type == 0:
                        player.hasSavingGrace = True

                    elif powerup.type == 1:
                        player.hasDoubleJump = True

                    else:
                        player.hasExtraForce = True

            if good:
                goodPowerups.append(powerup)

        self.powerups = goodPowerups


        for player in self.players:
            player.handleKeys(keys)

        for player in self.players:
            if player.action:
                player.forceCooldown = player.forceCooldownDef
                player.action = False
                for other in self.players:
                    if other != player:
                        dY = other.y - player.y
                        dX = other.x - player.x

                        dist = (dY ** 2+ dX ** 2) ** (1/2)
                        if dist == 0:
                            dist = 0.01
                        xForce = dX/dist * 10000/(dist**(3/4)) + 45
                        yForce = dY/dist * 10000/(dist**(3/4)) + 45
                        if xForce < -500:
                            xForce = -500

                        if yForce < -500:
                            yForce = -500

                        if xForce > 500:
                            xForce = 500

                        if yForce > 500:
                            yForce = 300

                        if player.hasExtraForce:
                            xForce = abs(xForce) ** 1.5 * (-1 if xForce < 0 else 1)
                            yForce = abs(yForce) ** 1.5 * (-1 if yForce < 0 else 1)
                            player.hasExtraForce = False

                        other.xVel += xForce
                        other.yVel += yForce


        for player in self.players:
            w = len(self.level[self.frame][0])
            h = len(self.level[self.frame])
            prospectiveY = player.y
            didStuff = False
            for i in range(1, math.ceil(player.yVel*dt)+1):
                didStuff = True
                prospectiveY = i + player.y
                good = False
                for j in range(player.w):
                    testX = round((player.x+j) / (self.screenW / w))
                    testY = round((prospectiveY+player.h) / (self.screenH / h))
                    if (testY < 0 or testY>=h or testX<0 or testX>=w):
                        continue

                    if (self.level[self.frame][testY, testX, 0] == 0):
                        player.yVel = 0
                        good = True
                        player.onGround = True
                        break
                    # if abs(testY-100) < 20:
                    #     player.yVel = 0
                    #     good = True
                    #     player.onGround = True
                    #     break

                if good:
                    break

            if prospectiveY == player.y and player.yVel != 0:
                player.onGround = False

            if didStuff:
                player.y = prospectiveY-1

            else:
                player.y = prospectiveY

        for player in self.players:
            w = len(self.level[self.frame][0])
            h = len(self.level[self.frame])
            prospectiveY = player.y
            didStuff = False
            for i in range(-1, math.floor(player.yVel*dt)-1, -1):
                didStuff = True
                prospectiveY = i + player.y
                good = False
                for j in range(player.w):
                    testX = round((player.x+j) / (self.screenW / w))
                    testY = round((prospectiveY) / (self.screenH / h))
                    if (testY < 0 or testY>=h or testX<0 or testX>=w):
                        continue

                    if (self.level[self.frame][testY, testX, 0] == 0):
                        player.yVel = 0
                        good = True
                        break

                if good:
                    break

            if didStuff:
                player.y = prospectiveY+1

            else:
                player.y = prospectiveY

        for player in self.players:
            w = len(self.level[self.frame][0])
            h = len(self.level[self.frame])
            prospectiveX = player.x
            didStuff = False

            for i in range(math.ceil(player.xVel*dt)):
                didStuff = True
                prospectiveX = i + player.x
                good = False
                for j in range(player.h-1):
                    testY = round((player.y+j) / (self.screenH / h))
                    testX = round((prospectiveX+player.w) / (self.screenW / w))
                    if (testY < 0 or testY>=h or testX<0 or testX>=w):
                        continue

                    if (self.level[self.frame][testY, testX, 0] == 0):
                        player.xVel = 0
                        good = True
                        break

                    # if abs(testX - 100) < 20:
                    #     print("hi")
                    #     player.xVel = 0
                    #     good = True
                    #     break

                if good:
                    break

            if didStuff:
                player.x = prospectiveX-1

            else:
                player.x = prospectiveX

        for player in self.players:
            w = len(self.level[self.frame][0])
            h = len(self.level[self.frame])
            prospectiveX = player.x
            didStuff = False
            for i in range(-1, math.floor(player.xVel*dt)-1, -1):
                didStuff = True
                prospectiveX = i + player.x
                good = False
                for j in range(player.h-1):
                    testY = round((player.y+j) / (self.screenH / h))
                    testX = round((prospectiveX) / (self.screenW / w))
                    if (testY < 0 or testY>=h or testX<0 or testX>=w):
                        continue

                    if (self.level[self.frame][testY, testX, 0] == 0):
                        player.xVel = 0
                        good = True
                        break

                    # if abs(testX - 100) < 20:
                    #     print("hi 2")
                    #     player.xVel = 0
                    #     good = True
                    #     break

                if good:
                    break

            if didStuff:
                player.x = prospectiveX + 1

            else:
                player.x = prospectiveX

        for player in self.players:
            player.tick(keys, dt)

    def render(self, screen):
        if self.delay < 5:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(100, 0, self.screenW-200, 50))
            Text("GRACE PERIOD: USE WASD/IJKL TO MOVE TO STARTING SPOT", ("Calibri", 14), (0, 0, 0), (110, 10)).render(screen)
            Text(f"{round(5-self.delay)} secs remaining", ("Calibri", 14), (0, 0, 0), (110, 30)).render(screen)

        for player in self.players:
            screen.blit(player.get_render(), (player.x, player.y))

        p1 = self.players[0]
        Text("Player 1", ("Calibri", 18), (0, 0, 0), (10, 10)).render(screen)
        if p1.hasDoubleJump:
            screen.blit(pygame.transform.scale(loader.load_image(f"{self.workingDir}/resources/sprites/double_jump.png"),
                                               (32, 32)), (10, 40))

        if p1.hasExtraForce:
            screen.blit(pygame.transform.scale(loader.load_image(f"{self.workingDir}/resources/sprites/force_field_icon.png"),
                                       (32, 32)), (50, 40))

        if p1.hasSavingGrace:
            screen.blit(pygame.transform.scale(loader.load_image(f"{self.workingDir}/resources/sprites/balloon_save.png"),
                                       (32, 32)), (90, 40))

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10, 80, 100, 20))
        if p1.forceCooldown == 0:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 80, 100*(1-p1.forceCooldown/p1.forceCooldownDef), 20))

        else:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(10, 80, 100 * (1 - p1.forceCooldown / p1.forceCooldownDef), 20))

        p2 = self.players[1]

        Text("Player 2", ("Calibri", 18), (0, 0, 0), (self.screenW - 60 - 10, 10)).render(screen)
        if p2.hasDoubleJump:
            screen.blit(
                pygame.transform.scale(loader.load_image(f"{self.workingDir}/resources/sprites/double_jump.png"),
                                       (32, 32)), (self.screenW - 10 - 80 - 32, 40))

        if p2.hasExtraForce:
            screen.blit(
                pygame.transform.scale(loader.load_image(f"{self.workingDir}/resources/sprites/force_field_icon.png"),
                                       (32, 32)), (self.screenW - 10 - 40 - 32, 40))

        if p2.hasSavingGrace:
            screen.blit(
                pygame.transform.scale(loader.load_image(f"{self.workingDir}/resources/sprites/balloon_save.png"),
                                       (32, 32)), (self.screenW - 10 - 32, 40))

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.screenW - 10 - 100, 80, 100, 20))
        if p2.forceCooldown == 0:
            pygame.draw.rect(screen, (0, 255, 0),
                             pygame.Rect(self.screenW - 10 - 100, 80, 100 * (1 - p2.forceCooldown / p2.forceCooldownDef), 20))

        else:
            pygame.draw.rect(screen, (255, 255, 0),
                             pygame.Rect(self.screenW - 10 - 100, 80, 100 * (1 - p2.forceCooldown / p2.forceCooldownDef), 20))

        [powerup.render(screen) for powerup in self.powerups]

    def preGame(self, dt, keys):
        SPEED = 120
        p1 = self.players[0]
        if (keys[pygame.K_a]):
            p1.x -= SPEED * dt

        if (keys[pygame.K_d]):
            p1.x += SPEED * dt

        if (keys[pygame.K_w]):
            p1.y -= SPEED * dt

        if (keys[pygame.K_s]):
            p1.y += SPEED * dt

        p2 = self.players[1]
        if (keys[pygame.K_j]):
            p2.x -= SPEED * dt

        if (keys[pygame.K_l]):
            p2.x += SPEED * dt

        if (keys[pygame.K_i]):
            p2.y -= SPEED * dt

        if (keys[pygame.K_k]):
            p2.y += SPEED * dt

    def renderResult(self, screen):
        p1 = self.players[0]
        p2 = self.players[1]
        Text(f"Time: {round(p1.timeAlive, 2)} secs * 50 \n= {round(p1.timeAlive * 50, 2)} pts", ("Calibri", 21), (0, 0, 0), (10, 10)).render(screen)
        Text(f"Survival: {1000 if p1.alive else 0} pts", ("Calibri", 21), (0, 0, 0), (10, 70)).render(screen)
        Text(f"Other Survival: {0 if p2.alive else 1000} pts", ("Calibri", 21), (0, 0, 0), (10, 100)).render(screen)
        Text(f"Avr. Altitude: {round(p1.altitudePoints/p1.altitudeQueries)} * 5\n= {round(p1.altitudePoints/p1.altitudeQueries * 5)} pts", ("Calibri", 21), (0, 0, 0), (10, 130)).render(screen)
        Text(f"Powerups: {p1.powerupsGotten} x 100\n={p1.powerupsGotten*100} pts", ("Calibri", 21), (0, 0, 0), (10, 190)).render(screen)

        p1Total = p1.timeAlive * 50 + (1000 if p1.alive else 0) + (0 if p2.alive else 1000) + p1.altitudePoints/p1.altitudeQueries * 5 + p1.powerupsGotten * 100

        Text(f"TOTAL POINTS:\n{round(p1Total, 2)}", ("Calibri", 42), (0, 0, 0), (10, 240)).render(screen)

        Text(f"Time Survived: {round(p2.timeAlive, 2)} secs * 50 \n= {round(p2.timeAlive * 50, 2)} pts", ("Calibri", 21), (0, 0, 0),
             (310, 10)).render(screen)
        Text(f"Survival: {1000 if p2.alive else 0} pts", ("Calibri", 21), (0, 0, 0), (310, 70)).render(screen)
        Text(f"Other Survival: {0 if p1.alive else 1000} pts", ("Calibri", 21), (0, 0, 0), (310, 100)).render(screen)
        Text(
            f"Avr. Altitude: {round(p2.altitudePoints / p2.altitudeQueries, 2)} * 5\n= {round(p2.altitudePoints / p2.altitudeQueries * 5, 2)} pts",
            ("Calibri", 21), (0, 0, 0), (310, 130)).render(screen)
        Text(f"Powerups: {p2.powerupsGotten} x 100\n={p2.powerupsGotten*100} pts", ("Calibri", 21), (0, 0, 0), (310, 190)).render(screen)

        p2Total = p2.timeAlive * 50 + (1000 if p2.alive else 0) + (
            0 if p1.alive else 1000) + p2.altitudePoints / p2.altitudeQueries * 5 + p2.powerupsGotten * 100

        Text(f"TOTAL POINTS:\n{round(p2Total, 2)}", ("Calibri", 42), (0, 0, 0), (310, 240)).render(screen)

        if p1Total > p2Total:
            Text("WINNER!", ("Trebuchet", 48), (255, 197, 0), (10, self.screenH-60)).render(screen)

        else:
            Text("WINNER!", ("Trebuchet", 48), (255, 197, 0), (310, self.screenH-60)).render(screen)
