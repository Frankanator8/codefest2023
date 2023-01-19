import pygame
import loader

class Player:
    XVEL = 80
    JUMP = -200
    DOWN = 200

    GRAVITY = 600
    FRICTION = 500

    def __init__(self, x, y, w, h, facingLeft, playerNumber, workingDir, screenW, screenH):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.facingLeft = facingLeft
        self.playerNumb = playerNumber
        self.yVel = 0
        self.xVel = 0
        self.action = False
        self.workingdir = workingDir

        self.hasDoubleJump = False
        self.hasExtraForce = False
        self.hasSavingGrace = False

        self.animationCycle = 0
        self.animationNextTick = 0

        self.forceCooldown = 0
        self.forceCooldownDef = 1

        self.prevKeys = []
        self.alive = True
        self.timeAlive = 0

        self.screenW = screenW
        self.screenH = screenH
        self.altitudePoints = 0
        self.altitudeQueries = 0
        self.powerupsGotten = 0
        self.onGround = False
        self.saveTime = 0


    def reset(self):
        self.xVel = 0
        self.yVel = 0
        self.x = 0
        self.y = 0
        self.altitudePoints = 0
        self.altitudeQueries = 0
        self.powerupsGotten = 0
        self.alive = True
        self.forceCooldown = 0
        self.hasDoubleJump = False
        self.hasExtraForce = False
        self.hasSavingGrace = False
        self.action = False

        self.saveTime = 0


    def handleKeys(self, keys):
        if self.alive:
            if self.playerNumb == 1:
                if (keys[pygame.K_a]):
                    self.facingLeft = True
                    self.xVel = -Player.XVEL

                if (keys[pygame.K_d]):
                    self.facingLeft = False
                    self.xVel = Player.XVEL

                if (keys[pygame.K_w]):
                    if self.onGround:
                        self.yVel = Player.JUMP

                    else:
                        if self.hasDoubleJump:
                            if not self.prevKeys[pygame.K_w]:
                                self.yVel = Player.JUMP
                                self.hasDoubleJump = False

                if (keys[pygame.K_s]):
                    self.yVel = Player.DOWN

                if (keys[pygame.K_e]):
                    if (not self.prevKeys[pygame.K_e]):
                        if self.forceCooldown == 0:
                            self.action = True

            else:
                if (keys[pygame.K_j]):
                    self.facingLeft = True
                    self.xVel = -Player.XVEL

                if (keys[pygame.K_l]):
                    self.facingLeft = False
                    self.xVel = Player.XVEL

                if (keys[pygame.K_i]):
                    if self.onGround:
                        self.yVel = Player.JUMP

                    else:
                        if self.hasDoubleJump:
                            if not self.prevKeys[pygame.K_w]:
                                self.yVel = Player.JUMP
                                self.hasDoubleJump = False

                if (keys[pygame.K_k]):
                    self.yVel = Player.DOWN

                if (keys[pygame.K_o]):
                    if (not self.prevKeys[pygame.K_o]):
                        if self.forceCooldown == 0:
                            self.action = True

        self.prevKeys = keys

    def tick(self, keys, dt):
        if self.alive:
            if self.saveTime > 0:
                self.saveTime -= dt
                self.yVel = -50

            else:
                self.saveTime = 0
            self.altitudeQueries += 1
            self.altitudePoints += self.y
            self.timeAlive += dt
            self.y += self.yVel * dt
            self.yVel += Player.GRAVITY * dt
            self.x += self.xVel * dt
            if self.xVel > 0:
                self.xVel -= Player.FRICTION * dt

            else:
                self.xVel += Player.FRICTION * dt

            if abs(self.xVel) < Player.FRICTION * 0.05:
                self.xVel = 0

            # self.handleKeys(keys)

            if self.forceCooldown > 0:
                self.forceCooldown -= min(dt, self.forceCooldown)

            else:
                self.forceCooldown = 0

            if self.x < 0:
                self.x = 0
                self.xVel = 0

            if self.x > self.screenW-self.w:
                self.x = self.screenW-self.w
                self.xVel = 0

            if self.y < -50:
                self.y = -50
                self.yVel = 0

            if self.y > self.screenH-self.h:
                self.y = self.screenH-self.h
                self.yVel = 0
                if self.hasSavingGrace:
                    self.y -= 10
                    self.saveTime = 5
                    self.hasSavingGrace = False

                else:
                    self.alive = False

            self.animationNextTick += dt
            if self.animationNextTick < 1/4:
                self.animationCycle = 1 - self.animationCycle
                self.animationNextTick = 0


    def get_render(self):
        if self.facingLeft:
            direction = "left"

        else:
            direction = "right"

        if self.yVel < 0:
            img = f"clown{self.playerNumb}_jump_{direction}_0.png"


        elif self.yVel > 0:
            img = f"clown{self.playerNumb}_fall_{direction}_0.png"

        else:
            if self.xVel == 0:
                img = f"clown{self.playerNumb}_idle_{direction}_{self.animationCycle}.png"

            else:
                img = f"clown{self.playerNumb}_run_{direction}_{self.animationCycle}.png"

        img = pygame.transform.scale(loader.load_image(f"{self.workingdir}/resources/sprites/{img}"), (self.w, self.h))
        if not self.alive:
            img.fill((255, 255, 255, 200), None, pygame.BLEND_RGBA_MULT)
        return img
