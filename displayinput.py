import pygame as pg

class DisplayInputs():
    def __init__(self, write, x, y, activeCol, inactiveCol):
        self.content = write
        self.x = x
        self.y = y
        self.actCol = activeCol
        self.inactCol = inactiveCol
        self.color = inactiveCol
        self.clicked = False

    def draw(self, screen):
        basicfont = pg.font.SysFont(None, 48)
        self.printContent = basicfont.render(self.content, False, self.color, (0, 0, 0))
        self.textrect = self.printContent.get_rect()

        self.textrect.centerx = self.x
        self.textrect.centery = self.y
        screen.blit(self.printContent, self.textrect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.textrect.collidepoint(event.pos):
            if self.color == self.actCol:
                self.color = self.inactCol
                self.clicked = not self.clicked
                return self
            else:
                self.color = self.actCol
                self.clicked = not self.clicked
                return self
        return 0
